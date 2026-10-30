# Installation and troubleshooting

## Mandatory ESP32 core version

Install the esp32 board package by Espressif Systems at version 2.0.17 exactly. This is the Arduino-ESP32 board-support package, not the Arduino IDE version, firmware version or microcontroller model.

Current ESP32 releases support only 2.0.17. Do not choose latest, another 2.x version, or 3.x. Other versions are unsupported until the project intentionally upgrades and validates the BLE implementation. Creating or adopting a replacement BLE library alone does not establish compatibility; validation and an explicit support-policy update are required.

Select 2.0.17 in Arduino IDE's Boards Manager and check the installed version before compiling. Do not upgrade the core or switch BLE backends as a generic troubleshooting step. See [COMPATIBILITY.md](COMPATIBILITY.md).

## Supported archive platform

All current version archives are for Seeed Studio XIAO ESP32-S3. nRF52840 is a future target, not a supported board in these downloads. Its eventual board/core requirements will be documented separately.

## Firmware

1. Back up your working sketch and library files.
2. Download the manually attached version ZIP from Releases and extract it.
3. Open the .ino from its matching folder. Do not rename only the sketch or only the folder.
4. Confirm Arduino-ESP32 is exactly 2.0.17. Use U8g2 and the matching BLE Keyboard dependencies; the current v2.2 setup uses T-vK ESP32 BLE Keyboard 0.3.0 with the local reconnect patch.
5. If your release includes replacement DeckCore.h/DisplayUI.h headers, put them into the sketch folder.
6. If it includes the BLE reconnect patch, apply it to the installed BLE Keyboard library, NOT the sketch folder. Back up that library outside Arduino's libraries directory to avoid duplicate copies. A fingerprint-checked patcher must not be forced onto an unfamiliar library version.
7. Verify, then upload with your known-working board and port settings.

No universal connector pinout is provided here. Verify electrical connections against the actual board and selected source.

## Windows companion

Use the companion supplied for the selected firmware. Stop older instances first. If included, run setup_companion.bat as a normal user; it creates a fresh local environment and installs requirements.txt. Then run start_companion.bat and leave its window open. Otherwise follow the archive's instructions.

The latest companion uses Windows Runtime APIs and Pycaw for default-output volume. Its environment must be installed locally; do not distribute .venv.

## Acceptance checks

- Confirm the installed Arduino-ESP32 core is 2.0.17.
- Volume, mute, track and play/pause controls affect the PC.
- PC time/media/volume telemetry arrives independently of HID commands.
- Reconnection works after power cycles with the companion stopped and running.
- Clock-format preference survives reboot.
- Display menus, date, carousel and configured back gesture work.

## Troubleshooting

- Check core 2.0.17 and the intended library folder before investigating compilation or BLE regressions.
- COMMAND SENT only indicates a send attempt; verify that the PC responds.
- Connected Bluetooth does not itself prove HID input is ready.
- Missing telemetry: keep the companion window open and inspect its error/log.
- Invalid parameter count: ensure the companion contains the enumeration and named GATT overload fixes.
- Unknown volume is not zero volume; estimates should remain explicitly labelled.
- Do not erase flash, disable encryption, or repeatedly re-pair as a generic fix. Record the actual error first.

Review logs before sharing: device IDs, media titles, usernames and local paths may be present.
