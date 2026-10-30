# Display label rules

These rules keep companion-entered labels predictable on the current display.

| Rule | Value |
|---|---|
| Maximum stored length | 16 characters |
| Maximum rendered length | 12 characters |
| Empty label | Rejected at save time |
| Whitespace-only label | Rejected at save time |
| Unsupported characters | Warn at save time; do not silently rewrite user text |
| Rendering fallback | Truncate from the end and append `…` only when truncation is required |
| Empty rendered result | Show `SLOT n` |

## Rendering examples

| Entered label | Displayed label |
|---|---|
| `OBS` | `OBS` |
| `NETFLIX` | `NETFLIX` |
| `SPOTIFY MUSIC` | `SPOTIFY MUS…` |
| Empty | `SLOT 4` |

## Implementation notes

- The companion stores the user’s original label.
- The display renderer applies truncation; it does not modify the stored profile.
- The future firmware configuration message must carry the original label, not pre-truncated text.
- Emoji, complex scripts, and characters absent from the display font must produce a clear warning rather than a silent blank.
