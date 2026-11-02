# Installation

## 1. Requirements
- Your existing XIAO ESP32-S3 + ST7920/Ender display setup.
- Arduino-ESP32 2.0.17 and your known-working XIAO ESP32-S3 board settings.
- U8g2 (use your already working version; this archive does not provide a dependency lock).
- T-vK ESP32 BLE Keyboard 0.3.0 compatible with the uploaded library and optional local reconnect patcher.
- Windows with Python available through the py launcher for companion setup. Requirements install into a new local .venv; do not copy an old environment.

These dependencies are not vendored. Requirements use version ranges, not a reproduced lock of your machine. No pinout or library upgrade should be inferred from this packaging task.

## 2. Reconnect library patch
If your reconnect patch is already installed and controls work after power cycles, do not reinstall the library. The bundled patcher can verify it and report Already installed without changing anything.

For an unpatched compatible installation:
1. Close Arduino IDE and back up the library outside Arduino's libraries folder.
2. Double-click tools/apply_reconnect_patch.bat.
3. Select the installed library's BleKeyboard.cpp (not any file in the sketch).
4. The tool checks the matching header and exact source fingerprint before writing. It backs up the original file and produces the same patched-source fingerprint as the reconnect candidate you tested.
5. If it reports a different library/version, STOP; do not force it. Supply that version for review.
6. Reopen Arduino IDE, Verify, and Upload the sketch. Editing a PC library file alone does not update the ESP32.

No pairing reset is requested. Roll back by restoring the backed-up library file, rebuilding and uploading. The patcher does not resolve upstream licence permissions; do not redistribute upstream code on the strength of this archive's MIT licence.

If Python's file picker is unavailable, run from a terminal:
  py -3 tools/apply_reconnect_patch.py "FULL PATH TO INSTALLED BleKeyboard.cpp"

## 3. Firmware
Open firmware/RotaryDeck_v2_1/RotaryDeck_v2_1.ino. Both headers are already present under their canonical names. Keep this folder/sketch name pairing. Verify, then Upload with your existing board and port settings. Do not enable full-flash erase as part of this update.

Keep your existing wiring. docs/GPIO_REFERENCE.md lists source constants only, not an electrically verified wiring diagram. Never use these ESP32 builds on nRF52840.

## 4. Windows companion
Stop old companion instances. In companion/, run setup_companion.bat as a normal user. It creates a local .venv, installs requirements and runs dependency/audio/paired-device diagnostics. Then run start_companion.bat and leave the window open. Startup logging should progress through paired-device enumeration, service discovery, Sync active and actual volume readings.

For multiple paired decks, run in a terminal from companion/:
  start_companion.bat --list
  start_companion.bat --device-id "EXACT WINDOWS DEVICE ID"

The companion reads default-output endpoint volume, not an individual application's volume. HID controls do not require the sync script for normal basic media commands. App-launch shortcuts may require your existing Windows shortcut helper; no launch helper or GUI is installed by the sync script.

## 5. Verification before replacing your release ZIP
Test all media controls, volume values, time/date, clock-format persistence, all menu entries and three power cycles with the companion stopped and running. Check that Windows actually responds; COMMAND SENT is not an acknowledgement.

Run portable checks using:
  py -3 -m unittest discover -s tests -v

Inspect companion/rotary_deck_sync.log on failure. Review logs before sharing: they may contain device IDs, media titles and personal paths. Do not reset pairing, disable encryption or change dependencies without an error-specific reason.
