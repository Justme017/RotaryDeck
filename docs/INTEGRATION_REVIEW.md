# Static integration review

Reviewed PR #1 at 20b93d5eb82a8cd6bc570b077056d51002cdc946, 2026-11-02. Not an executable test report.

## Merge blockers
1. Digest mismatch: control_centre/deck_sync.py prepare_payload computes SHA-256; firmware DeckCore.h simpleDigest computes a custom accumulator. Valid host payloads fail BAD_DIGEST. Use matching standard SHA-256 and cross-language test vectors.
2. Readback unreachable after success: COMMIT sets txOpen_=false, while processConfigFrame rejects non-open transactions before handling READBACK_REQUEST. Permit authenticated active-state readback outside an open staging transaction and test COMMIT then readback.
3. Unreachable GUI connection: sync_transport starts None, refresh_sync_state disables the Sync button, and _try_open_transport is only reached through the disabled button's handler. Add an accessible connection/discovery path and test initial startup.
4. Unsafe staging activation: parseProfileMetadata mutates live labels/modes before storage succeeds; malformed metadata or failed persistence can alter runtime state. Parse strictly into a separate candidate with exact fields, unique six slots per group, correct escaped-string handling and bounded types; publish only after durable verified commit.
5. Storage selector ordering: saveActiveProfile attempts putUChar(active,next) even if prior writes failed because each call is evaluated before &&ok. Only switch after all writes and readback validation succeed; retain/recover previous valid generation.
6. Missing live action pipeline: ActivationRouter exists but the editor/transport does not bind a successful profile and continuously dispatch validated activation events. Telemetry companion remains separate. Complete single-owner routing, disconnect invalidation and non-replayed execution.
7. Session disagreement: host generates lowercase hexadecimal session IDs; firmware constructs uppercase IDs and does not return a confirmed session in APPLIED/readback. Establish and verify a single explicit live session identity; never infer missing session confirmation.
8. Built-in semantics lost: device projection omits builtin_action and firmware falls back to fixed per-slot HID behavior. Map configured built-ins explicitly or reject unsupported changes; unknown/unsupported modes must not silently trigger legacy shortcuts.
9. Evidence/provenance: modified headers no longer match baseline fingerprint tests/manifests. Keep baseline provenance separate from v2.3 artifact checksums and run current tests, including actual firmware receiver integration. Existing fake transport uses its own compatible SHA-256 behavior and cannot catch firmware mismatch.

## Other issues to test/fix
- Firmware notification descriptor/subscription and encryption behavior on actual Bluedroid stack.
- Unbounded host fragment assembly and asynchronous event/response demultiplexing.
- Tk callbacks capture exception variable exc in delayed lambdas; capture an immutable message before the except scope ends.
- Full firmware compilation, including unsigned long(...) casts and min<T> use under exact core headers.

## Verification limits
GitHub check-runs lookup showed one successful GitGuardian check, not firmware/GUI functional CI. Log deletion is confirmed only in the reviewed current tree. No Windows test, physical measurements, firmware compile or conflict resolution was performed by this review.
