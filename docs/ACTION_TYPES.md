# Action types

These identifiers are shared by profiles, the Windows Control Centre, and future firmware configuration handling.

| Type | Meaning | Required fields | PC test behaviour |
|---|---|---|---|
| `open_app` | Launch an installed application or registered URI | `target` | Launch the target without arguments unless a later schema adds them |
| `open_url` | Open an HTTP or HTTPS website | `target` | Open the URL in the default browser |
| `open_folder` | Open a local folder in File Explorer | `target` | Open the folder if it exists |
| `run_shortcut` | Run a Windows `.lnk` shortcut | `target` | Launch the shortcut if it exists |
| `builtin` | Run a firmware/companion-defined action | `builtin_action` | Execute only the selected built-in action |

## Built-in actions

| Identifier | Meaning |
|---|---|
| `toggle_mute` | Toggle system mute |
| `play_pause` | Toggle media play/pause |
| `next_track` | Advance to the next media track |
| `previous_track` | Return to the previous media track |
| `screenshot` | Trigger the configured screenshot action |
| `volume_up` | Increase system volume |
| `volume_down` | Decrease system volume |
| `open_settings` | Open the RotaryDeck settings view |

## Rules

- Do not add implicit fallbacks: an unsupported type must fail validation.
- Do not auto-run an action when loading or importing a profile.
- `Test on PC` must require an explicit user click.
- Device activation is a separate future firmware feature and must not be assumed to work because PC testing succeeds.
