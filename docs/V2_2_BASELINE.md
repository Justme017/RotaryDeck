# v2.2 known-good baseline

This documents the current working configuration. Do not change these versions while developing v2.3.

## Firmware

| Item | Requirement |
|---|---|
| Board | Seeed Studio XIAO ESP32-S3 |
| Arduino-ESP32 board package | Exactly 2.0.17 |
| Display library | U8g2 |
| BLE Keyboard library | T-vK ESP32 BLE Keyboard 0.3.0 |
| BLE reconnect patch | Apply to the installed BLE Keyboard library, not the sketch folder |
| BLE backend | Existing Bluedroid-based setup |

## Build rules

- Use the manually uploaded release ZIP, not an automatic GitHub source-code archive.
- Open the `.ino` from its matching folder.
- Do not rename only the sketch or only its folder.
- Do not upgrade the ESP32 core as a troubleshooting step.
- Do not switch BLE backends or replace the BLE Keyboard library during v2.3.

## Known-working behaviour

- Animated carousel and encoder navigation.
- Bluetooth media controls and firmware-defined shortcuts.
- Windows time, media, and output-volume telemetry.
- Dashboard date and saved 12/24-hour clock preference.
- Reconnect behaviour reported working on the owner’s device.

## Change policy

Any change to the core, BLE library, BLE backend, or board target requires a separate migration branch, validation, and an explicit compatibility-policy update.
