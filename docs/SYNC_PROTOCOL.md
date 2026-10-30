# Deck sync protocol: proposed v1

Status: design only. This document does not enable BLE sync. UUIDs, negotiated payload sizes and firmware hooks must be resolved from the actual working v2.2 source before implementation. Preserve Arduino-ESP32 exactly 2.0.17, existing encryption, HID, telemetry and reconnect behaviour.

## Responsibilities

The Windows companion owns executable targets and the full validated profile. The deck receives display metadata, stable group/slot identifiers, supported action classifications and a configuration revision. A URL, folder path or command is not executed by the ESP32. On a deliberate slot activation the deck emits an identifier; the paired companion resolves it against the acknowledged profile revision. Media actions must not fire both as HID and companion commands. Unsupported action types remain disabled.

## Capability negotiation

Read capabilities before enabling sync: protocol version, configuration schema version, maximum total configuration bytes, maximum frame payload, supported action types and active revision. Older v2.2 firmware with no capability endpoint remains explicitly unsupported for sync. Do not invent endpoint UUIDs or repurpose telemetry blindly. Only one companion should own the connection; integrate with the existing connection manager.

## Transaction

1. Validate the full local profile, then derive a device-safe metadata payload. Canonical bytes use UTF-8 JSON, sorted keys and compact separators. SHA-256 identifies these exact bytes.
2. BEGIN carries protocol version, transaction ID, new revision, total byte length and digest. Receiver accepts only within negotiated bounds.
3. DATA carries transaction ID, zero-based sequence and bounded binary payload. Frames must fit the negotiated transport write size including headers. Reject missing, duplicate or out-of-order frames; do not append data from another transaction.
4. COMMIT requests validation of complete byte length, digest, metadata schema, six Apps and six Actions, unique slot IDs and label bounds. Stage changes away from the active configuration.
5. Persist a validated generation with rollback protection. Only after durable storage and active-state switching succeeds, return APPLIED with matching transaction ID, revision and digest.
6. Read back active revision and digest. The companion may show Synced only when both match the intended device payload. A transport write response alone is not an application acknowledgement.

Use a bounded transaction timeout and discard staging on disconnect, timeout or ABORT. Keep the previous active generation on parse, digest, storage or validation failure. A retry with an already-applied revision/digest returns the current state without repeated writes; revision conflicts return an error. SHA-256 is integrity checking, not authentication; preserve authenticated/encrypted transport and never downgrade pairing to make sync work.

## Activation events

An event includes session identifier, monotonic event sequence, active revision, group and slot. Accept only from the paired authenticated device on the current live session, for the matching locally approved revision and an enabled action. Deduplicate events. Never replay old events or queue application launches across reconnect. Load, import, sync, boot and reconnect must never generate execution. Initially allow URL/folder activation only after an explicit user opt-in for the paired device.

## Errors and privacy

Use explicit codes such as UNSUPPORTED_PROTOCOL, TOO_LARGE, BAD_SEQUENCE, BAD_DIGEST, BAD_SCHEMA, STORAGE_FAILED, REVISION_CONFLICT and TIMEOUT. Report useful errors without dumping targets, usernames, media titles or keys. Exact frame layout, UUID assignments, maximum bytes and timeout values remain pending source inspection and hardware validation; this proposal is not a finalized wire contract.
