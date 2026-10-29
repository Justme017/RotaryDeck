# Roadmap

## Current: XIAO ESP32-S3

Maintain reproducible archives and documentation for the existing v1.0–v2.2 development line. Preserve the working Windows companion and reconnect-library patch. Record device-tested behaviour separately from static checks.

## Final platform: nRF52840 (planned)

The maintainer intends the final version to use nRF52840. The exact board has not yet been specified.

- [ ] Select the exact board, Arduino core or SDK, and BLE stack.
- [ ] Define and electrically verify display, encoder, button, beeper and optional backlight connections.
- [ ] Port the BLE HID and custom companion service while preserving a documented protocol.
- [ ] Replace ESP32-specific storage, critical sections, interrupt and sleep implementations.
- [ ] Validate reconnects, HID/media controls, companion sync and power behaviour on the chosen hardware.
- [ ] Publish board-specific build/install instructions and a separately tested release.

These items are plans, not implemented features. No nRF52840 pinout, binary compatibility or release number is promised. The ESP32-S3 firmware must not be used as an nRF52840 build.
