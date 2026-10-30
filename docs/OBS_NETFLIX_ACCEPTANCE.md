# OBS to Netflix acceptance test

This is the end-to-end test for configurable app slots. It must pass before v2.3 can claim dynamic Apps and Actions.

## Preconditions

- [ ] v2.2 firmware is installed and working.
- [ ] Arduino-ESP32 is exactly 2.0.17.
- [ ] The v2.3 Control Centre can load and save a profile.
- [ ] Device sync is implemented only if firmware acknowledgement exists; otherwise it must clearly remain unavailable.

## Test steps

1. Load `profiles/default.json`.
2. Confirm slot 1 is labelled `OBS` and targets the OBS executable.
3. Confirm slot 2 is labelled `NETFLIX` and targets `https://www.netflix.com`.
4. Use **Test on PC** for slot 1 and verify OBS opens.
5. Use **Test on PC** for slot 2 and verify Netflix opens in the default browser.
6. Save the profile locally.
7. Reload the profile and confirm both slots remain unchanged.
8. If device sync is implemented, send the profile to the deck and wait for an explicit acknowledgement.
9. Rotate the deck to slot 1 and activate it; verify the configured action runs.
10. Rotate to slot 2 and activate it; verify Netflix opens.
11. Power-cycle the deck.
12. Reconnect and repeat steps 9–10.
13. Restore the OBS configuration and repeat the relevant activation test.

## Pass criteria

- [ ] No firmware recompilation is needed to change OBS to Netflix.
- [ ] The display shows the configured labels within the documented limits.
- [ ] Activation runs the intended configured action.
- [ ] Reconnection preserves the intended configured behaviour.
- [ ] No automatic action runs during profile load, import, reconnect, or sync.
- [ ] Existing media controls, telemetry, clock preference, and menus continue to work.
