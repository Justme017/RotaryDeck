# Release and validation checklist

Updated 2026-11-03. The owner has made the repository public. Public visibility is established, not a claim that all release gates passed. This checklist now governs candidate acceptance and future releases; it does not require changing visibility back.

Scope: Windows x64 + XIAO ESP32-S3, Arduino-ESP32 exactly 2.0.17 and the existing BLE backend. nRF52840, Linux and macOS are deferred, not mandatory completed ports for this preview.

## Available source and documentation

- [x] Public README has original branding, scope, download/source links and limitations.
- [x] v2.2 source and Windows editor/desktop candidate are committed on feature/v2.3-control-centre.
- [x] Local profile UI, tools, Help, installer/tray/startup definitions and build workflow are committed.
- [ ] Verify latest actual EXE/installer build artifacts and record exact tested commit.
- [ ] Resolve integration review findings/branch conflicts before merging implementation.
- [ ] Reconcile modified firmware manifests and original baseline fingerprints.

## Windows desktop acceptance

- [ ] Fresh Windows install/start, uninstall and retained-profile behavior tested.
- [ ] Tray creation, hide/reopen, Start/Stop/Exit and duplicate-instance behavior tested.
- [ ] Startup checkbox/toggle, quoted installed path, login launch and removal tested.
- [ ] Saved device selection and dependency/audio diagnostics tested.
- [ ] Local profile validation/import/save/backups/default restore and unsaved-edit prompts tested.
- [ ] Confirmed URL/folder tests and cancel paths tested with no unintended execution.
- [ ] Unsigned-preview and unavailable-sync/update messages remain honest.

## Firmware and integration acceptance

- [ ] Exact-core clean firmware build with intended dependencies and reconnect patch recorded.
- [ ] Actual firmware/host codec agreement, strict staging and failure-path tests pass.
- [ ] Durable APPLIED plus matching revision/digest/session readback confirmed.
- [ ] Interrupted sync/storage failure retains the previous valid active configuration.
- [ ] Power cycles/reconnects retain state and never replay actions.
- [ ] Configured labels/activation and OBS-to-Netflix end-to-end acceptance pass.
- [ ] USB updater remains disabled until board-specific compiled package/flash layout/integrity checks and real-device recovery testing exist.

## Hardware and packaging

- [ ] Verify exact display PCB, connector orientation, electrical wiring and power arrangement.
- [ ] Complete measurements, enclosure CAD/print fit and assembly instructions.
- [ ] Capture genuine hardware photos/GIFs; no generated images used as evidence.
- [ ] Review public history, build outputs and screenshots for secrets/private logs; deleting current files is not a history purge.
- [ ] Package editable source, dependency/patch instructions, licences and accurate checksums without caches/venvs/private logs.
- [ ] Release names, tags, attachments and descriptions match; no archive-comparison assumptions.
- [ ] Obtain signing identity and test signatures if signing is introduced; publisher metadata alone is not signing.
- [ ] Owner explicitly approves each future stable release/publication. A successful workflow or completed agent session is not that approval.
