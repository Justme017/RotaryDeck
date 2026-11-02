# Controls and current limits

Rotate the encoder to move selection. Press to activate. Use the configured back gesture (double press or hold); the footer reflects it. On Media, select VOLUME and press to enter adjustment, rotate to change volume, and press to finish.

Settings > Display > CLOCK: 24H toggles to 12H and saves immediately. 12H mode shows AM/PM; 24H mode shows the year in the right-hand date column. Time is valid only after sync; date derives from that same local time.

## Apps: fixed shortcut mapping
| Display label | HID shortcut |
|---|---|
| CHROME | Ctrl+Alt+Shift+F2 |
| SPOTIFY | Ctrl+Alt+Shift+F3 |
| DISCORD | Ctrl+Alt+Shift+F4 |
| FILES | Windows+E |
| OBS | Ctrl+Alt+Shift+F6 |
| CODE | Ctrl+Alt+Shift+F1 |

Except FILES, these require PC-side bindings. This package does not install a launch helper or claim these applications automatically launch. Keep your existing helper or configure those shortcuts separately. Custom slots and a graphical editor are future work.

## Actions: fixed mapping
SHOT sends Windows+Shift+S; MUTE sends media mute; LOCK sends Windows+L; SEARCH sends Windows+S; DESKTOP sends Windows+D; TASKS sends Windows+Tab. These are Windows-oriented mappings, not cross-platform support claims. Do not test LOCK while unsaved work or access requirements make locking inconvenient.

The deck is an input device. A connected indicator or COMMAND SENT message does not prove Windows executed a command. Companion telemetry uses a separate custom GATT service.
