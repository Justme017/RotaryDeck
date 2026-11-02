# Project status

## Done

- [x] v2.2 firmware and Windows companion remain the known-good baseline.
- [x] Arduino-ESP32 core is pinned to exactly 2.0.17 for current ESP32 releases.
- [x] v2.3 development branch exists.
- [x] Profile schema, validation rules, action catalogue, display-label rules, backup policy, validation checklist, hardware-evidence checklist and OBS-to-Netflix acceptance test are documented.
- [x] Local Control Centre source is committed: six Apps and six Actions, profile load/import, validation, local save/load, timestamped backups, unsaved-edit protection, and explicit URL/folder PC tests.
- [x] Deck-sync protocol and implementation plan are drafted.
- [x] The prior Windows Control Centre equivalent was manually smoke-tested by the owner.
- [x] Exact source snapshot e0b52ae passes Python syntax compilation and all 15 automated model tests in a headless environment; see control_centre/TEST_RESULTS.txt.

## In progress

- [ ] Perform a fresh Windows GUI smoke test on this exact source revision.
- [ ] Implement the host-side sync transaction codec and state machine.
- [ ] Implement ESP32 configuration staging, validation, NVS/Preferences persistence, acknowledgement and readback.

## Next

- [ ] Render synced labels with measured display-font width and supported truncation.
- [ ] Emit deliberate slot-activation events for URL and folder actions.
- [ ] Resolve actions on the Windows companion against the acknowledged profile revision.
- [ ] Run the OBS-to-Netflix end-to-end acceptance test.
- [ ] Complete enclosure, verified wiring evidence, screen photos/GIFs and concise user documentation.

## Guardrails

- Keep main as the known-working v2.2 baseline.
- Keep Arduino-ESP32 at exactly 2.0.17 during v2.3.
- Do not replace or migrate the BLE library/backend during this work.
- Do not mix nRF52840 work into the ESP32 v2.3 release.
- Do not mark a profile Synced without an APPLIED acknowledgement and matching revision/digest readback.
- Do not execute actions on load, import, sync, boot, retry or reconnect.
