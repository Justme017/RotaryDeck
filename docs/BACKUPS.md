# Profile backups

## Location

Store user profiles locally under:

```text
%APPDATA%\RotaryDeck\profiles\
```

Store automatic backups under:

```text
%APPDATA%\RotaryDeck\profiles\backups\
```

Do not store profiles in the program installation folder or distribute a `.venv`.

## Naming

Use this pattern:

```text
YYYY-MM-DD-HHMMSS-profile-name.json
```

Example:

```text
2026-10-30-151900-default.json
```

## Rules

- Create a backup before overwriting an existing profile.
- Create a backup before importing a profile that replaces the current one.
- Do not create a backup merely for opening or viewing a profile.
- Retain at least the ten most recent backups per profile name.
- Never automatically launch an action while creating, loading, importing, or restoring a backup.
- Show the backup location in the Control Centre so users can retrieve files manually.
