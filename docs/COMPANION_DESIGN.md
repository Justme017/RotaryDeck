# Configurable companion — proposed design

Status: requirements and design only. No graphical editor, dynamic slot protocol or cross-platform implementation is added by this document. The existing Windows sync script and fixed firmware actions remain the baseline.

## User outcome

A user can select an Apps slot labelled OBS, rename it NETFLIX, choose Open website, enter https://www.netflix.com, test it deliberately, then Save & Sync. The device label and action change together without recompiling firmware. The same editor configures Actions slots such as screenshot, mute or show desktop.

## Initial scope

Retain six Apps slots and six Actions slots. Variable page lengths, custom bitmap uploads and arbitrary scripts are later proposals, not first-iteration requirements.

Proposed action types:
- Open an application using a selected executable and structured arguments.
- Open a validated http/https website in the default browser.
- Open a selected folder.
- Send an explicitly configured keyboard shortcut.
- Execute a selected built-in media/system action.

## Proposed interface

- Device status: connection, sync state, firmware/protocol version and last error.
- Apps and Actions: slot list with device-length label preview.
- Editor: label, action type, target and argument fields appropriate to that type.
- Test on PC: explicit local action with confirmation where appropriate.
- Save & Sync: validate, save the host profile and apply device configuration.
- Profiles: create, select, export/import and restore defaults. Imported profiles are inert until reviewed and applied.

Only show Synced after a matching device acknowledgement. Distinguish host profile saved, device sync pending, and device sync failed.

## Responsibilities

The companion stores PC-specific application paths, website targets, arguments and OS-specific action implementations. The device stores bounded labels, slot identities, configuration revision and presentation information. It sends slot activation events rather than interpreting arbitrary PC command strings.

Keep basic media HID controls independent where practical. Companion-managed slots must show an unavailable status if the companion is absent; do not silently invoke a different action.

## Protocol work required

The current time/media/volume path does not itself implement custom slot activation. A matched firmware/companion revision must define:
- Protocol/capability negotiation.
- Stable page/slot identities and configuration revisions.
- Bounded, validated configuration transfer with staging and an explicit commit.
- Acknowledgement/error responses and rollback to the last valid configuration.
- Device-to-host activation events with session identifiers and duplicate suppression.
- Reconnect reconciliation without replaying old launch events.

Do not change the working packet formats or UUIDs merely by documenting this proposal. Concrete encoding, size limits and firmware storage strategy require review during implementation.

## Safety and portability

Treat an authenticated paired device as an input source, not permission to run arbitrary shell text. Resolve only actions in the locally approved active profile. Separate executable paths and arguments; disable arbitrary script execution for the first iteration. Validate labels, URLs, paths and profile sizes.

Display destructive or security-sensitive action confirmation on the PC where needed. Do not block the firmware loop waiting for user confirmation. Test imports, missing targets, interrupted sync, disconnects, duplicate events and acknowledgement loss.

Share the profile model and controller logic across OS backends, not assumptions about executable paths or shortcuts. Windows is the next implementation target; Linux and macOS remain unimplemented until their backends and permissions are tested.

## Acceptance scenario

1. Replace OBS with NETFLIX through the editor.
2. Test intentionally and confirm the intended website opens.
3. Save & Sync; receive acknowledgement and see NETFLIX on the device.
4. Activate the slot and open the configured target exactly once.
5. Reconnect/restart without replaying an activation.
6. Interrupt a later configuration update and retain the previous valid configuration.

Implementation, code framework selection and hardware/OS validation are subsequent tasks.
