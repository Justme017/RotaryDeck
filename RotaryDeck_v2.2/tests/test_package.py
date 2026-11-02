import hashlib
import importlib.util
from pathlib import Path
import struct
import unittest

ROOT = Path(__file__).resolve().parents[1]

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

sync = load("rotarydeck_sync_test", ROOT / "companion" / "rotary_deck_sync.py")
patcher = load("rotarydeck_patcher_test", ROOT / "tools" / "apply_reconnect_patch.py")

class PacketTests(unittest.TestCase):
    def test_time_packet(self):
        packet = sync.time_packet(257, 1700000000, -90)
        self.assertEqual(struct.unpack("<BBIh", packet), (1, 1, 1700000000, -90))

    def test_volume_range_and_mute(self):
        for percent in range(101):
            for muted in (False, True):
                self.assertEqual(sync.volume_packet(257, percent, muted), bytes((4, 1, percent, int(muted))))
        self.assertEqual(sync.volume_packet(0, None), bytes((4, 0, 255, 0)))
        for invalid in (-1, 101, 254, 256):
            with self.assertRaises(ValueError):
                sync.volume_packet(0, invalid)

    def test_title_chunking(self):
        for length in (0, 1, 16, 17, 127, 128, 200):
            packets = sync.title_packets(5, "x" * length)
            self.assertTrue(all(4 <= len(packet) <= 20 for packet in packets))
            self.assertEqual(b"".join(p[4:] for p in packets), b"x" * min(length, 128))
            for i, packet in enumerate(packets):
                self.assertEqual(packet[:4], bytes((2, 5, i, len(packets))))
        self.assertEqual(b"".join(p[4:] for p in sync.title_packets(0, "café")), b"cafe")

    def test_state_and_uuid(self):
        self.assertEqual(sync.state_packet(257, 1, 1), bytes((3, 1, 1, 1)))
        core = (ROOT / "firmware" / "RotaryDeck_v2_1" / "DeckCore.h").read_text()
        self.assertIn(str(sync.SERVICE_UUID), core)
        self.assertIn(str(sync.RX_UUID), core)
        self.assertIn("p.data[0]==4 && p.size==4", core)

class PackageTests(unittest.TestCase):
    def test_matching_sketch_folder(self):
        folder = ROOT / "firmware" / "RotaryDeck_v2_1"
        sketch = folder / (folder.name + ".ino")
        self.assertTrue(sketch.is_file())
        for name in ("DeckCore.h", "DisplayUI.h"):
            self.assertTrue((folder / name).is_file())
            self.assertIn('"' + name + '"', sketch.read_text())

    def test_known_header_fingerprints(self):
        expected = {"DeckCore.h": "adb211089196ab0a80d76190d969ac7ddb0c5862", "DisplayUI.h": "970f6dcacda9e33fa757866bfe465aa423208d0b"}
        for filename, value in expected.items():
            data = (ROOT / "firmware" / "RotaryDeck_v2_1" / filename).read_bytes()
            self.assertEqual(hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest(), value)

    def test_reconnect_patcher_refuses_unknown_source(self):
        with self.assertRaises(RuntimeError):
            patcher.transformed("// Different library version\n")

    def test_guarded_function_replacement(self):
        source = "void f(){if(true){int x=0;}}\nvoid g(){}"
        result = patcher.replace_function(source, "void f()", "void f(){int x=1;}")
        self.assertEqual(result, "void f(){int x=1;}\nvoid g(){}")

if __name__ == "__main__":
    unittest.main()
