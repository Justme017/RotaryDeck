# RotaryDeck

A Bluetooth rotary controller with a graphical LCD, encoder-driven menus, media controls, and a Windows PC companion.

## Platform status

| Platform | Status |
|---|---|
| Seeed Studio XIAO ESP32-S3 | Platform for all current v1.0–v2.2 archives |
| nRF52840 | Planned platform for the final version; no supported port or downloadable build yet |

Do not flash the ESP32-S3 archives to an nRF52840 board. The exact nRF52840 board, pinout, BLE implementation and release version remain to be established.

## Features developed in v2.2

- Animated category carousel with centred position dots.
- Media controls, volume adjustment, mute and configurable encoder behaviour.
- Windows companion for time, media information and default-output volume telemetry.
- Dashboard date and saved 12/24-hour clock selection.
- Local BLE Keyboard reconnect patch, reported working on the owner's device.

Features describe the development line; check the contents of each download. An archive's existence is not a claim of full hardware validation. HID commands and PC-to-deck telemetry are separate paths: a working clock does not prove media-key delivery.

## Downloads

Open [Releases](https://github.com/Justme017/RotaryDeck/releases) while signed in to see drafts. Current entries remain drafts until the owner verifies the files and publishes them. This repository currently provides documentation and release packaging; the editable firmware tree has not been imported into main.

| Version | Platform | Archive role |
|---|---|---|
| v1.0 | XIAO ESP32-S3 | Initial archived firmware and optional Windows helper |
| v1.2 | XIAO ESP32-S3 | Modular archived sketch and headers |
| v2.0 | XIAO ESP32-S3 | Historical firmware snapshot |
| v2.1 | XIAO ESP32-S3 | Historical firmware; companion packaged separately |
| v2.2 | XIAO ESP32-S3 | Current development line; verify complete firmware, corrected companion and reconnect patch are included |

Use the manually uploaded firmware ZIPs, not GitHub's automatic Source code archives. The current release tags identify archive entries at the repository setup commit, not reconstructed historical source commits. Dashboard/date and reconnect packages can be incremental patches rather than standalone projects.

## Getting started

1. Choose an archive matching XIAO ESP32-S3 and inspect its README.
2. Follow [installation](docs/INSTALLATION.md), including the local reconnect-library patch where required.
3. Verify and upload the Arduino sketch.
4. For live time/media/volume, install and run the matching Windows companion.

Build context for the supplied ESP32-S3 project: Arduino-ESP32 2.0.17, U8g2, and T-vK ESP32 BLE Keyboard 0.3.0 with the documented local reconnect patch. Confirm requirements for your selected archive. Never copy .venv, logs, secrets or machine-specific Python environments into a distribution.

## Documentation

- [Changelog](CHANGELOG.md)
- [Installation and troubleshooting](docs/INSTALLATION.md)
- [Roadmap](ROADMAP.md)
- [Contributing](CONTRIBUTING.md)
- [Licensing and third-party notices](docs/LICENSING.md)

## Licence

Original work owned by the project maintainer is offered under the [MIT License](LICENSE). Third-party code is not relicensed by this statement. In particular, verify the BLE Keyboard code's provenance and applicable upstream terms before redistributing a combined archive.

## Validation status

The owner reported successful reconnect testing on their device. No claim is made that all historical archives, the consolidated v2.2 package, or an nRF52840 port have passed complete hardware testing.
