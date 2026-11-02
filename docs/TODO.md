# RotaryDeck updated to-do list

## Completed

- [x] Create feature/v2.3-control-centre from main.
- [x] Pin current ESP32 releases to Arduino-ESP32 exactly 2.0.17.
- [x] Document compatibility policy, v2.2 baseline and validation checklist.
- [x] Define profile schema, action catalogue, display-label rules and backup policy.
- [x] Define OBS-to-Netflix acceptance test and hardware-evidence checklist.
- [x] Build local Control Centre editor for six Apps and six Actions.
- [x] Implement profile load/import, validation, save, save-as, restore and unsaved-edit protection.
- [x] Implement timestamped backups with ten retained per filename.
- [x] Implement explicit URL and folder Test on PC actions.
- [x] Keep Sync to deck disabled and prevent false synced status.
- [x] Draft deck-sync protocol and implementation plan.
- [x] Replace all earlier placeholder commits with actual source and documents.
- [x] Manually smoke-test the prior equivalent Windows Control Centre build.
- [x] Run py_compile on the exact e0b52ae source snapshot: passed for model.py, app.py and test_model.py.
- [x] Run the 15-test unittest suite on the exact e0b52ae source snapshot: passed.
- [x] Record actual automated test output in control_centre/TEST_RESULTS.txt.

## Immediate

- [ ] Repeat the Windows GUI smoke test on this exact revision.
- [ ] Confirm load, save/reload, overwrite backup, invalid-input rejection, unsaved-edit prompt, URL/folder test and disabled Sync.

## Deck sync

- [ ] Inspect actual v2.2 firmware/companion source and record UUIDs, security, connection ownership, encoder and display hooks (blocked until the v2.2.2 release ZIP can be downloaded in this environment).
- [x] Finalize host-side sync frame layout, capability endpoint handling, payload limits and timeout/retry behaviour.
- [x] Implement host codec and transaction state machine.
- [x] Add fake-transport tests for chunking, bad sequence, bad digest, timeout, disconnect, retry and readback mismatch.
- [ ] Implement ESP32 staging and strict metadata validation.
- [ ] Implement atomic active-generation selection and recoverable NVS/Preferences persistence.
- [ ] Return APPLIED only after durable storage and active-state switch.
- [x] Add revision/digest readback and show Synced only on exact match.

## Dynamic deck

- [ ] Render configured labels using measured pixel width and supported truncation.
- [ ] Emit deliberate slot-activation events.
- [ ] Resolve URL and folder actions on Windows against the acknowledged revision.
- [x] Prevent duplicate activation events and execution across reconnect in host routing logic.
- [ ] Keep existing HID media controls with exactly one execution path.
- [ ] Pass the OBS-to-Netflix end-to-end acceptance test without recompiling firmware.

## Hardware and release

- [ ] Verify exact display PCB and connector orientation.
- [ ] Produce verified XIAO ESP32-S3 wiring documentation.
- [ ] Design, print and fit-test the enclosure.
- [ ] Capture real screen photos/GIFs and assembly photos.
- [ ] Update installation and user documentation for v2.3.
- [ ] Update changelog and create a manually uploaded release ZIP only after all acceptance gates pass.
- [ ] Review logs and screenshots for private data before sharing.
