# RotaryDeck roadmap

Updated 2026-11-03. RotaryDeck is public and under active development. Public visibility is not a stable-release or hardware-validation claim. The current supported development scope is Windows x64 + XIAO ESP32-S3, with Arduino-ESP32 exactly 2.0.17 and the existing BLE backend.

## How to read status

Checked means the stated source/documentation task is committed, not that every runtime scenario is validated. Working firmware archives, development source, successful build artifacts and real-device acceptance are different evidence levels. Firmware v2.2/v2.3 and companion 0.3.0-preview use separate version numbers.

## 1. Repository and source

- [x] Publish repository with an accurate README, original logo/banner and source/download links.
- [x] Import owner-provided v2.2 firmware, companion, patcher and tests into RotaryDeck_v2.2/ on feature/v2.3-control-centre.
- [x] Record compatibility and third-party licensing boundaries.
- [ ] Reconcile modified firmware with original baseline fingerprints/manifests before new packaging.
- [ ] Review source and resolve integration-branch conflicts before merging implementation.
- [ ] Audit public history/artifacts for sensitive logs; current-tree deletion alone does not purge history.

## 2. Windows companion — implemented preview source

Source: [development branch](https://github.com/Justme017/RotaryDeck/tree/feature/v2.3-control-centre/windows_app). Latest desktop candidate commit: c133ed901cfc70cd2c8322ef8b02407840a2a9b2.

- [x] Graphical Start/Stop wrapper for v2.2 clock/media/output-volume telemetry.
- [x] Combine Companion, local Apps & Actions editor and guarded Tools in one EXE build.
- [x] Local six-Apps/six-Actions profiles, validation, import/save/default restore and overwrite backups.
- [x] Explicit confirmed URL/folder Test on PC. Other listed action types are not working arbitrary PC execution.
- [x] Midnight/cyan theme, dial logo/icon and searchable offline Help/FAQ.
- [x] GitHub/About, publisher/version metadata and explicit unsigned-preview status.
- [x] Tray Open/Start/Stop/Exit, close-to-tray, saved device selection and duplicate-instance guard.
- [x] Per-user installer/startup checkbox and app startup toggle; uninstall removes the startup entry.
- [x] Windows build workflow with Node 24 action versions and source/packaged startup checks configured.
- [ ] Verify newest EXE and installer build outputs for their exact commit.
- [ ] Test installer/uninstall, startup after login, tray lifecycle and clean-machine dependencies on Windows.

The owner reported that an earlier basic EXE launches. That does not certify the newer installer/tray build or end-to-end deck configuration.

## 3. Matched firmware/profile integration — unfinished

- [ ] Resolve protocol/digest/readback, GUI connection, session, strict staging, persistence and action-routing review findings.
- [ ] Complete and test one connection owner for telemetry, configuration and activation events.
- [ ] Activate bounded device labels/configuration only after durable storage; confirm APPLIED plus matching revision/digest/session readback.
- [ ] Implement configured built-ins deliberately and reject unsupported mappings without legacy fallbacks.
- [ ] Verify measured display-label widths and deliberate slot activation, without replay after boot/reconnect.
- [ ] Pass OBS-to-Netflix acceptance without recompiling firmware.

Local profile editing does not currently update the physical deck. Preview Sync remains unavailable.

## 4. USB firmware updating and trust

- [x] Add a clearly disabled Firmware tab explaining the missing validated update package.
- [ ] Build and validate a flashable XIAO ESP32-S3 package, correct addresses/settings and integrity metadata.
- [ ] Implement USB target selection, compatibility checks, explicit confirmation, progress, verification and recovery guidance.
- [ ] Test update interruption and settings behavior on the real board; do not promise settings preservation prematurely.
- [ ] Obtain a trusted code-signing identity and sign EXE/installer if available. Publisher text is metadata, not signing or guaranteed SmartScreen reputation.

## 5. Hardware, enclosure and evidence

- [ ] Verify exact display PCB, connector orientation and electrical wiring.
- [ ] Measure PCB, mounting holes, encoder and cable/USB clearances.
- [ ] Design, print and fit-test enclosure; publish editable CAD and assembly instructions.
- [ ] Capture genuine device photos/GIFs and supported-platform acceptance evidence.

## 6. Future platforms — deferred

- [ ] Select exact nRF52840 board/core/backend, then port and independently validate it.
- [ ] Implement/test Linux and macOS backends and permissions before claiming support.

Neither is required for the current ESP32-S3/Windows preview. Do not flash ESP32 firmware onto nRF52840.

## Release gate

Use [LAUNCH_CHECKLIST.md](docs/LAUNCH_CHECKLIST.md). Do not equate a public repository, completed agent session, security check or successful build with complete functional validation. No automatic release, code merge, BLE migration or dependency/core upgrade is implied. No Copilot work is requested.
