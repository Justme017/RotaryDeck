# Project status

## Inspection snapshot
Reviewed PR #1 source at 20b93d5eb82a8cd6bc570b077056d51002cdc946 on 2026-11-02. This is a static review, not fresh firmware compilation or Windows/hardware validation.

## Available
- Local Control Centre editor and host sync implementation exist. Earlier recorded reports list 15 model and 15 sync tests passing; they do not certify the latest firmware integration.
- Owner-uploaded v2.2 firmware, display, companion, patcher and baseline tests are committed under RotaryDeck_v2.2/. Source retrieval is no longer a blocker.
- Candidate firmware configuration/label/event code and Windows transport now exist, but review found blocking incompatibilities; see INTEGRATION_REVIEW.md.
- Runtime companion log is absent from the reviewed PR tree and a scoped ignore rule exists. Historical copies were not purged.

## Blocking before merge or flashing
- Host SHA-256 and firmware simpleDigest are incompatible.
- Firmware rejects readback after COMMIT closes the transaction.
- Editor initially disables Sync and has no reachable startup connection/enabling path.
- Strict metadata validation and atomic runtime/storage activation require fixes.
- Host activation listener/profile binding and shared telemetry connection ownership remain incomplete.
- Baseline fingerprints/manifests conflict with modified firmware files.
- Resolve reported PR merge conflicts, then rerun checks on the resolved commit.

## Validation still pending
Exact-core ESP32 build, Windows GUI and clean install, real BLE/reconnect, interrupted sync, power-loss persistence and deliberate OBS-to-Netflix acceptance. Do not mark any of these passed without execution evidence.

## Guardrails
v2.3 scope is Windows + XIAO ESP32-S3. Keep Arduino-ESP32 exactly 2.0.17, existing Bluedroid/T-vK BLE Keyboard backend and reconnect workaround. No automatic merge, tag/release changes or publication. No action execution during load/import/save/sync/boot/retry/reconnect. Synced requires durable APPLIED and matching revision/digest readback.
