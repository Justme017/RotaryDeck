# RotaryDeck

### Your old printer display deserves a better job.

Repurpose an Ender 3 display into a wireless DIY stream deck: animated menus, a rotary encoder, media controls, and live PC information.

> REQUIRED: Arduino-ESP32 board package 2.0.17 exactly. Do not upgrade the ESP32 core for current releases. Other core versions are unsupported until the BLE implementation is deliberately migrated and validated. See [compatibility policy](docs/COMPATIBILITY.md).

Private work in progress. No public launch until the [launch checklist](docs/LAUNCH_CHECKLIST.md) is reviewed and completed.

## Current prototype

- Animated carousel and encoder navigation.
- Bluetooth media controls and firmware-defined shortcuts.
- Windows time, media and output-volume sync.
- Dashboard date and saved 12/24-hour clock setting.
- Reconnect patch reported working on the owner's device.

| Platform | Status |
|---|---|
| XIAO ESP32-S3 | Current v1.0–v2.2 archives; Arduino-ESP32 2.0.17 required |
| nRF52840 | Planned final hardware; port and exact board pending |
| Windows | Existing sync script; graphical configuration app pending |
| Linux / macOS | Not implemented or supported yet |

## Next

Editable Apps and Actions from the companion, including replacing a slot such as OBS with Netflix—without recompiling firmware. This is planned, not available in the current archives.

Also pending: enclosure, verified wiring diagrams for both boards, real screen photos/GIFs, and final validation. Verify the exact display PCB; Ender 3/V3 naming does not guarantee pin compatibility.

[Build guide](docs/INSTALLATION.md) · [Downloads](https://github.com/Justme017/RotaryDeck/releases) · [Changelog](CHANGELOG.md)

[Roadmap](ROADMAP.md) · [Companion design](docs/COMPANION_DESIGN.md) · [Contributing](CONTRIBUTING.md)

Use manually uploaded firmware ZIPs, not automatic Source code archives. Editable firmware is not yet imported into main; archive contents and test coverage vary. Do not flash ESP32 builds to nRF52840.

[MIT](LICENSE) covers original maintainer-owned work only; see [third-party licensing](docs/LICENSING.md). Independent project, not affiliated with Creality or Elgato.
