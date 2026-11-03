# Installation and troubleshooting

Updated 2026-11-03. Windows companion previews and firmware archives are separate downloads. Keep your working firmware/library backup while testing candidate desktop builds.

## Windows desktop preview

1. Open [Windows companion EXE builds](https://github.com/Justme017/RotaryDeck/actions/workflows/windows-companion-exe.yml?query=branch%3Afeature%2Fv2.3-control-centre). Choose a successful run for the intended commit, not a queued/failed run.
2. Download its RotaryDeckCompanion-Windows-x64-preview artifact while retained. Sign-in may be required. Extract the ZIP.
3. If RotaryDeckSetup-Windows-x64-preview.exe is included, use it for installation/startup integration. The standalone RotaryDeckCompanion.exe is the application, not an installer. No separate Python/BAT environment is required for the packaged app.
4. Installer target defaults to the current user's LocalAppData/Programs/RotaryDeck. Review the startup checkbox; it can be changed in Settings. Profiles remain under the user's saved locations.
5. Stop older companion scripts/windows. Pair the deck in Windows, open Companion, enter its paired name or exact ID and click Start. Read the log; Starting does not prove connection.

The desktop source is on the development branch. Feature inclusion depends on the exact artifact; newest installer/tray behavior still requires real Windows acceptance. The preview is unsigned. Publisher metadata alone does not establish trusted Windows signing. Do not disable security protection as a generic installation fix.

## Tray, startup and exit

Candidate desktop builds hide the window on close only after tray creation succeeds, with an initial notice. Tray menu: Open, Start bridge, Stop bridge, Exit. Exit checks unsaved profile edits and stops telemetry. Settings/About also offers Exit.

With startup enabled, the installed app launches in the tray and starts the bridge using the saved device selection. The setting can be disabled in the app or Windows Startup Apps. Startup configuration inside the app requires its expected installed location. Uninstall removes the app startup entry; user profiles/preferences are retained. Validate these paths on the exact installed build.

## Local profiles and tools

Apps & Actions edits six slots per group locally. Loading/importing/saving/restoring never runs actions. Test on PC supports confirmed URLs/folders only. Restore default loads the bundled example; recover saved backups by importing them and using Save as. Profile editing does not currently change the physical deck.

Tools diagnostics check dependencies/audio, not full BLE readiness. Reconnect patching requires the exact supported BleKeyboard.cpp/header fingerprints, an explicit target confirmation and backup. Close Arduino IDE first and rebuild/upload separately afterward. Do not force unfamiliar libraries or repeatedly patch a working setup.

## Mandatory firmware platform/core

Current firmware archives target Seeed Studio XIAO ESP32-S3. Install Espressif's Arduino-ESP32 board package at **exactly 2.0.17**, not a different 2.x/3.x version. This is the board package version, not IDE/app/firmware version. See [COMPATIBILITY.md](COMPATIBILITY.md). nRF52840 is unsupported by these images. Do not switch BLE backend/core as a generic fix.

## Manual firmware installation

1. Back up working sketch and library files. Download the manually attached version ZIP from [Releases](https://github.com/Justme017/RotaryDeck/releases), not an automatic archive as a substitute for historical firmware.
2. Preserve the matching .ino and folder names. In the consolidated v2.2 source these remain RotaryDeck_v2_1 intentionally.
3. Keep known-working board/port settings, U8g2, T-vK ESP32 BLE Keyboard 0.3.0 and documented reconnect changes. Verify core 2.0.17 before compiling.
4. Use the matching DeckCore.h/DisplayUI.h. Apply any required guarded library patch to the installed library, not the sketch, and avoid duplicate library copies.
5. Verify then upload using Arduino tools. Preserve working wiring; firmware GPIO constants are not a universal display-connector pinout or voltage specification.

The Firmware tab does not yet flash over USB: a validated compiled package, addresses/settings and real-board testing remain required. A source ZIP is not flashable firmware.

## Legacy script alternative

Use the companion matched to the firmware archive. In its companion folder, setup_companion.bat creates a local Python environment and installs requirements; start_companion.bat runs the telemetry bridge. Do not run this alongside the GUI bridge. Do not redistribute .venv.

## Acceptance and troubleshooting

- Verify actual volume/mute/track/play response, telemetry, menu/clock-format persistence and reconnect after power cycles with the bridge stopped/running.
- COMMAND SENT is a send attempt, not execution acknowledgement. Bluetooth pairing does not itself prove HID or custom GATT readiness.
- Missing telemetry: inspect the exact log, pairing/name/device selection and correct receiver firmware.
- Audio errors: check the Windows default output endpoint. Unknown volume is not zero; media titles depend on app metadata.
- Do not erase flash, disable encryption or repeatedly re-pair without an error-specific reason.
- Review logs/screenshots before sharing: device IDs, titles, usernames and paths may be present.
