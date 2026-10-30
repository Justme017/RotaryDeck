# Deck sync implementation plan

Status: pending implementation. Correcting the local editor source does not complete BLE sync. Work only on feature/v2.3-control-centre. Keep main and working v2.2 firmware unchanged. Arduino-ESP32 remains exactly 2.0.17; no BLE-library or backend migration.

## Source prerequisite

Retrieve and inspect the actual working v2.2 firmware and companion from the supplied repository archives. Record sketch/header names, existing UUIDs, security settings, library versions, encoder callbacks, display layout and companion connection ownership. Do not fabricate missing hooks or claim a baseline is reproducible before exact build settings are recorded.

## Implementation order

1. Run syntax checks and the local editor test suite on the committed correction source. Fix failures through separately reviewed changes; record real results.
2. Review SYNC_PROTOCOL.md against the actual source. Finalize frame fields, capability endpoint, UUIDs, bounded sizes and timeouts. Avoid overlapping BLE connections from the editor and telemetry script.
3. Implement a host codec, transaction state machine and fake-transport tests for chunking, failures, timeout, retry, wrong acknowledgements and readback mismatch. No GUI Synced status without an APPLIED acknowledgement plus matching readback.
4. Implement ESP32 staging, strict metadata validation, atomic active-generation selection and recoverable Preferences/NVS persistence. Add an exact 2.0.17 compile guard in the future firmware change. Do not write flash on every chunk or retry.
5. Add labels using measured pixel width and the actual font. Preserve original stored labels; select a supported truncation marker after checking glyph coverage. Do not treat a character count as proof of physical fit.
6. Emit slot activation identifiers from deliberate encoder interactions. Keep URL/folder targets on the PC; resolve against the acknowledged revision. Keep existing HID media controls with exactly one execution path.
7. Integrate GUI sync with the existing connection manager, worker-thread BLE operations and main-thread Tk updates. Add cancellation, explicit unsupported-firmware states and honest pending/failed/acknowledged indicators.

## Acceptance gates

- [ ] Automated codec and state-machine tests pass, including oversize payloads, malformed UTF-8/JSON, duplicate or missing frames and disconnect before commit.
- [ ] Firmware compiles for the actual XIAO ESP32-S3 settings with core exactly 2.0.17 and unchanged BLE dependencies.
- [ ] A failed or interrupted transaction leaves the last valid configuration active.
- [ ] An acknowledged revision survives power-cycle and is read back correctly.
- [ ] Change the SAME Apps slot from OBS to Netflix, acknowledge/read back, observe its changed label and deliberately activate it to open Netflix without recompiling. Restore that same slot afterwards.
- [ ] No actions execute on load, import, sync, boot, retry or reconnect; duplicate activation events execute at most once per live session.
- [ ] Existing encoder navigation, media HID, telemetry, mute/volume, clock persistence and reconnect still work with companion stopped and running.
- [ ] Logs and screenshots are reviewed for private data before sharing.

No release, merge to main, firmware flash, or claim of completed device sync is authorized by this documentation/source correction.
