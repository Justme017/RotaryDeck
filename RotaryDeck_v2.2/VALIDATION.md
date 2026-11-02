# Validation report — consolidated v2.2 source package

## Passed during packaging
- DeckCore.h and DisplayUI.h match the extracted dashboard/date archive's Git blob fingerprints exactly.
- Corrected companion matches the archived fixed companion byte-for-byte (CRLF preserved).
- Reconnect patcher's output on the uploaded original library matches the archived reconnect candidate fingerprint exactly.
- Patcher recognises the already-patched source and refuses unfamiliar source.
- Python syntax checks passed for all packaged Python files.
- Eight included portable unittest tests passed: packet formatting, chunking, volume range/mute, UUID/receiver agreement, header fingerprints, sketch-folder matching and patcher guards.
- Actual firmware receiver logic compiled and passed host C++11 tests with undefined-behaviour checks. Valid volume/mute values, unavailable volume, invalid values and disconnected-state rejection were checked.
- UI compiled under host C++11 with mocked U8g2/Arduino functions and the actual state declarations; exercised clock formatting, all screens and rapid carousel changes with mocked text bounds and undefined-behaviour checks.
- Menu geometry checked for representative font ascent/descent measurements.
- Final ZIP integrity, safe paths and packaged SHA-256 checksums checked.

## Not performed
- No full Arduino/ESP32 compilation: arduino-cli and the ESP32 toolchain were not available in this environment.
- No real Windows COM/WinRT/audio/Bluetooth run.
- No physical LCD rendering, firmware upload, power-cycle test or clock-preference reboot test of this newly consolidated ZIP.
- Dependency ranges are not a tested lockfile for a fresh Windows installation.
- No legal clearance of upstream library redistribution, no enclosure fit or wiring verification.

The owner previously reported the reconnect patch working. That is evidence for that tested local patch, not independent validation of this entire assembled archive. This package preserves the known source fingerprints rather than introducing new firmware behaviour.

## Before publishing as a stable download
Run Arduino Verify/Upload and the hardware acceptance checks in docs/INSTALLATION.md. Verify the companion in a clean local environment, confirm required PC shortcut bindings, and review licensing. A complete source package is not the same as a compiled or fully validated release.
