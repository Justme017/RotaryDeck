# GPIO reference — not a verified wiring diagram

Values copied from the included DeckCore.h. These are ESP32 GPIO numbers, NOT XIAO D labels, LCD connector pin numbers or a supply-voltage specification.

| Function | ESP32 GPIO |
|---|---:|
| Display CLOCK | 7 |
| Display DATA | 9 |
| Display CS | 44 |
| Encoder A | 1 |
| Encoder B | 4 |
| Button / wake | 5 |
| Beeper | 6 |

Preserve your known-working connections. The exact salvaged display PCB/connector, logic levels and power arrangement must be verified before another build. Ender 3/V3 naming does not establish universal pin compatibility. S3 and nRF52840 wiring diagrams remain pending. No backlight-control hardware is implemented in this release.
