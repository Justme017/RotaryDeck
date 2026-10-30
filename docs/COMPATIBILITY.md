# Compatibility policy

## Current ESP32 baseline: pinned, not a minimum version

| Component | Requirement |
|---|---|
| Board | Seeed Studio XIAO ESP32-S3 |
| Arduino-ESP32 board package | Exactly 2.0.17 |
| Current v2.2 BLE library | T-vK ESP32 BLE Keyboard 0.3.0 with the documented local reconnect patch |
| BLE backend | Preserve the existing Bluedroid-based setup; no unreviewed NimBLE switch |

2.0.17 is not shorthand for 2.x, 2.0.17 or newer, or latest. No other ESP32 core version is supported for current releases. This policy does not claim that every other version has been tested and found to fail; it defines the project's supported build configuration.

The number refers to the esp32 package by Espressif Systems in Arduino Boards Manager. It does not refer to Arduino IDE, RotaryDeck v2.2, Python or the silicon revision.

## When this pin may change

A future upgrade or project-owned BLE implementation requires an explicit migration and documented tests before relaxing this requirement:

- Build the complete firmware with the proposed core and libraries.
- Verify HID keyboard/media controls and the encrypted companion service together.
- Test power-cycle reconnects with the companion stopped and running.
- Verify time/media/volume telemetry, settings, persistence and sleep/wake.
- Review library provenance/licensing and document reproducible dependency versions.
- Update firmware guards/build manifests, documentation and release notes together.

Do not automatically update archived releases' compatibility claims or recommend a core upgrade as a generic fix.

## Enforcement status

This commit makes the documentation requirement explicit. It does not add a compiler version guard, change firmware, rewrite the already-delivered ZIP, or update release descriptions. Those must be kept in sync in the next authorised source/package update.

## nRF52840

The planned nRF52840 implementation is separate. Its exact board, core/SDK, BLE stack and tested versions remain pending; Arduino-ESP32 2.0.17 is not an nRF52840 dependency.
