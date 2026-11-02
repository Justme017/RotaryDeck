"""Apply the known RotaryDeck reconnect changes to your locally installed 0.3.0 library.
No upstream library source is bundled. This utility does not establish upstream redistribution permission.
"""
from pathlib import Path
import argparse
import datetime
import hashlib

ORIGINAL = '8b77b98e3813dd163deb84c6a4cd073ef6c0346c'
PATCHED = "6b6d6d5d03f289ad4e1c7c79c89a9d3a75441a05"
HEADER = "4fdeaa5d84bb349a0f57315595d2c27b0864af7e"
ON_CONNECT = 'void BleKeyboard::onConnect(BLEServer* pServer) {\n  // Reset local reports without sending any key presses.\n  memset(&this->_keyReport, 0, sizeof(this->_keyReport));\n  memset(&this->_mediaKeyReport, 0, sizeof(this->_mediaKeyReport));\n#if !defined(USE_NIMBLE)\n  // Bluedroid reconnect compatibility workaround for bonded HID hosts.\n  // Keep the existing HID report map, UUIDs and security configuration.\n  BLE2902* keyboardCccd = (BLE2902*)this->inputKeyboard->getDescriptorByUUID(BLEUUID((uint16_t)0x2902));\n  BLE2902* mediaCccd = (BLE2902*)this->inputMediaKeys->getDescriptorByUUID(BLEUUID((uint16_t)0x2902));\n  if (keyboardCccd) keyboardCccd->setNotifications(true);\n  if (mediaCccd) mediaCccd->setNotifications(true);\n#endif\n  this->connected = true;\n}\n'
ON_DISCONNECT = 'void BleKeyboard::onDisconnect(BLEServer* pServer) {\n  this->connected = false;\n  memset(&this->_keyReport, 0, sizeof(this->_keyReport));\n  memset(&this->_mediaKeyReport, 0, sizeof(this->_mediaKeyReport));\n#if !defined(USE_NIMBLE)\n  BLE2902* keyboardCccd = (BLE2902*)this->inputKeyboard->getDescriptorByUUID(BLEUUID((uint16_t)0x2902));\n  BLE2902* mediaCccd = (BLE2902*)this->inputMediaKeys->getDescriptorByUUID(BLEUUID((uint16_t)0x2902));\n  if (keyboardCccd) keyboardCccd->setNotifications(false);\n  if (mediaCccd) mediaCccd->setNotifications(false);\n  if (advertising) advertising->start();\n#endif\n}\n'
PREFIX = '#include <string.h>\n// RotaryDeck Bluedroid HID reconnect candidate, based on the supplied 0.3.0 source.\n'

def blob_sha(source):
    data = source.encode("utf-8")
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()

def replace_function(source, signature, replacement):
    start = source.index(signature)
    opening = source.index("{", start)
    depth = 0
    for i in range(opening, len(source)):
        if source[i] == "{":
            depth += 1
        elif source[i] == "}":
            depth -= 1
            if depth == 0:
                return source[:start] + replacement + source[i + 1:]
    raise ValueError("Cannot locate end of " + signature)

def transformed(source):
    if blob_sha(source) == PATCHED:
        return source
    if blob_sha(source) != ORIGINAL:
        raise RuntimeError("Different library source/version. No changes made. Do not force this patch; provide your actual library for review.")
    updated = replace_function(source, "void BleKeyboard::onConnect(BLEServer* pServer)", ON_CONNECT)
    updated = replace_function(updated, "void BleKeyboard::onDisconnect(BLEServer* pServer)", ON_DISCONNECT)
    start = updated.index("void BleKeyboard::releaseAll(void)")
    end = updated.index("size_t BleKeyboard::write", start)
    block = updated[start:end]
    if block.count("sendReport(&_keyReport);") != 1:
        raise RuntimeError("Unexpected releaseAll implementation. No changes made.")
    updated = PREFIX + updated[:start] + block.replace("sendReport(&_keyReport);", "sendReport(&_keyReport);\n  sendReport(&_mediaKeyReport);") + updated[end:]
    if blob_sha(updated) != PATCHED:
        raise RuntimeError("Patched source hash mismatch. No changes made.")
    return updated

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", nargs="?", help="Full path to installed BleKeyboard.cpp")
    args = parser.parse_args()
    selected = args.source
    if not selected:
        from tkinter import Tk, filedialog
        root = Tk()
        root.withdraw()
        try:
            selected = filedialog.askopenfilename(title="Select the installed BleKeyboard.cpp", filetypes=[("BleKeyboard.cpp", "BleKeyboard.cpp")])
        finally:
            root.destroy()
    if not selected:
        return
    target = Path(selected).resolve()
    if target.name != "BleKeyboard.cpp":
        raise RuntimeError("Select BleKeyboard.cpp from the installed Arduino library, not the sketch.")
    header = target.with_name("BleKeyboard.h")
    if not header.exists() or blob_sha(header.read_text(encoding="utf-8-sig")) != HEADER:
        raise RuntimeError("Missing or different matching BleKeyboard.h. No changes made.")
    source = target.read_text(encoding="utf-8-sig")
    updated = transformed(source)
    if updated == source:
        print("Known reconnect patch is already installed. No changes made.")
        return
    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    backup = target.with_name(target.name + ".before-rotarydeck-" + stamp + ".bak")
    backup.write_bytes(target.read_bytes())
    temp = target.with_name(target.name + ".rotarydeck.tmp")
    with temp.open("w", encoding="utf-8", newline="\n") as stream:
        stream.write(updated)
    temp.replace(target)
    print("Reconnect patch applied. Backup:", backup.name)
    print("Reopen Arduino IDE, Verify and Upload your sketch. No pairing reset is requested.")

if __name__ == "__main__":
    try:
        main()
    except Exception:
        import traceback
        traceback.print_exc()
        raise SystemExit(1)
