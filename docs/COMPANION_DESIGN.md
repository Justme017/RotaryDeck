# Companion — preview implementation and remaining design

Updated 2026-11-03. This is no longer a design-only project. The local editor and Windows desktop candidate are committed on [feature/v2.3-control-centre](https://github.com/Justme017/RotaryDeck/tree/feature/v2.3-control-centre). Main holds public documentation; it does not imply that development code is merged or validated.

## Current desktop candidate

- Companion: Start/Stop around existing v2.2 Windows clock/media/default-output volume telemetry.
- Apps & Actions: six slots each; local JSON profiles, label/type/target validation, save/import/default restore, overwrite backups and unsaved-edit protection.
- Test on PC: confirmed URLs/folders only. open_app, run_shortcut and built-in profile entries are not arbitrary working PC execution in this build.
- Tools: dependency/audio diagnostics and the existing fingerprint-guarded reconnect-library patcher, with confirmation and backup.
- Help: searchable offline usage, FAQs, safety and limitations.
- Desktop integration: tray controls, close-to-tray notice, startup setting, stored device selection, duplicate-instance guard, per-user installer and GitHub/About metadata.
- Firmware tab: explicitly disabled until a verified flashable package exists.

Source implementation is not the same as a tested installer, successful Bluetooth connection or complete deck integration. Latest desktop candidate source: c133ed901cfc70cd2c8322ef8b02407840a2a9b2. Firmware v2.2/v2.3 is separate from companion 0.3.0-preview.

## Still-required user outcome

Replace an OBS slot with NETFLIX, intentionally test the website, apply the profile with durable device acknowledgement/readback, see the new label on the deck and activate it exactly once without recompiling firmware. Only the local editing/testing portion is available in the preview; physical-deck profile sync remains unavailable.

## Integration contract to complete

1. Capability negotiation and bounded versioned transfer.
2. Identical standard digest computation in host and actual firmware, not merely a compatible Python fake receiver.
3. Strict isolated candidate validation; no mutation of active mappings before durable commit.
4. Recoverable storage generation selection and matching APPLIED/revision/digest/session readback.
5. One coordinated Windows connection owner for telemetry, config responses and activation events.
6. Live-session activation binding, stale/duplicate rejection and disconnect invalidation.
7. Measured display widths and explicit configured built-in semantics, with no unsafe legacy fallback.

The companion keeps PC paths/URLs on the host and resolves only approved local mappings; the deck receives bounded labels/identities. Existing telemetry UUIDs/types and working HID/reconnect behavior must remain compatible. No shell scripts or arbitrary command text execution is authorised.

## Safety and acceptance

Never execute actions during load/import/save/sync/boot/retry/reconnect. Synced requires durable APPLIED and matching readback, not GATT write success. Confirm sensitive PC tests and exact patch targets. USB updating must use verified board-specific images/settings and never a guessed offset. Publisher text is not code signing.

Required evidence: model/sync tests, actual firmware receiver integration, exact Arduino-ESP32 2.0.17 build, clean Windows install, tray/startup/uninstall tests, real BLE reconnect, interrupted transfers, power-loss persistence and OBS-to-Netflix acceptance. Existing reports apply to their recorded revision, not automatically to later edits. Linux/macOS/nRF52840 remain deferred.
