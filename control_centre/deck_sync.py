import hashlib
import queue
import json
import os
import struct
import threading
import time
import uuid
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
FRAGMENT_MAGIC = 0xA5
FRAGMENT_HEADER = struct.Struct('!BBH')
FRAGMENT_PAYLOAD_MAX = 20 - FRAGMENT_HEADER.size
FRAGMENT_FLAG_START = 0x01
FRAGMENT_FLAG_END = 0x02


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
    session_id: str = ''


class SyncTransport(Protocol):
    def request(self, frame: bytes, timeout_seconds: float) -> bytes:
        ...


class _FragmentAssembler:
    def __init__(self):
        self._expected = None
        self._buffer = bytearray()

    def push(self, packet: bytes) -> Optional[bytes]:
        if len(packet) < FRAGMENT_HEADER.size:
            raise SyncProtocolError('Fragment too short.')
        magic, flags, sequence = FRAGMENT_HEADER.unpack(packet[:FRAGMENT_HEADER.size])
        if magic != FRAGMENT_MAGIC:
            raise SyncProtocolError('Fragment magic mismatch.')
        if flags & FRAGMENT_FLAG_START:
            self._expected = sequence
            self._buffer = bytearray()
        if self._expected is None:
            raise SyncProtocolError('Fragment stream did not start.')
        if sequence != self._expected:
            raise SyncProtocolError(ERROR_BAD_SEQUENCE)
        self._buffer.extend(packet[FRAGMENT_HEADER.size:])
        self._expected = (self._expected + 1) & 0xFFFF
        if flags & FRAGMENT_FLAG_END:
            frame = bytes(self._buffer)
            self._expected = None
            self._buffer = bytearray()
            return frame
        return None


def split_fragments(frame: bytes, sequence_start: int = 0) -> List[bytes]:
    fragments = []
    sequence = sequence_start & 0xFFFF
    chunks = [frame[index:index + FRAGMENT_PAYLOAD_MAX] for index in range(0, len(frame), FRAGMENT_PAYLOAD_MAX)] or [b'']
    for index, chunk in enumerate(chunks):
        flags = 0
        if index == 0:
            flags |= FRAGMENT_FLAG_START
        if index == len(chunks) - 1:
            flags |= FRAGMENT_FLAG_END
        fragments.append(FRAGMENT_HEADER.pack(FRAGMENT_MAGIC, flags, sequence) + chunk)
        sequence = (sequence + 1) & 0xFFFF
    return fragments


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


class WinRTSyncTransport:
    """Windows BLE transport for v2.3 config/control/status characteristics."""

    def __init__(self, device_name: str = 'Rotary Deck'):
        self.device_name = device_name
        self._loop = None
        self._device = None
        self._service = None
        self._control = None
        self._status = None
        self._token = None
        self._queue: "queue.Queue[bytes]" = queue.Queue()
        self._fragment_sequence = int.from_bytes(os.urandom(2), 'big')
        self._guard = threading.Lock()

    def request(self, frame: bytes, timeout_seconds: float) -> bytes:
        if os.name != 'nt':
            raise ConnectionError('Windows WinRT transport required for live deck sync.')
        with self._guard:
            if self._loop is None:
                self._open()
            self._queue = queue.Queue()
            for fragment in split_fragments(frame, self._fragment_sequence):
                self._write_fragment(fragment, timeout_seconds)
                self._fragment_sequence = (self._fragment_sequence + 1) & 0xFFFF
            assembler = _FragmentAssembler()
            deadline = time.monotonic() + timeout_seconds
            while True:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise TimeoutError('Timed out waiting for status response.')
                packet = self._queue.get(timeout=remaining)
                maybe = assembler.push(packet)
                if maybe is not None:
                    return maybe

    def close(self) -> None:
        if self._loop is None:
            return
        try:
            if self._status is not None and self._token is not None:
                self._run(self._status.remove_value_changed(self._token), 5)
        except Exception:
            pass
        for handle in (self._service, self._device):
            try:
                if handle is not None:
                    handle.close()
            except Exception:
                pass
        self._loop = None
        self._device = self._service = self._control = self._status = self._token = None

    def _open(self) -> None:
        import asyncio
        self._loop = asyncio.new_event_loop()
        selector = self._run(self._find_selector(), 20)
        self._device = self._run(self._open_device(selector), 20)
        self._service, self._control, self._status = self._run(self._resolve_chars(), 20)
        self._token = self._status.add_value_changed(self._on_status)
        self._run(self._enable_notifications(), 10)

    async def _find_selector(self):
        from winrt.windows.devices.bluetooth import BluetoothLEDevice
        from winrt.windows.devices.enumeration import DeviceInformation
        selector = BluetoothLEDevice.get_device_selector_from_pairing_state(True)
        devices = None
        method = getattr(DeviceInformation, 'find_all_async_aqs_filter', None)
        if method is not None:
            devices = await method(selector)
        if devices is None:
            method = getattr(DeviceInformation, 'find_all_async_aqs_filter_and_additional_properties', None)
            if method is not None:
                devices = await method(selector, [])
        if devices is None:
            method = getattr(DeviceInformation, 'find_all_async', None)
            if method is not None:
                try:
                    devices = await method(selector, [])
                except TypeError:
                    devices = await method(selector)
        if devices is None:
            raise ConnectionError('Windows DeviceInformation enumeration overloads unavailable.')
        match = [d for d in devices if d.name.casefold() == self.device_name.casefold()]
        if len(match) != 1:
            raise ConnectionError('Could not resolve a unique paired Rotary Deck device.')
        return match[0]

    async def _open_device(self, info):
        from winrt.windows.devices.bluetooth import BluetoothLEDevice
        device = await BluetoothLEDevice.from_id_async(info.id)
        if device is None:
            raise ConnectionError('Unable to open paired deck device.')
        return device

    async def _resolve_chars(self):
        from winrt.windows.devices.bluetooth import BluetoothCacheMode
        from winrt.windows.devices.bluetooth.genericattributeprofile import GattCommunicationStatus
        service_result = await self._device.get_gatt_services_for_uuid_with_cache_mode_async(uuid.UUID(CONFIG_SERVICE_UUID), BluetoothCacheMode.UNCACHED)
        if service_result.status != GattCommunicationStatus.SUCCESS or len(service_result.services) != 1:
            raise ConnectionError('v2.3 config service unavailable on this firmware.')
        service = service_result.services[0]
        control_result = await service.get_characteristics_for_uuid_with_cache_mode_async(uuid.UUID(CONFIG_CONTROL_UUID), BluetoothCacheMode.UNCACHED)
        status_result = await service.get_characteristics_for_uuid_with_cache_mode_async(uuid.UUID(CONFIG_STATUS_UUID), BluetoothCacheMode.UNCACHED)
        if control_result.status != GattCommunicationStatus.SUCCESS or len(control_result.characteristics) != 1:
            raise ConnectionError('v2.3 control characteristic missing.')
        if status_result.status != GattCommunicationStatus.SUCCESS or len(status_result.characteristics) != 1:
            raise ConnectionError('v2.3 status characteristic missing.')
        return service, control_result.characteristics[0], status_result.characteristics[0]

    async def _enable_notifications(self):
        from winrt.windows.devices.bluetooth.genericattributeprofile import GattClientCharacteristicConfigurationDescriptorValue, GattCommunicationStatus
        result = await self._status.write_client_characteristic_configuration_descriptor_with_result_async(
            GattClientCharacteristicConfigurationDescriptorValue.NOTIFY
        )
        if result.status != GattCommunicationStatus.SUCCESS:
            raise ConnectionError('Unable to subscribe to v2.3 status notifications.')

    def _on_status(self, sender, args):
        if args is None or args.characteristic_value is None:
            return
        data = bytes(args.characteristic_value)
        self._queue.put(data)

    def _write_fragment(self, fragment: bytes, timeout_seconds: float) -> None:
        from winrt.windows.storage.streams import DataWriter
        from winrt.windows.devices.bluetooth.genericattributeprofile import GattWriteOption, GattCommunicationStatus
        writer = DataWriter()
        writer.write_bytes(fragment)
        buffer = writer.detach_buffer()
        writer.close()
        result = self._run(self._control.write_value_with_result_and_option_async(buffer, GattWriteOption.WRITE_WITH_RESPONSE), timeout_seconds)
        if result.status != GattCommunicationStatus.SUCCESS:
            raise ConnectionError(f'GATT write failed: {result.status}')

    def _run(self, operation, timeout: float):
        import asyncio
        return self._loop.run_until_complete(asyncio.wait_for(operation, timeout))


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
        session_id = f'{revision:08x}{tx_id:04x}'
        begin = _canonical_json_bytes({'revision': revision, 'length': len(payload), 'digest': digest, 'session_id': session_id})
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
        if 'session_id' in applied and applied.get('session_id') != session_id:
            raise SyncProtocolError('APPLIED session mismatch.')

        kind, response_tx, _, _, response_payload = self._exchange(SyncCodec.encode(FRAME_READBACK_REQUEST, tx_id, 0))
        if kind != FRAME_READBACK or response_tx != tx_id:
            raise SyncProtocolError('Expected READBACK response.')
        readback = _decode_json(response_payload)
        state = ReadbackState(
            revision=int(readback.get('revision', -1)),
            digest=str(readback.get('digest', '')),
            session_id=str(readback.get('session_id', session_id)),
        )
        if state.revision != revision or state.digest != digest:
            raise SyncReadbackMismatchError('Readback mismatch.')
        if state.session_id != session_id:
            raise SyncReadbackMismatchError('Readback session mismatch.')
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
