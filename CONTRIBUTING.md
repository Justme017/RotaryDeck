# Contributing

Thanks for helping improve RotaryDeck.

For bug reports, include the release/archive name, exact board, Arduino core and library versions, companion/Python versions if relevant, reproduction steps, expected result and actual result. Remove credentials and unnecessary personal paths from logs.

For pull requests, keep one focused change per PR, describe the files and behaviour changed, preserve third-party notices, and report exactly what was tested. Distinguish syntax/static checks, actual firmware builds, and tests on physical hardware. Do not claim CI or device coverage that was not run.

Current archives target XIAO ESP32-S3. Discuss the selected nRF52840 board and implementation before submitting a platform port. Do not replace working ESP32-specific code with an untested cross-platform claim.

Do not commit .venv, dependencies installed on a workstation, credentials, logs or generated binaries. Original contributions must be code you own or have permission to contribute; third-party code must retain its applicable licence and attribution.
