import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from time import time
from pathlib import Path
from model import TYPES, BUILTINS, ProfileError, validate, load_profile, save_profile, profile_folder, safe_stem, warnings, test_action
from deck_sync import DeckSyncClient, SyncError, SyncUnsupportedError

class Editor:
    def __init__(self, window):
        self.window = window
        self.path = None
        self.dirty = False
        self.loading = False
        self.rows = {}
        self.name = tk.StringVar()
        self.status = tk.StringVar(value='Local editor only. Device sync unavailable: no v2.3-capable firmware endpoint detected.')
        self.sync_transport = None
        window.title('RotaryDeck Control Centre - local editor')
        window.geometry('1100x650')
        window.minsize(920, 540)
        toolbar = ttk.Frame(window, padding=10)
        toolbar.pack(fill='x')
        buttons = [('Load / import', self.load), ('Save', self.save), ('Save as', lambda: self.save(True)), ('Restore default', self.restore)]
        for title, command in buttons:
            ttk.Button(toolbar, text=title, command=command).pack(side='left', padx=3)
        self.sync_button = ttk.Button(toolbar, text='Sync to deck', command=self.sync_to_deck, state='disabled')
        self.sync_button.pack(side='right')
        namebar = ttk.Frame(window, padding=(12, 4))
        namebar.pack(fill='x')
        ttk.Label(namebar, text='Profile name:').pack(side='left')
        ttk.Entry(namebar, textvariable=self.name, width=42).pack(side='left', padx=8)
        self.name.trace_add('write', self.changed)
        tabs = ttk.Notebook(window)
        tabs.pack(fill='both', expand=True, padx=12, pady=8)
        for group in ('apps', 'actions'):
            tab = ttk.Frame(tabs, padding=10)
            tabs.add(tab, text=group.title() + ' - six slots')
            tab.columnconfigure(3, weight=1)
            for column, title in enumerate(('Slot', 'Label (max 16)', 'Type', 'Target / built-in identifier', '')):
                ttk.Label(tab, text=title).grid(row=0, column=column, padx=4, pady=8, sticky='w')
            self.rows[group] = []
            for index in range(6):
                label, kind, target = tk.StringVar(), tk.StringVar(), tk.StringVar()
                row = index + 1
                ttk.Label(tab, text=str(row)).grid(row=row, column=0, padx=4)
                ttk.Entry(tab, textvariable=label, width=19).grid(row=row, column=1, padx=4, pady=10)
                ttk.Combobox(tab, textvariable=kind, values=TYPES, state='readonly', width=15).grid(row=row, column=2, padx=4)
                field = ttk.Combobox(tab, textvariable=target, width=42)
                field.grid(row=row, column=3, padx=4, sticky='ew')
                def refresh(*_, variable=kind, widget=field):
                    builtin = variable.get() == 'builtin'
                    widget.configure(values=BUILTINS if builtin else (), state='readonly' if builtin else 'normal')
                kind.trace_add('write', refresh)
                ttk.Button(tab, text='Test on PC', command=lambda g=group, i=index: self.test(g, i)).grid(row=row, column=4, padx=4)
                for variable in (label, kind, target):
                    variable.trace_add('write', self.changed)
                self.rows[group].append((label, kind, target))
            ttk.Label(tab, text='Only URL and folder execution is implemented. Load, save, import and restore never run actions.', wraplength=820).grid(row=8, column=0, columnspan=5, sticky='w', pady=20)
        ttk.Label(window, textvariable=self.status, padding=10, wraplength=1050).pack(fill='x')
        ttk.Label(window, text='Firmware baseline: Arduino-ESP32 exactly 2.0.17. No firmware or BLE-library changes.', padding=(10, 0, 10, 10)).pack(fill='x')
        window.protocol('WM_DELETE_WINDOW', self.close)
        self.refresh_sync_state()
        try:
            self.show(load_profile(Path(__file__).parent / 'profiles' / 'default.json'))
        except (OSError, ValueError) as exc:
            messagebox.showerror('Default profile failed to load', str(exc))

    def changed(self, *_):
        if not self.loading:
            self.dirty = True
            self.status.set('Unsaved edits. Device sync unavailable until a v2.3-capable deck endpoint is connected.')

    def refresh_sync_state(self):
        self.sync_button.configure(state='normal' if self.sync_transport else 'disabled')

    def sync_to_deck(self):
        if not self.sync_transport:
            self.status.set('Device sync unavailable: connected firmware is missing required v2.3 capability endpoints.')
            return
        try:
            profile = self.collect()
            client = DeckSyncClient(self.sync_transport)
            revision = int(time())
            client.sync_profile(profile, revision)
            self.status.set('Synced: APPLIED acknowledgement and readback digest matched.')
        except SyncUnsupportedError as exc:
            self.status.set(f'Device sync unavailable: {exc}')
        except (SyncError, OSError, ValueError) as exc:
            self.status.set(f'Device sync failed: {exc}')

    def discard(self):
        return not self.dirty or messagebox.askyesno('Unsaved edits', 'Discard unsaved edits?')

    def show(self, profile, path=None):
        validate(profile)
        self.loading = True
        try:
            self.name.set(profile['profile_name'])
            for group, rows in self.rows.items():
                for entry in sorted(profile[group], key=lambda item: item['slot']):
                    label, kind, target = rows[entry['slot'] - 1]
                    label.set(entry['label'])
                    kind.set(entry['type'])
                    target.set(entry.get('target', entry.get('builtin_action', '')))
            self.path = path
            self.dirty = False
        finally:
            self.loading = False
        self.status.set(f'Loaded: {path or "bundled example - not yet saved"}. Not synced to device.')

    def collect(self):
        profile = {'schema_version': 1, 'profile_name': self.name.get(), 'apps': [], 'actions': []}
        for group, rows in self.rows.items():
            for index, (label, kind, target) in enumerate(rows, 1):
                field = 'builtin_action' if kind.get() == 'builtin' else 'target'
                profile[group].append({'slot': index, 'label': label.get(), 'type': kind.get(), field: target.get()})
        return validate(profile)

    def load(self):
        if not self.discard():
            return
        try:
            selected = filedialog.askopenfilename(initialdir=profile_folder(), filetypes=[('JSON profiles', '*.json')])
            if selected:
                self.show(load_profile(selected), Path(selected))
        except (OSError, ValueError) as exc:
            messagebox.showerror('Load failed - current edits retained', str(exc))

    def save(self, save_as=False):
        try:
            profile = self.collect()
            notes = warnings(profile)
            if notes and not messagebox.askyesno('Profile warnings', '\n'.join(notes) + '\n\nSave anyway? No actions will run.'):
                return
            path = self.path
            if path is None or save_as:
                selected = filedialog.asksaveasfilename(initialdir=profile_folder(), initialfile=safe_stem(profile['profile_name']) + '.json', defaultextension='.json', filetypes=[('JSON profiles', '*.json')])
                if not selected:
                    return
                path = Path(selected)
            backup = save_profile(profile, path)
            self.path = path
            self.dirty = False
            self.status.set(f'Saved locally: {path}. ' + (f'Backup: {backup}. ' if backup else '') + 'Not synced to device.')
        except (OSError, ValueError) as exc:
            messagebox.showerror('Save failed', str(exc))

    def restore(self):
        if not self.discard():
            return
        try:
            self.show(load_profile(Path(__file__).parent / 'profiles' / 'default.json'))
        except (OSError, ValueError) as exc:
            messagebox.showerror('Restore failed', str(exc))

    def test(self, group, index):
        try:
            entry = self.collect()[group][index]
            if entry['type'] not in ('open_url', 'open_folder'):
                raise ProfileError('Only URL and folder tests are implemented.')
            if not messagebox.askyesno('Run this action now?', f'{entry["label"]}\n{entry["target"]}\n\nAsk Windows to open this target?'):
                return
            test_action(entry, confirmed=True)
            self.status.set('Open request sent to Windows. Verify the actual result; this is not device sync.')
        except (OSError, ValueError) as exc:
            messagebox.showerror('Test failed', str(exc))

    def close(self):
        if self.discard():
            self.window.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    Editor(root)
    root.mainloop()
