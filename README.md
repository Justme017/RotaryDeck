# RotaryDeck

An ESP32-S3 Bluetooth rotary controller with an ST7920 128x64 LCD, encoder navigation, media controls, and a Windows PC companion.

## Current project

The v2.2 work includes an animated category carousel, centred position dots, media controls, PC-synchronised time and media information, actual Windows output-volume telemetry, a saved 12/24-hour clock option, and a dashboard date display. The BLE keyboard reconnect patch was reported working on the owner's device; this is not a claim of broad hardware validation.

## Downloads and version archives

Open [Releases](https://github.com/Justme017/RotaryDeck/releases). The repository owner will attach the version ZIPs manually. Draft releases are placeholders until files and notes are reviewed. No firmware is included in this initial repository setup.

| Draft | Intended upload |
|---|---|
| v1.0 | RotaryDeck_v1_complete.zip |
| v1.2 | RotaryDeck_v1_2_modular.zip |
| v2.0 | RotaryDeck_v2_0.zip |
| v2.1 | RotaryDeck_v2_1_firmware.zip and the compatible PC companion |
| v2.2 | Latest working firmware, corrected PC companion, and reconnect patch |

The dashboard/date ZIP contains replacement headers, not a complete standalone project. The reconnect ZIP modifies the installed BLE Keyboard library, not the sketch folder. For v2.2, upload the complete working set or clearly document how its component archives combine. Exclude .venv, caches, logs and credentials.

These archive releases do not reconstruct historical Git commits. Tags created by the setup workflow target the setup commit; GitHub's automatic source-code archives are NOT substitutes for the manually uploaded firmware ZIPs.

## Upload files

1. Open Releases after the setup workflow finishes.
2. Edit the appropriate draft and attach its ZIP files.
3. Review the version, contents, installation notes, dependency versions and test status.
4. Publish only when the draft is complete. Keep unverified builds marked as pre-releases where appropriate.

Latest editable source can also be added using Add file > Upload files on the repository Code page. Keep the Arduino sketch folder name matched to its .ino filename.

## Build context

The supplied project targets Seeed XIAO ESP32-S3, Arduino-ESP32 2.0.17, U8g2, and T-vK ESP32 BLE Keyboard 0.3.0 with the local reconnect patch. Confirm dependencies against the selected version before compiling. The Windows companion has its own requirements.txt and is separate from the Bluetooth HID controls.

## Licensing

A licence for the original project has not yet been selected. Third-party library code remains subject to its upstream licence; retain and verify its notices before redistribution.

## Setup workflow

The Create draft archive releases workflow runs when first added and can also be run manually from Actions. It creates only missing drafts and does not publish releases, upload assets, or change firmware. If Actions is disabled or permissions block it, inspect the workflow error; no releases should be assumed created until verified.
