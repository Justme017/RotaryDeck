# Hardware evidence

This folder collects the evidence needed before public documentation or a hardware release.

## Required files

- `display-pcb-front.jpg` — front of the exact display PCB.
- `display-pcb-back.jpg` — back of the exact display PCB, showing markings and connector orientation.
- `wiring-esp32-s3.md` — verified XIAO ESP32-S3 wiring table and notes.
- `enclosure-measurements.md` — display, encoder, PCB, cable, and case dimensions.
- `assembly photos/` — assembled unit photos from several angles.
- `screen-captures/` — real photos or GIFs of menus and features.

## Rules

- Do not assume that “Ender 3” or “Ender 3 V3” naming guarantees pin compatibility.
- Verify every connection against the actual display PCB and selected wiring source.
- Do not publish wiring as universal until it has been checked against the exact hardware.
- Keep nRF52840 evidence in a separate future folder; do not mix its wiring with ESP32-S3 documentation.
