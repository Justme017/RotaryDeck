# v2.3 release gates

Scope: Windows companion/Control Centre + Seeed Studio XIAO ESP32-S3. nRF52840 and Linux/macOS are deferred and unsupported by this release, not required completed ports. Preserve Arduino-ESP32 2.0.17 and existing BLE backend. Publication and visibility changes require explicit owner approval.

## Repository and implementation
- [x] Owner-uploaded baseline source available under RotaryDeck_v2.2/.
- [ ] Fix all blockers in INTEGRATION_REVIEW.md.
- [ ] Resolve PR conflicts and review the resolved source.
- [ ] Run model/sync/baseline receiver tests and exact-core firmware build; record exact commit and real outputs.
- [ ] Reconcile baseline manifests with v2.3 modified artifacts.

## Windows smoke test - NOT RUN here
- [ ] Record Windows/Python/dependency versions and tested commit.
- [ ] Launch editor; load/import; save/reload; overwrite backup/restore.
- [ ] Reject invalid input; cancel unsaved navigation and action confirmation.
- [ ] Explicitly test harmless HTTPS URL and existing test folder.
- [ ] Confirm unsupported/disconnected firmware never appears Synced.
- [ ] Test clean companion installation and diagnostics locally.

## Physical deck - NOT RUN here
- [ ] Editable slots, measured label rendering and deliberate activation.
- [ ] Durable APPLIED and matching revision/digest/session readback.
- [ ] Interrupted transfers and storage failures retain prior active profile.
- [ ] Power cycles/reconnects retain profile and never replay launch actions.
- [ ] OBS-to-Netflix acceptance without firmware recompilation.

## Hardware and enclosure - measurements required
- [ ] Label exact display PCB and front/back connector orientation.
- [ ] Verify wiring and power/logic levels on actual hardware.
- [ ] Measure PCB width/height/thickness, mounting-hole centres and diameters.
- [ ] Measure encoder shaft/knob, connector height, cable exit and USB clearance.
- [ ] Design/print/fit-test enclosure and write assembly instructions.
- [ ] Capture real photographs/GIFs; no fabricated dimensions or feature evidence.

## Packaging
- [ ] No logs, virtual environments, caches, credentials or private evidence.
- [ ] Editable source, dependencies, licence scope and patch instructions included.
- [ ] Release asset filenames and documentation links match.
- [ ] New artifact checksums verified; historical baseline hashes not misrepresented.
- [ ] Owner explicitly approves release/publication after acceptance.
