<p align="center">
  <img src="assets/branding/rotarydeck-banner.svg" alt="RotaryDeck — Your old printer display deserves a better job." width="100%">
</p>

# RotaryDeck

Repurpose an Ender 3 display into a Bluetooth DIY desktop controller: rotary navigation, animated menus, media controls and live Windows information.

[📦 Firmware downloads](https://github.com/Justme017/RotaryDeck/releases) · [🖥 Windows preview builds](https://github.com/Justme017/RotaryDeck/actions/workflows/windows-companion-exe.yml?query=branch%3Afeature%2Fv2.3-control-centre) · [📖 Build guide](docs/INSTALLATION.md) · [🐛 Report an issue](https://github.com/Justme017/RotaryDeck/issues)

> Public development project, not a fully validated plug-and-play product. Current ESP32 releases require Arduino-ESP32 **exactly 2.0.17**. Do not upgrade the core or change the BLE backend without deliberate migration and validation. [Compatibility policy](docs/COMPATIBILITY.md).

## What it does

- 🎛 Rotary-encoder navigation with animated carousel menus.
- 🎵 Bluetooth HID media controls and firmware-defined shortcuts.
- 🕒 Windows clock, media and output-volume telemetry; dashboard date and saved 12/24-hour setting.
- ♻️ Gives an existing printer display a second life.

## Windows companion preview

The [development branch](https://github.com/Justme017/RotaryDeck/tree/feature/v2.3-control-centre) contains the unified companion, local Apps & Actions editor and guarded utilities. New candidate builds add Help, tray/startup controls and an installer. Build availability and behavior must be checked for the exact downloaded commit.

1. Open [Windows companion EXE builds](https://github.com/Justme017/RotaryDeck/actions/workflows/windows-companion-exe.yml?query=branch%3Afeature%2Fv2.3-control-centre).
2. Select a successful run and download its `RotaryDeckCompanion-Windows-x64-preview` artifact while available. GitHub may require sign-in; artifacts have limited retention.
3. Use the installer if included, or run the companion EXE. Keep your existing working firmware and stop older companion processes first.

Preview binaries are unsigned. Publisher metadata is not a trusted digital signature. Local profile editing does not yet configure the physical deck: deck profile sync and one-click USB firmware updates remain unavailable. Do not treat a successful build as Windows/BLE/hardware acceptance.

## Supported scope

| Component | Current status |
|---|---|
| XIAO ESP32-S3 | Current firmware target; Arduino-ESP32 2.0.17 required |
| Windows x64 | v2.2 telemetry companion; unified graphical app under development |
| Editable Apps & Actions | Local editor; physical-deck profile transfer not enabled in the preview |
| nRF52840 | Future work; do not flash ESP32 images to this board |
| Linux / macOS | Not implemented or supported |

## Source and firmware

- [Published firmware archives](https://github.com/Justme017/RotaryDeck/releases): download the manually attached version ZIP, not automatic Source code archives as a substitute for historical firmware.
- [Committed v2.2 baseline](https://github.com/Justme017/RotaryDeck/tree/feature/v2.3-control-centre/RotaryDeck_v2.2) and [Windows app source](https://github.com/Justme017/RotaryDeck/tree/feature/v2.3-control-centre/windows_app) are on the development branch.
- Historical version tags index release archives and may point to the same commit; GitHub tag comparison does not compare uploaded ZIP contents.
- Archive contents and hardware coverage vary. Verify the exact display PCB, connector orientation, wiring and required patches before another build.

## Roadmap and documentation

Physical-deck profile sync, validated USB firmware updating, enclosure, verified wiring diagrams, real device photos/GIFs and final acceptance testing remain work in progress.

[Installation](docs/INSTALLATION.md) · [Roadmap](ROADMAP.md) · [Changelog](CHANGELOG.md) · [Contributing](CONTRIBUTING.md) · [Release gates](https://github.com/Justme017/RotaryDeck/blob/feature/v2.3-control-centre/docs/LAUNCH_CHECKLIST.md)

## Credits and licence

Created by [Shubham Mehta / Justme017](https://github.com/Justme017). [MIT](LICENSE) applies to original maintainer-owned work and original brand graphics only; [third-party licensing](docs/LICENSING.md) remains separate. Independent project, not affiliated with Creality or Elgato.
