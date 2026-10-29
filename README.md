# RotaryDeck

### Your old printer display deserves a better job.

Repurpose an Ender 3 display into a wireless DIY stream deck—with an animated interface, a rotary encoder, media controls, and live information from your PC.

A second life for a printer screen. A new control surface for your desk.

[Get the files](https://github.com/Justme017/RotaryDeck/releases) · [Build guide](docs/INSTALLATION.md) · [Changelog](CHANGELOG.md) · [nRF52840 roadmap](ROADMAP.md)

## From 3D printer to desktop controller

RotaryDeck is a hardware-reuse project built around a repurposed Ender 3 printer display. Instead of treating the screen and encoder as spare parts, it gives them a new role: navigating apps and actions, controlling media, and showing PC-synchronised information.

Rotate to browse. Press to select. Keep the controls on your desk—not buried in another window.

The current prototypes use a Seeed Studio XIAO ESP32-S3. The final hardware direction is nRF52840; that port is planned, not available yet.

## What it does

| Feature | What you get |
|---|---|
| Animated carousel | Category icons that slide into focus with short selection animations |
| Encoder navigation | Browse menus, select actions, and adjust volume |
| Bluetooth media controls | Play/pause, previous/next track, mute, and volume commands |
| App and desktop shortcuts | Firmware-defined keyboard shortcuts; app launching may require host-side configuration |
| Live PC information | Windows companion for time, media information, and default-output volume |
| Clock and date | Dashboard date with a saved 12/24-hour clock option |
| Reconnect patch | Local BLE Keyboard patch reported working after power cycles on the owner's device |

These features describe the v2.2 development line. Check each archive's contents: older versions and incremental patches do not necessarily contain every feature.

## Hardware and platform status

| Component / platform | Status |
|---|---|
| Repurposed Ender 3 display and rotary encoder | Basis of the current build; verify the exact PCB and connector revision |
| Seeed Studio XIAO ESP32-S3 | Platform for all current v1.0–v2.2 archives |
| Windows PC companion | Time, media and volume telemetry for matching firmware |
| nRF52840 | Planned final platform; exact board and port are not yet established |

Display naming alone is not a compatibility guarantee. Verify the actual module, connector pinout, supply voltage and signal levels before wiring; do not assume all Ender 3 or V3 variants share the same display hardware.

Do not flash the ESP32-S3 archives to an nRF52840 board.

## Build your own

1. Choose a [version archive](https://github.com/Justme017/RotaryDeck/releases) for XIAO ESP32-S3.
2. Read the archive's instructions and the [installation guide](docs/INSTALLATION.md).
3. Install the matching Arduino core and libraries, including the reconnect patch where required.
4. Verify and upload the sketch, keeping its folder and .ino names matched.
5. Run the matching Windows companion for live time, media and volume telemetry.

Build context for the supplied ESP32-S3 project: Arduino-ESP32 2.0.17, U8g2, and T-vK ESP32 BLE Keyboard 0.3.0 with the documented local reconnect patch. Confirm dependencies against the selected version.

Bluetooth HID commands and PC-to-deck telemetry are separate paths. A working clock does not prove that Windows is accepting media keys; COMMAND SENT records an attempt, not a PC acknowledgement.

## Downloads and version history

Firmware is currently distributed through manually uploaded release archives. The editable firmware tree has not been imported into main. Draft releases are visible to authorised users and remain unpublished until the owner reviews them.

| Version | Platform | Archive role |
|---|---|---|
| v1.0 | XIAO ESP32-S3 | Initial archived firmware and optional Windows helper |
| v1.2 | XIAO ESP32-S3 | Modular archived sketch and headers |
| v2.0 | XIAO ESP32-S3 | Historical firmware snapshot |
| v2.1 | XIAO ESP32-S3 | Historical firmware; companion packaged separately |
| v2.2 | XIAO ESP32-S3 | Current development line; verify complete firmware, corrected companion and reconnect patch are included |

Use the manually attached firmware ZIPs, not GitHub's automatic Source code archives. The archive tags do not reconstruct historical firmware commits. Dashboard/date headers and reconnect-library files may be incremental patches, not standalone projects.

See [CHANGELOG.md](CHANGELOG.md) for the documented development history.

## Where this is going

The next hardware chapter is nRF52840. The roadmap covers board selection, display/encoder integration, BLE HID and companion-service migration, storage/sleep changes, and device testing. No nRF52840 release or pinout is promised yet.

Follow the [roadmap](ROADMAP.md) for the planned work.

## Help give more hardware a second life

Built one? Share your display's exact PCB revision, photos, build notes, and what you tested. Found a bug? Include the version, board, dependencies and reproduction steps. Contributions that make the build easier to reproduce are welcome.

If this is the kind of hardware reuse you want to see more of, a star helps show your support.

- [Installation and troubleshooting](docs/INSTALLATION.md)
- [Contributing](CONTRIBUTING.md)
- [Licensing and third-party notices](docs/LICENSING.md)

## Licence and project status

Original maintainer-owned work is offered under the [MIT License](LICENSE). Third-party code is not relicensed by this statement; verify the BLE Keyboard source's applicable upstream terms before redistributing combined archives.

Reconnect success is user-reported on the owner's hardware. All historical versions, the consolidated package, and the planned nRF52840 port are not claimed to have passed complete hardware validation.

RotaryDeck is an independent DIY project, not an official Creality or Elgato product.
