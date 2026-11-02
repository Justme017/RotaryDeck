import hashlib
import json
import os
import struct
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, List, Optional, Protocol, Tuple

from model import ProfileError, valid_url, validate

TELEMETRY_SERVICE_UUID = '917e0001-d588-4b6b-a9a0-a81a964ce2b1'
TELEMETRY_RX_UUID = '917e0002-d588-4b6b-a9a0-a81a964ce2b1'

# v2.3 config endpoints are separate from existing telemetry endpoints.
CONFIG_SERVICE_UUID = '917e1001-d588-4b6b-a9a0-a81a964ce2b1'
CONFIG_CONTROL_UUID = '917e1002-d588-4b6b-a9a0-a81a964ce2b1'
CONFIG_STATUS_UUID = '917e1003-d588-4b6b-a9a0-a81a964ce2b1'

PROTOCOL_VERSION = 1
SCHEMA_VERSION = 1

FRAME_CAPS_REQUEST = 0x01
FRAME_CAPS_RESPONSE = 0x02
FRAME_BEGIN = 0x10
FRAME_DATA = 0x11
FRAME_COMMIT = 0x12
FRAME_CANCEL = 0x13
FRAME_READBACK_REQUEST = 0x14
FRAME_ACK = 0x20
FRAME_APPLIED = 0x21
FRAME_READBACK = 0x22
FRAME_ERROR = 0x23
FRAME_ACTIVATION = 0x30

ERROR_UNSUPPORTED_PROTOCOL = 'UNSUPPORTED_PROTOCOL'
ERROR_TOO_LARGE = 'TOO_LARGE'
ERROR_BAD_SEQUENCE = 'BAD_SEQUENCE'
ERROR_BAD_DIGEST = 'BAD_DIGEST'
ERROR_BAD_SCHEMA = 'BAD_SCHEMA'
ERROR_STORAGE_FAILED = 'STORAGE_FAILED'
ERROR_REVISION_CONFLICT = 'REVISION_CONFLICT'
ERROR_TIMEOUT = 'TIMEOUT'

HEADER = struct.Struct('!2sBBHHBH')
MAGIC = b'RD'

LABEL_MAX_PIXELS = 72
ELLIPSIS = '…'


class SyncError(RuntimeError):
    pass


class SyncUnsupportedError(SyncError):
    pass


class SyncTimeoutError(SyncError):
    pass


class SyncDisconnectError(SyncError):
    pass


class SyncReadbackMismatchError(SyncError):
    pass


class SyncProtocolError(SyncError):
    pass


class RetryableSyncError(SyncError):
    pass


@dataclass(frozen=True)
class Capabilities:
    protocol_version: int
    schema_version: int
    max_profile_bytes: int
    max_frame_payload: int
    encrypted_write: bool


@dataclass(frozen=True)
class ReadbackState:
    revision: int
    digest: str


class SyncTransport(Protocol):
    def request(self, frame: bytes, timeout_seconds: float) -> bytes:
        ...


class SyncCodec:
    @staticmethod
    def encode(kind: int, tx_id: int, sequence: int, payload: bytes = b'', flags: int = 0) -> bytes:
        if not isinstance(payload, (bytes, bytearray)):
            raise SyncProtocolError('Payload must be bytes.')
        if len(payload) > 0xFFFF:
            raise SyncProtocolError('Frame payload exceeds 65535 bytes.')
        return HEADER.pack(MAGIC, PROTOCOL_VERSION, kind, tx_id & 0xFFFF, sequence & 0xFFFF, flags & 0xFF, len(payload)) + bytes(payload)

    @staticmethod
    def decode(frame: bytes) -> Tuple[int, int, int, int, bytes]:
        if len(frame) < HEADER.size:
            raise SyncProtocolError('Frame too short.')
        magic, version, kind, tx_id, sequence, flags, length = HEADER.unpack(frame[:HEADER.size])
        if magic != MAGIC:
            raise SyncProtocolError('Invalid frame magic.')
        if version != PROTOCOL_VERSION:
            raise SyncProtocolError('Unsupported frame version.')
        payload = frame[HEADER.size:]
        if len(payload) != length:
            raise SyncProtocolError('Frame length mismatch.')
        return kind, tx_id, sequence, flags, payload


def _canonical_json_bytes(payload: Dict) -> bytes:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')


def _label_pixel_width(label: str) -> int:
    wide = set('MW@#%&')
    narrow = set('ijlI.,:;!|')
    width = 0
    for char in label:
        if char in wide:
            width += 7
        elif char in narrow:
            width += 4
        else:
            width += 6
    return width


def render_label(label: str, slot: int) -> str:
    text = (label or '').strip()
    if not text:
        return f'SLOT {slot}'
    if _label_pixel_width(text) <= LABEL_MAX_PIXELS:
        return text
    result = ''
    for char in text:
        candidate = result + char
        if _label_pixel_width(candidate + ELLIPSIS) > LABEL_MAX_PIXELS:
            break
        result = candidate
    return (result or text[:1]) + ELLIPSIS


def build_device_profile(profile: Dict) -> Dict:
    validated = validate(profile)
    payload = {
        'schema_version': SCHEMA_VERSION,
        'profile_name': validated['profile_name'],
        'apps': [],
        'actions': [],
    }
    for group in ('apps', 'actions'):
        for entry in sorted(validated[group], key=lambda item: item['slot']):
            payload[group].append({
                'slot': entry['slot'],
                'label': entry['label'],
                'display_label': render_label(entry['label'], entry['slot']),
                'type': entry['type'],
                'activation_id': f'{group}:{entry["slot"]}',
            })
    return payload


def prepare_payload(profile: Dict) -> Tuple[bytes, str]:
    payload = _canonical_json_bytes(build_device_profile(profile))
    digest = hashlib.sha256(payload).hexdigest()
    return payload, digest


class DeckSyncClient:
    def __init__(self, transport: SyncTransport, timeout_seconds: float = 3.0, retries: int = 1):
        self.transport = transport
        self.timeout_seconds = timeout_seconds
        self.retries = max(0, retries)
        self._tx_counter = int.from_bytes(os.urandom(2), 'big')

    def _next_tx_id(self) -> int:
        self._tx_counter = (self._tx_counter + 1) & 0xFFFF
        return self._tx_counter

    def _exchange(self, frame: bytes) -> Tuple[int, int, int, int, bytes]:
        try:
            response = self.transport.request(frame, self.timeout_seconds)
        except TimeoutError as exc:
            raise SyncTimeoutError(ERROR_TIMEOUT) from exc
        except ConnectionError as exc:
            raise SyncDisconnectError('DISCONNECTED') from exc
        return SyncCodec.decode(response)

    def discover_capabilities(self) -> Capabilities:
        frame = SyncCodec.encode(FRAME_CAPS_REQUEST, 0, 0)
        kind, _, _, _, payload = self._exchange(frame)
        if kind != FRAME_CAPS_RESPONSE:
            raise SyncUnsupportedError('Expected capabilities response.')
        try:
            body = json.loads(payload.decode('utf-8'))
        except (UnicodeError, json.JSONDecodeError) as exc:
            raise SyncUnsupportedError('Malformed capabilities payload.') from exc
        capabilities = Capabilities(
            protocol_version=int(body.get('protocol_version', 0)),
            schema_version=int(body.get('schema_version', 0)),
            max_profile_bytes=int(body.get('max_profile_bytes', 0)),
            max_frame_payload=int(body.get('max_frame_payload', 0)),
            encrypted_write=bool(body.get('encrypted_write', False)),
        )
        if capabilities.protocol_version != PROTOCOL_VERSION:
            raise SyncUnsupportedError(ERROR_UNSUPPORTED_PROTOCOL)
        if capabilities.schema_version != SCHEMA_VERSION:
            raise SyncUnsupportedError('Unsupported schema version.')
        if capabilities.max_profile_bytes <= 0 or capabilities.max_frame_payload <= HEADER.size:
            raise SyncUnsupportedError('Invalid capability bounds.')
        if not capabilities.encrypted_write:
            raise SyncUnsupportedError('Encrypted write endpoint is required.')
        return capabilities

    def sync_profile(self, profile: Dict, revision: int) -> ReadbackState:
        payload, digest = prepare_payload(profile)
        capabilities = self.discover_capabilities()
        if len(payload) > capabilities.max_profile_bytes:
            raise SyncProtocolError(ERROR_TOO_LARGE)
        last_error: Optional[Exception] = None
        for attempt in range(self.retries + 1):
            tx_id = self._next_tx_id()
            try:
                return self._sync_once(tx_id, revision, payload, digest, capabilities)
            except (SyncTimeoutError, SyncDisconnectError, RetryableSyncError) as exc:
                last_error = exc
                self._cancel(tx_id)
                if attempt >= self.retries:
                    raise
            except SyncError:
                self._cancel(tx_id)
                raise
        if last_error:
            raise last_error
        raise SyncError('Sync failed.')

    def _sync_once(self, tx_id: int, revision: int, payload: bytes, digest: str, capabilities: Capabilities) -> ReadbackState:
        begin = _canonical_json_bytes({'revision': revision, 'length': len(payload), 'digest': digest})
        kind, response_tx, _, _, response_payload = self._exchange(SyncCodec.encode(FRAME_BEGIN, tx_id, 0, begin))
        self._expect_ack(kind, response_tx, tx_id, 0, response_payload)

        max_data = capabilities.max_frame_payload - HEADER.size
        if max_data <= 0:
            raise SyncProtocolError('Capability frame payload too small.')
        chunks = [payload[index:index + max_data] for index in range(0, len(payload), max_data)] or [b'']
        for sequence, chunk in enumerate(chunks):
            kind, response_tx, response_seq, _, response_payload = self._exchange(SyncCodec.encode(FRAME_DATA, tx_id, sequence, chunk))
            self._expect_ack(kind, response_tx, tx_id, sequence, response_payload)
            if response_seq != sequence:
                raise RetryableSyncError(ERROR_BAD_SEQUENCE)

        kind, response_tx, _, _, response_payload = self._exchange(SyncCodec.encode(FRAME_COMMIT, tx_id, len(chunks)))
        if kind == FRAME_ERROR:
            error = _decode_error(response_payload)
            if error in (ERROR_STORAGE_FAILED, ERROR_TIMEOUT):
                raise RetryableSyncError(error)
            raise SyncProtocolError(error)
        if kind != FRAME_APPLIED or response_tx != tx_id:
            raise SyncProtocolError('Expected APPLIED response.')
        applied = _decode_json(response_payload)
        if applied.get('revision') != revision or applied.get('digest') != digest:
            raise SyncProtocolError('APPLIED revision/digest mismatch.')

        kind, response_tx, _, _, response_payload = self._exchange(SyncCodec.encode(FRAME_READBACK_REQUEST, tx_id, 0))
        if kind != FRAME_READBACK or response_tx != tx_id:
            raise SyncProtocolError('Expected READBACK response.')
        readback = _decode_json(response_payload)
        state = ReadbackState(revision=int(readback.get('revision', -1)), digest=str(readback.get('digest', '')))
        if state.revision != revision or state.digest != digest:
            raise SyncReadbackMismatchError('Readback mismatch.')
        return state

    def _cancel(self, tx_id: int) -> None:
        try:
            self._exchange(SyncCodec.encode(FRAME_CANCEL, tx_id, 0))
        except SyncError:
            pass

    @staticmethod
    def _expect_ack(kind: int, response_tx: int, tx_id: int, sequence: int, payload: bytes) -> None:
        if kind == FRAME_ERROR:
            raise SyncProtocolError(_decode_error(payload))
        if kind != FRAME_ACK or response_tx != tx_id:
            raise SyncProtocolError('Expected ACK.')
        body = _decode_json(payload)
        if int(body.get('sequence', sequence)) != sequence:
            raise RetryableSyncError(ERROR_BAD_SEQUENCE)


class ActivationRouter:
    def __init__(self):
        self._session_id = ''
        self._revision = -1
        self._slots: Dict[Tuple[str, int], Dict] = {}
        self._seen: set[Tuple[str, int]] = set()

    def bind_profile(self, profile: Dict, revision: int, session_id: str) -> None:
        validated = validate(profile)
        slots = {}
        for group in ('apps', 'actions'):
            for entry in validated[group]:
                slots[(group, entry['slot'])] = entry
        self._slots = slots
        self._revision = revision
        self._session_id = session_id
        self._seen.clear()

    def handle_event(self, event_payload: bytes, execute: Callable[[Dict], None]) -> bool:
        event = _decode_json(event_payload)
        event_session = str(event.get('session_id', ''))
        event_revision = int(event.get('revision', -1))
        sequence = int(event.get('event_sequence', -1))
        group = str(event.get('group', ''))
        slot = int(event.get('slot', 0))
        if event_session != self._session_id or event_revision != self._revision:
            return False
        token = (event_session, sequence)
        if token in self._seen:
            return False
        self._seen.add(token)
        entry = self._slots.get((group, slot))
        if not entry:
            return False
        if entry['type'] == 'open_url':
            valid_url(entry['target'])
        elif entry['type'] == 'open_folder':
            path = Path(entry['target'])
            if not path.is_absolute() or not path.is_dir():
                raise ProfileError('Select an existing absolute folder path.')
        else:
            return False
        execute(entry)
        return True


def _decode_json(payload: bytes) -> Dict:
    try:
        value = json.loads(payload.decode('utf-8'))
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise SyncProtocolError('Malformed JSON payload.') from exc
    if not isinstance(value, dict):
        raise SyncProtocolError('Expected JSON object payload.')
    return value


def _decode_error(payload: bytes) -> str:
    body = _decode_json(payload)
    code = str(body.get('code', 'UNKNOWN'))
    return code
