# Project status

## Done

- [x] v2.2 firmware and Windows companion are working.
- [x] Arduino-ESP32 core is pinned to exactly 2.0.17 for current ESP32 releases.
- [x] Compatibility policy documents the strict core requirement.
- [x] v2.3 development branch created.

## In progress

- [ ] Windows Control Centre editor for Apps and Actions.
- [ ] Local profile save/load and validation.
- [ ] PC-side action testing.

## Next

- [ ] Firmware configuration-message support.
- [ ] Dynamic display labels and slot activation.
- [ ] OBS-to-Netflix end-to-end validation.
- [ ] Enclosure, wiring evidence, screen GIFs/photos, and concise user documentation.

## Guardrails

- Keep `main` as the known-working v2.2 baseline.
- Do not upgrade Arduino-ESP32 away from 2.0.17 during v2.3.
- Do not mix nRF52840 work into the ESP32 v2.3 release.
- Do not claim device sync is available until firmware acknowledgement is implemented and tested.
