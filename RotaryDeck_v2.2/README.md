# RotaryDeck v2.2 — complete source package

Give an Ender 3 display a second life as a Bluetooth desktop controller.

Target: Seeed Studio XIAO ESP32-S3. Windows companion included. This is a consolidated source distribution, not a compiled firmware binary or a newly certified stable build.

## Start here
1. Back up your working sketch, BLE library and companion.
2. Read docs/INSTALLATION.md.
3. Open firmware/RotaryDeck_v2_1/RotaryDeck_v2_1.ino in Arduino IDE.
4. Keep your known-working board settings and wiring. Verify the local reconnect patch as documented, then Verify and Upload.
5. Run companion/setup_companion.bat, then companion/start_companion.bat.

The sketch/folder name intentionally remains RotaryDeck_v2_1 for compatibility. Its included UI is v2.2.

## Included
- Complete sketch and both matching headers.
- Animated carousel, centred dots, solid speaker icons and improved Media layout.
- Clock/date dashboard and saved 12/24-hour setting.
- Actual Windows output-volume/mute telemetry.
- Corrected Windows enumeration and GATT overload calls.
- A fingerprint-checked reconnect patcher for your locally installed BLE Keyboard library.
- Installation, controls, protocol, changelog, licensing, tests and checksums.

## Not included / not implemented
No compiled .bin, graphical companion, editable custom Apps/Actions, enclosure, verified wiring diagrams, Linux/macOS implementation or nRF52840 firmware. App shortcuts remain fixed and may require an existing host-side shortcut helper; the companion does not launch apps.

Original maintainer-owned work: MIT, see LICENSE. Third-party code remains under its own applicable terms; see THIRD_PARTY_NOTICES.md. Upstream BLE library source and installed dependencies are deliberately not bundled.

See VALIDATION.md for checks actually run and checks still required on Windows/hardware. SHA256SUMS.txt covers packaged files; SOURCE_MANIFEST.json records provenance. No GitHub upload, release publication or visibility change was performed by assembling this ZIP.
