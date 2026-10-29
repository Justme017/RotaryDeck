# Changelog

This records archive provenance and changes established during development. Original development dates and historical Git commits have not been reconstructed. All listed archives target XIAO ESP32-S3.

## Unreleased — nRF52840 roadmap

- Planned migration of the final version to nRF52840.
- Exact board, pin mapping, firmware architecture and release version are not yet defined.
- No supported nRF52840 build is available.

## v2.2 — ESP32-S3 development line

### Added
- Animated carousel with category-specific pixel animations and centred position dots.
- Windows default-output volume/mute telemetry and matching firmware packet receiver.
- Saved 12/24-hour clock setting and dashboard date display.

### Changed
- Improved menu spacing, selection alignment and Media labels.
- Solid volume/mute speaker shapes.

### Fixed
- Python/WinRT paired-device enumeration overload selection.
- Named GATT overloads for service discovery, characteristic discovery and packet writes.
- BLE Keyboard reconnect candidate restores local notification flags and clears stale report state; releaseAll also sends media release. Reconnect success is user-reported on the owner's hardware.

### Packaging status
- The development work was distributed across a volume-sync package, dashboard/date replacement headers and a reconnect-library patch.
- Verify the final uploaded ZIP includes or documents all required components.
- No newly composed package is declared hardware-verified solely by these notes.

## v2.1 — historical ESP32-S3 snapshot

- Archived RotaryDeck_v2_1 sketch with DeckCore.h and DisplayUI.h.
- Separate PC time/media companion package exists.
- The archive inventory identified a backup header; do not mistake a .bak file for active firmware.
- No additional feature delta or test status is inferred from the version number.

## v2.0 — historical ESP32-S3 snapshot

- Archived RotaryDeck_v2_0 sketch and headers.
- Original archive uses nested folders; preserve the Arduino sketch/folder name when opening it.
- Feature differences and hardware test coverage are not asserted without a source comparison.

## v1.2 — historical ESP32-S3 snapshot

- Modular RotaryDeck_v1_2 sketch with DeckCore.h and DisplayUI.h.
- No machine-readable dependency manifest was present in the inspected archive.

## v1.0 — initial archived ESP32-S3 snapshot

- RotaryDeck_v1 sketch, DeckFirmware.h and optional WindowsApps.ahk helper.
- Historical archive retained for reference; no blanket testing claim.

## Provenance

Archive classifications come from the inventory prepared in Justme017/deck-zips- at commit 0049669c3c1d42fce29d30aaebaa0c6befcc6ef5. These notes are not a reconstruction of original release dates. Current GitHub drafts remain unpublished until reviewed by the owner.
