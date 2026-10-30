# Private development roadmap

The repository stays private. This plan does not publish releases, change visibility, or claim unfinished features exist. Current archives remain XIAO ESP32-S3 builds; the final hardware direction is nRF52840.

## 1. Repository foundation

- [x] Concise README with current-versus-planned status.
- [x] Document launch gates and configurable companion requirements.
- [ ] Import a reviewed, reproducible current source tree without changing behaviour.
- [ ] Identify exact dependency versions and preserve the working companion/reconnect fixes.
- [ ] Check existing release tags, archives, licences and completeness.

The checked items refer to documentation only, not implementation of the features below.

## 2. Windows companion and configurable slots — next implementation milestone

- [ ] Create a usable graphical interface for connection, live status and configuration.
- [ ] Edit the existing six Apps and six Actions slots: name, action type and target.
- [ ] Support app, website, folder, keyboard-shortcut and built-in actions.
- [ ] Add explicit Test on PC and Save & Sync controls.
- [ ] Persist host profiles and validate imports without executing them.
- [ ] Sync device labels and slot identities with acknowledged configuration transfer.
- [ ] Add device-to-companion activation events with duplicate protection.
- [ ] Handle unavailable companion, invalid targets, failed sync and reconnect safely.
- [ ] Retain independent basic HID media control where practical.

See docs/COMPANION_DESIGN.md. This requires matched firmware and companion changes; renaming a label alone does not change an action.

## 3. Final hardware and firmware

- [ ] Select the exact nRF52840 board, core/SDK and BLE stack.
- [ ] Port BLE HID, companion protocol, storage, interrupts and sleep.
- [ ] Verify reconnect, configuration persistence, media controls and telemetry on-device.
- [ ] Keep the S3 version buildable as a separate supported development target.

No nRF52840 pinout, binary or release number is established yet.

## 4. Wiring and enclosure

- [ ] Verify the exact salvaged display PCB and connector orientation.
- [ ] Produce and electrically validate the XIAO ESP32-S3 wiring diagram.
- [ ] Produce a separate verified diagram for the selected nRF52840 board.
- [ ] Measure display, mounting holes, encoder, boards and connector clearances.
- [ ] Design the case; test fit, cable routing and access with printed prototypes.
- [ ] Publish editable CAD and print-ready files with assembly instructions.

Mechanical concepts can begin earlier; final mounting depends on the selected hardware.

## 5. Linux and macOS

- [ ] Define common action/profile interfaces and OS-specific capabilities.
- [ ] Implement Linux connection, launching, shortcuts and supported media/volume integrations.
- [ ] Implement macOS equivalents with documented permission requirements.
- [ ] Test each platform before describing it as supported.

Windows paths and shortcuts must not be presented as portable profiles without validation.

## 6. Visual documentation and release

- [ ] Capture real screen photos and short GIFs of carousel, media, clock/date and custom-slot editing.
- [ ] Keep the README short and move detailed instructions into docs.
- [ ] Validate clean setup, configuration, power cycles and recovery on supported hardware/OS combinations.
- [ ] Review release contents, third-party licences and sensitive information.
- [ ] Obtain explicit owner approval before changing visibility or publishing releases.

Use docs/LAUNCH_CHECKLIST.md as the release gate. These checkboxes are pending work, not a promise of completion or a release date.
