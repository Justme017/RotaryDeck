import json
import tempfile
import unittest
from pathlib import Path

import deck_sync
import model

DEFAULT = Path(__file__).parent / 'profiles' / 'default.json'


class FakeDeckTransport:
    def __init__(self, *, max_profile_bytes=4096, max_frame_payload=64, timeout_once_on_begin=False,
                 disconnect_on_commit=False, bad_sequence_ack=False, bad_digest_error=False,
                 storage_error=False, readback_mismatch=False, malformed_caps=False):
        self.capabilities = {
            'protocol_version': deck_sync.PROTOCOL_VERSION,
            'schema_version': deck_sync.SCHEMA_VERSION,
            'max_profile_bytes': max_profile_bytes,
            'max_frame_payload': max_frame_payload,
            'encrypted_write': True,
        }
        self.timeout_once_on_begin = timeout_once_on_begin
        self.disconnect_on_commit = disconnect_on_commit
        self.bad_sequence_ack = bad_sequence_ack
        self.bad_digest_error = bad_digest_error
        self.storage_error = storage_error
        self.readback_mismatch = readback_mismatch
        self.malformed_caps = malformed_caps

        self.active_tx = None
        self.expected_seq = 0
        self.buffer = bytearray()
        self.begin_meta = {}
        self.timeout_used = False

    def request(self, frame: bytes, timeout_seconds: float) -> bytes:
        kind, tx_id, sequence, _, payload = deck_sync.SyncCodec.decode(frame)
        if kind == deck_sync.FRAME_CAPS_REQUEST:
            if self.malformed_caps:
                body = b'not-json'
            else:
                body = json.dumps(self.capabilities).encode('utf-8')
            return deck_sync.SyncCodec.encode(deck_sync.FRAME_CAPS_RESPONSE, 0, 0, body)

        if kind == deck_sync.FRAME_BEGIN:
            if self.timeout_once_on_begin and not self.timeout_used:
                self.timeout_used = True
                raise TimeoutError('lost ack')
            self.active_tx = tx_id
            self.expected_seq = 0
            self.buffer = bytearray()
            self.begin_meta = json.loads(payload.decode('utf-8'))
            ack_sequence = 99 if self.bad_sequence_ack else 0
            return self._ack(tx_id, ack_sequence)

        if kind == deck_sync.FRAME_DATA:
            if tx_id != self.active_tx:
                return self._error(tx_id, deck_sync.ERROR_BAD_SEQUENCE)
            if sequence != self.expected_seq:
                return self._error(tx_id, deck_sync.ERROR_BAD_SEQUENCE)
            self.buffer.extend(payload)
            self.expected_seq += 1
            return self._ack(tx_id, sequence)

        if kind == deck_sync.FRAME_COMMIT:
            if self.disconnect_on_commit:
                raise ConnectionError('disconnect')
            if self.storage_error:
                return self._error(tx_id, deck_sync.ERROR_STORAGE_FAILED)
            digest = self.begin_meta.get('digest')
            length = self.begin_meta.get('length')
            computed = deck_sync.hashlib.sha256(bytes(self.buffer)).hexdigest()
            if self.bad_digest_error or digest != computed or length != len(self.buffer):
                return self._error(tx_id, deck_sync.ERROR_BAD_DIGEST)
            applied = {
                'revision': int(self.begin_meta.get('revision', -1)),
                'digest': computed,
            }
            return deck_sync.SyncCodec.encode(deck_sync.FRAME_APPLIED, tx_id, sequence, json.dumps(applied).encode('utf-8'))

        if kind == deck_sync.FRAME_READBACK_REQUEST:
            digest = deck_sync.hashlib.sha256(bytes(self.buffer)).hexdigest()
            if self.readback_mismatch:
                digest = '0' * 64
            readback = {
                'revision': int(self.begin_meta.get('revision', -1)),
                'digest': digest,
            }
            return deck_sync.SyncCodec.encode(deck_sync.FRAME_READBACK, tx_id, 0, json.dumps(readback).encode('utf-8'))

        if kind == deck_sync.FRAME_CANCEL:
            return self._ack(tx_id, 0)

        return self._error(tx_id, 'UNKNOWN')

    @staticmethod
    def _ack(tx_id: int, sequence: int) -> bytes:
        return deck_sync.SyncCodec.encode(deck_sync.FRAME_ACK, tx_id, sequence, json.dumps({'sequence': sequence}).encode('utf-8'))

    @staticmethod
    def _error(tx_id: int, code: str) -> bytes:
        return deck_sync.SyncCodec.encode(deck_sync.FRAME_ERROR, tx_id, 0, json.dumps({'code': code}).encode('utf-8'))


class SyncTests(unittest.TestCase):
    def setUp(self):
        self.profile = model.load_profile(DEFAULT)

    def test_codec_rejects_malformed_frame(self):
        with self.assertRaises(deck_sync.SyncProtocolError):
            deck_sync.SyncCodec.decode(b'bad')

    def test_prepare_payload_uses_bounded_metadata(self):
        payload, digest = deck_sync.prepare_payload(self.profile)
        text = payload.decode('utf-8')
        self.assertIn('display_label', text)
        self.assertNotIn('https://www.netflix.com', text)
        self.assertEqual(len(digest), 64)

    def test_sync_success_with_chunk_boundaries(self):
        transport = FakeDeckTransport(max_frame_payload=deck_sync.HEADER.size + 24)
        client = deck_sync.DeckSyncClient(transport, retries=0)
        state = client.sync_profile(self.profile, revision=7)
        self.assertEqual(state.revision, 7)
        self.assertEqual(len(state.digest), 64)

    def test_sync_rejects_oversize_payload(self):
        transport = FakeDeckTransport(max_profile_bytes=80)
        client = deck_sync.DeckSyncClient(transport, retries=0)
        with self.assertRaises(deck_sync.SyncProtocolError):
            client.sync_profile(self.profile, revision=1)

    def test_sync_rejects_bad_sequence_ack(self):
        transport = FakeDeckTransport(bad_sequence_ack=True)
        client = deck_sync.DeckSyncClient(transport, retries=0)
        with self.assertRaises(deck_sync.RetryableSyncError):
            client.sync_profile(self.profile, revision=1)

    def test_sync_rejects_bad_digest(self):
        transport = FakeDeckTransport(bad_digest_error=True)
        client = deck_sync.DeckSyncClient(transport, retries=0)
        with self.assertRaises(deck_sync.SyncProtocolError):
            client.sync_profile(self.profile, revision=1)

    def test_sync_retries_after_lost_ack(self):
        transport = FakeDeckTransport(timeout_once_on_begin=True)
        client = deck_sync.DeckSyncClient(transport, retries=1)
        state = client.sync_profile(self.profile, revision=8)
        self.assertEqual(state.revision, 8)

    def test_sync_disconnect_raises(self):
        transport = FakeDeckTransport(disconnect_on_commit=True)
        client = deck_sync.DeckSyncClient(transport, retries=0)
        with self.assertRaises(deck_sync.SyncDisconnectError):
            client.sync_profile(self.profile, revision=8)

    def test_sync_storage_failure_reports_retryable(self):
        transport = FakeDeckTransport(storage_error=True)
        client = deck_sync.DeckSyncClient(transport, retries=0)
        with self.assertRaises(deck_sync.RetryableSyncError):
            client.sync_profile(self.profile, revision=8)

    def test_sync_readback_mismatch(self):
        transport = FakeDeckTransport(readback_mismatch=True)
        client = deck_sync.DeckSyncClient(transport, retries=0)
        with self.assertRaises(deck_sync.SyncReadbackMismatchError):
            client.sync_profile(self.profile, revision=9)

    def test_capability_discovery_rejects_old_protocol(self):
        transport = FakeDeckTransport()
        transport.capabilities['protocol_version'] = 0
        client = deck_sync.DeckSyncClient(transport)
        with self.assertRaises(deck_sync.SyncUnsupportedError):
            client.sync_profile(self.profile, revision=2)

    def test_capability_discovery_rejects_malformed_response(self):
        transport = FakeDeckTransport(malformed_caps=True)
        client = deck_sync.DeckSyncClient(transport)
        with self.assertRaises(deck_sync.SyncUnsupportedError):
            client.sync_profile(self.profile, revision=2)

    def test_activation_router_deduplicates_and_rejects_stale(self):
        router = deck_sync.ActivationRouter()
        calls = []
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            self.profile['apps'][0] = {'slot': 1, 'label': 'FILES', 'type': 'open_folder', 'target': str(folder)}
            router.bind_profile(self.profile, revision=4, session_id='abc')
            event = json.dumps({'session_id': 'abc', 'event_sequence': 12, 'revision': 4, 'group': 'apps', 'slot': 1}).encode('utf-8')
            stale = json.dumps({'session_id': 'old', 'event_sequence': 13, 'revision': 4, 'group': 'apps', 'slot': 1}).encode('utf-8')
            self.assertTrue(router.handle_event(event, calls.append))
            self.assertFalse(router.handle_event(event, calls.append))
            self.assertFalse(router.handle_event(stale, calls.append))
        self.assertEqual(len(calls), 1)

    def test_activation_router_rejects_unknown_and_builtin(self):
        router = deck_sync.ActivationRouter()
        calls = []
        router.bind_profile(self.profile, revision=3, session_id='s')
        unknown = json.dumps({'session_id': 's', 'event_sequence': 1, 'revision': 3, 'group': 'apps', 'slot': 99}).encode('utf-8')
        builtin = json.dumps({'session_id': 's', 'event_sequence': 2, 'revision': 3, 'group': 'actions', 'slot': 1}).encode('utf-8')
        self.assertFalse(router.handle_event(unknown, calls.append))
        self.assertFalse(router.handle_event(builtin, calls.append))
        self.assertEqual(calls, [])

    def test_render_label_truncates_by_width(self):
        rendered = deck_sync.render_label('SPOTIFY MUSIC', 3)
        self.assertTrue(rendered.endswith('…'))


if __name__ == '__main__':
    unittest.main(verbosity=2)
