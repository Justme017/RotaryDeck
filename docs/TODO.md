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

## Immediate

- [ ] Run python -m py_compile model.py app.py test_model.py on the exact committed revision.
- [ ] Run python -m unittest -v test_model.py on the exact committed revision.
- [ ] Record the actual test output in TEST_RESULTS.txt.
- [ ] Repeat the Windows GUI smoke test on this exact revision.
- [ ] Confirm load, save/reload, overwrite backup, invalid-input rejection, unsaved-edit prompt, URL/folder test and disabled Sync.

## Deck sync

- [ ] Inspect actual v2.2 firmware/companion source and record UUIDs, security, connection ownership, encoder and display hooks.
- [ ] Finalize sync frame layout, capability endpoint, payload limits and timeouts.
- [ ] Implement host codec and transaction state machine.
- [ ] Add fake-transport tests for chunking, bad sequence, bad digest, timeout, disconnect, retry and readback mismatch.
- [ ] Implement ESP32 staging and strict metadata validation.
- [ ] Implement atomic active-generation selection and recoverable NVS/Preferences persistence.
- [ ] Return APPLIED only after durable storage and active-state switch.
- [ ] Add revision/digest readback and show Synced only on exact match.

## Dynamic deck

- [ ] Render configured labels using measured pixel width and supported truncation.
- [ ] Emit deliberate slot-activation events.
- [ ] Resolve URL and folder actions on Windows against the acknowledged revision.
- [ ] Prevent duplicate activation events and prevent execution across reconnect.
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
