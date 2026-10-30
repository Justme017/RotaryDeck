# Validation checklist

Run this checklist before merging v2.3 changes or creating a release.

## Build baseline

- [ ] Arduino-ESP32 board package is exactly 2.0.17.
- [ ] Board is Seeed Studio XIAO ESP32-S3.
- [ ] U8g2 and the documented BLE Keyboard dependency are installed.
- [ ] The BLE reconnect patch is applied to the intended installed library folder.
- [ ] Firmware compiles without changing the core version or BLE backend.

## Existing v2.2 behaviour

- [ ] Display menus, date, carousel, and configured back gesture work.
- [ ] Encoder navigation is responsive.
- [ ] Volume, mute, track, and play/pause controls affect the PC.
- [ ] PC time, media, and output-volume telemetry arrive independently of HID commands.
- [ ] Reconnection works after a power cycle with the companion stopped.
- [ ] Reconnection works after a power cycle with the companion running.
- [ ] Clock-format preference survives reboot.

## v2.3 profile editing

- [ ] A profile loads without errors.
- [ ] Invalid JSON produces a clear, actionable error.
- [ ] Duplicate slot numbers are rejected.
- [ ] Empty labels are rejected.
- [ ] Unsupported action types are rejected.
- [ ] Invalid URLs are rejected.
- [ ] Missing targets for non-builtin actions are rejected.
- [ ] Profile save creates a valid JSON file.
- [ ] Profile reload preserves all six app and six action slots.

## PC-side action testing

- [ ] Test on PC runs only after an explicit button press.
- [ ] Open-application actions launch the intended target.
- [ ] URL actions open the intended website.
- [ ] Folder actions open the intended folder.
- [ ] Built-in actions perform their documented behaviour.
- [ ] Failed actions show a useful error instead of pretending to succeed.

## Future device sync

- [ ] Sync remains explicitly unavailable until firmware acknowledgement exists.
- [ ] A sync attempt shows an honest status and does not mark the profile as synced.
- [ ] Firmware acknowledges valid configurations.
- [ ] Firmware rejects invalid configurations with a useful error.
- [ ] OBS can be replaced by Netflix without recompiling firmware.
- [ ] A power-cycle reconnect preserves the intended configuration behaviour.
