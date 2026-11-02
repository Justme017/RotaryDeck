# RotaryDeck Control Centre: local editor

This revision replaces accidentally committed marker files with actual Python source. It is a local editor, not implemented deck sync or a public v2.3 release.

## Run on Windows

Use Python 3.10 or newer with Tcl/Tk. No pip dependencies are required. Keep the entire control_centre folder, including profiles/default.json. Run the existing start_control_centre.bat or run python app.py from this folder.

Edit six Apps and six Actions slots. Choose a type; builtin uses an identifier from its dropdown, while other types use a target. Save/load JSON locally. Test on PC supports HTTP/HTTPS websites and existing absolute folders only, after explicit confirmation. Application, shortcut and built-in execution are not implemented.

## Storage and backups

The suggested directory is %APPDATA%/RotaryDeck/profiles. Save as may select another directory. Before overwriting, the old bytes are backed up in a sibling backups folder. Names include a timestamp, a sanitized filename stem and a filename hash to distinguish similar names; ten backups are retained per filename. Writes use a temporary file followed by replacement. A failed replacement leaves the old file intact.

Load/import changes the editor only. Later Save overwrites the selected file with a backup; use Save as to preserve the imported original. Unsaved edits require discard confirmation before load, restore or close. Loading, restoring, importing and saving never execute an action. Review imported targets before testing.

## Deck sync and limits

The default profile is illustrative, not a verified copy of device mappings. Local paths may not exist on another PC; missing paths and application URIs generate warnings.

Host-side v2.3 sync logic is implemented in `deck_sync.py`: capability discovery, bounded framing/chunking, transaction IDs, sequence checks, digest/length validation, cancellation, retries, APPLIED acknowledgement handling, revision/digest readback validation, and slot-activation event de-duplication. Existing telemetry UUIDs remain unchanged (`917e0001` service and encrypted-write `917e0002` RX); new v2.3 config endpoints are explicitly separate (`917e1001/917e1002/917e1003`).

The GUI keeps Sync unavailable unless a connected deck exposes the required v2.3 capability endpoint. Unsupported/older firmware is reported honestly and never shown as Synced. Synced status is shown only after APPLIED plus matching readback digest/revision.

Arduino-ESP32 must remain exactly 2.0.17. This commit changes no firmware, core, BLE library, board target or main-branch content.

## Validation

Run `python -m py_compile model.py app.py deck_sync.py test_model.py test_deck_sync.py` and then `python -m unittest -v test_model.py test_deck_sync.py` from `control_centre`.

A fresh Windows GUI + real-device smoke test is still required on this exact revision: edit/save/reload, overwrite backup, reject invalid input, cancel unsaved navigation, open a URL/folder deliberately, verify unsupported firmware states are honest, and validate APPLIED+readback behaviour on v2.3-capable firmware.
