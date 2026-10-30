# RotaryDeck profile schema

## File format

Profiles are UTF-8 JSON files with extension `.json`.

- `schema_version` must be `1`.
- `profile_name` is a non-empty display name, maximum 40 characters.
- `apps` and `actions` must each contain exactly six entries.
- Slots are identified by `slot`, from `1` through `6`.
- Unknown fields are rejected rather than silently ignored.

## App slot

| Field | Type | Rules |
|---|---|---|
| `slot` | integer | `1`–`6`, unique |
| `label` | string | 1–16 characters; used on the display |
| `type` | string | `open_app`, `open_url`, `open_folder`, `run_shortcut`, or `builtin` |
| `target` | string | Required except for `builtin`; maximum 512 characters |
| `builtin_action` | string | Required only for `builtin`; see `ACTION_TYPES.md` |

## Action slot

Action slots use the same fields as app slots. Their semantic purpose is tools and quick actions rather than application launchers.

## Validation rules

- Reject an empty or whitespace-only label.
- Reject duplicate slot numbers.
- Reject unsupported `type` values.
- Require a target for every non-`builtin` action.
- Require `builtin_action` only for `builtin` actions.
- Validate HTTP/HTTPS URLs before saving.
- Validate that local application, folder, and shortcut paths exist at save time where practical.
- Warn, but do not silently alter, labels containing characters unsupported by the display font.

## Example

```json
{
  "schema_version": 1,
  "profile_name": "Default",
  "apps": [
    { "slot": 1, "label": "OBS", "type": "open_app", "target": "C:\\Program Files\\obs-studio\\bin\\64bit\\obs64.exe" },
    { "slot": 2, "label": "NETFLIX", "type": "open_url", "target": "https://www.netflix.com" },
    { "slot": 3, "label": "FILES", "type": "open_folder", "target": "C:\\Users\\Public" },
    { "slot": 4, "label": "SPOTIFY", "type": "open_app", "target": "spotify:" },
    { "slot": 5, "label": "GITHUB", "type": "open_url", "target": "https://github.com" },
    { "slot": 6, "label": "SETTINGS", "type": "builtin", "builtin_action": "open_settings" }
  ],
  "actions": [
    { "slot": 1, "label": "MUTE", "type": "builtin", "builtin_action": "toggle_mute" },
    { "slot": 2, "label": "PLAY", "type": "builtin", "builtin_action": "play_pause" },
    { "slot": 3, "label": "NEXT", "type": "builtin", "builtin_action": "next_track" },
    { "slot": 4, "label": "PREV", "type": "builtin", "builtin_action": "previous_track" },
    { "slot": 5, "label": "SHOT", "type": "builtin", "builtin_action": "screenshot" },
    { "slot": 6, "label": "VOL+", "type": "builtin", "builtin_action": "volume_up" }
  ]
}
```

This schema is the contract for the companion GUI, validation, and future firmware configuration messages.
