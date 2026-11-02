# Changelog — v2.2 consolidated source packaging

This package consolidates the known v2.2 development components. It is not a newly compiled binary or a fresh claim of complete hardware validation.

## Included development work
- Animated carousel and category pixel animations; centred position dots.
- Clearer speaker icons, menu spacing and Media labels.
- Windows default-output volume/mute telemetry and matching firmware receiver.
- Working named WinRT overloads for enumeration, service/characteristic discovery and writes.
- Saved 12/24-hour clock selection and compact seconds/date dashboard.
- Reconnect patcher reproducing the same local library modifications reported working by the owner.

## Packaging
- Matched sketch and headers; original sketch name retained to avoid folder/name breakage.
- Clean companion with setup/start/diagnostic launchers; no bundled .venv or logs.
- Portable packet/patcher tests, dependency ranges, source provenance and checksums.
- No upstream BLE library source included; install the compatible upstream library separately and apply the local change where permitted.

## Not implemented
Companion GUI, configurable custom slots, profiles/configuration transfer, case, verified wiring diagrams, Linux/macOS support and nRF52840 port remain planned. Existing app buttons use fixed shortcuts and require PC-side bindings.
