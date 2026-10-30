# RotaryDeck Control Centre: local editor

This revision replaces accidentally committed marker files with actual Python source. It is a local editor, not implemented deck sync or a public v2.3 release.

## Run on Windows

Use Python 3.10 or newer with Tcl/Tk. No pip dependencies are required. Keep the entire control_centre folder, including profiles/default.json. Run the existing start_control_centre.bat or run python app.py from this folder.

Edit six Apps and six Actions slots. Choose a type; builtin uses an identifier from its dropdown, while other types use a target. Save/load JSON locally. Test on PC supports HTTP/HTTPS websites and existing absolute folders only, after explicit confirmation. Application, shortcut and built-in execution are not implemented.

## Storage and backups

The suggested directory is %APPDATA%/RotaryDeck/profiles. Save as may select another directory. Before overwriting, the old bytes are backed up in a sibling backups folder. Names include a timestamp, a sanitized filename stem and a filename hash to distinguish similar names; ten backups are retained per filename. Writes use a temporary file followed by replacement. A failed replacement leaves the old file intact.

Load/import changes the editor only. Later Save overwrites the selected file with a backup; use Save as to preserve the imported original. Unsaved edits require discard confirmation before load, restore or close. Loading, restoring, importing and saving never execute an action. Review imported targets before testing.

## Limits

The default profile is illustrative, not a verified copy of device mappings. Local paths may not exist on another PC; missing paths and application URIs generate warnings. Unsupported labels are preserved with font/width warnings; no physical display rendering is implemented here. The Sync to deck button is disabled and never claims success. Keep the existing v2.2 telemetry companion; this editor does not replace it.

Arduino-ESP32 must remain exactly 2.0.17. This commit changes no firmware, core, BLE library, board target or main-branch content.

## Validation

Run python -m unittest -v test_model.py from control_centre. This exact correction revision has not yet been executed; TEST_RESULTS.txt states that explicitly. Earlier test results do not certify this revision. A fresh Windows GUI smoke test is also required: edit, save/reload, overwrite and inspect backup, reject invalid input, cancel unsaved navigation, open a URL/folder deliberately, and confirm sync stays disabled.
