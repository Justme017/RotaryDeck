# Changelog

Updated 2026-11-03. Historical sections record archive provenance, not reconstructed original commit dates. Firmware versions and desktop app versions are separate. Items under Unreleased describe committed development source, not a published stable firmware/app release.

## Unreleased — Windows desktop preview / v2.3 development

### Added
- Owner-provided v2.2 firmware, display, Windows companion, guarded reconnect patcher and baseline tests imported into RotaryDeck_v2.2/ on feature/v2.3-control-centre.
- Local six-Apps/six-Actions profile editor with validation, import/save/default restore, unsaved-edit protection and timestamped overwrite backups.
- Explicit confirmed URL/folder PC tests; other profile types are not implemented PC execution in this preview.
- Windows graphical telemetry bridge and single-EXE packaging workflow. The owner reported the earlier basic app launches.
- Unified Companion / Apps & Actions / Tools interface, original dial logo and application icon.
- Desktop candidate 0.3.0-preview: searchable offline Help, Settings/About and GitHub link, saved device selection, tray controls, startup option and duplicate-instance guard.
- Per-user installer definition, startup registration/removal and publisher/version metadata. These builds remain unsigned.
- Disabled Firmware tab explaining that no validated flashable update package is bundled.
- Integration audit documenting digest/readback/staging/session/storage/routing and provenance issues; completion and acceptance remain pending.

### Changed
- Public repository README and midnight/cyan brand assets updated on main. The owner made the repository public; this did not certify a stable product.
- Windows candidate build workflow updated to Node 24 action versions: checkout v5, setup-python v6 and upload-artifact v6.
- Current desktop scope clarified as Windows x64 + XIAO ESP32-S3; nRF52840/Linux/macOS remain future work.

### Status and version references
- Unified UI source: 46290dab81c89886545ad3709c30d0e23792162b.
- Desktop/installer candidate: c133ed901cfc70cd2c8322ef8b02407840a2a9b2.
- Public branding: dd3d28225dbcc72ea02043d2c0ae83855d81221c.
- Build definitions and smoke checks are committed; latest build success, installer/tray/startup runtime and real-device acceptance are not asserted by this changelog.
- Local profiles do not yet configure the deck. USB flashing, trusted code signing and validated end-to-end profile transfer remain unavailable.

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
- The development work was distributed across volume-sync, dashboard/date and reconnect-patch components, later consolidated as source.
- The v2.2 release is published. Its uploaded RotaryDeck_v2.2.2.zip is a renamed v2.2 archive according to the owner, not a separately established v2.2.2 firmware release.
- Baseline source is now committed on the development branch. Original archive provenance and checksums must remain distinct from modified v2.3 files.
- Publication and source consolidation do not constitute a fresh full firmware/Windows/hardware validation.

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

Historical archive classifications originate from the inventory in Justme017/deck-zips- at commit 0049669c3c1d42fce29d30aaebaa0c6befcc6ef5. Historical tags index archives and can point to the same repository commit; tag comparisons do not compare release-attachment ZIP contents. Original development dates are not reconstructed. Check each release's actual publication and assets rather than treating all releases as drafts.
