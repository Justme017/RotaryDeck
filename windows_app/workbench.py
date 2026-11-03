import sys
sys.coinit_flags = 0
import os
import tempfile
from pathlib import Path
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import launcher
import profile_editor
import apply_reconnect_patch as patcher

BG, FG, PANEL, MUTED = '#151918', '#e4e9dc', '#202624', '#a8b3aa'

def theme(root):
    root.configure(bg=BG)
    s = ttk.Style(root)
    s.theme_use('clam')
    s.configure('.', background=BG, foreground=FG, font=('Segoe UI', 10))
    s.configure('TButton', background=PANEL, foreground=FG, padding=(14, 9), borderwidth=0)
    s.map('TButton', background=[('active', '#344039')], foreground=[('disabled', '#738078')])
    s.configure('TEntry', fieldbackground=PANEL, foreground=FG, insertcolor=FG, padding=7)
    s.configure('TCombobox', fieldbackground=PANEL, foreground=FG, padding=5)
    s.map('TCombobox', fieldbackground=[('readonly', PANEL)], foreground=[('readonly', FG)])
    s.configure('TNotebook', background=BG, borderwidth=0)
    s.configure('TNotebook.Tab', padding=(20, 11), background=PANEL, foreground=MUTED)
    s.map('TNotebook.Tab', background=[('selected', '#344039')], foreground=[('selected', FG)])
    root.option_add('*TCombobox*Listbox.background', PANEL)
    root.option_add('*TCombobox*Listbox.foreground', FG)

class Page(ttk.Frame):
    def title(self, value): pass
    def geometry(self, value): pass
    def minsize(self, *args): pass
    def protocol(self, *args): pass

class Bridge(launcher.App):
    def __init__(self, page):
        self.mode = 'bridge'
        super().__init__(page)
        self.log.configure(bg=PANEL, fg=FG, insertbackground=FG, relief='flat', borderwidth=0, font=('Consolas', 10))
    def diagnostics(self):
        if self.thread and self.thread.is_alive():
            messagebox.showinfo('Stop bridge first', 'Stop the bridge before running diagnostics.')
            return
        self.mode = 'diagnostics'
        self.start()
    def worker(self, name, device_id):
        if self.mode != 'diagnostics':
            return super().worker(name, device_id)
        try:
            ok = launcher.backend.diagnose()
            launcher.logging.info('Dependency/audio checks passed; BLE not tested.' if ok else 'Diagnostics failed.')
        except Exception as exc:
            launcher.logging.error('Diagnostics error: %s', exc)
        finally:
            self.mode = 'bridge'

class Workbench:
    def __init__(self, root):
        self.root = root
        theme(root)
        root.title('RotaryDeck')
        root.geometry('1160x780')
        root.minsize(1000, 700)
        assets = Path(__file__).parent / 'assets'
        self.logo = tk.PhotoImage(file=str(assets / 'rotarydeck.png'))
        root.iconphoto(True, self.logo)
        if os.name == 'nt': root.iconbitmap(str(assets / 'rotarydeck.ico'))
        header = ttk.Frame(root, padding=(24, 16))
        header.pack(fill='x')
        self.small_logo = self.logo.subsample(4, 4)
        ttk.Label(header, image=self.small_logo).pack(side='left', padx=(0, 14))
        ttk.Label(header, text='RotaryDeck', font=('Segoe UI', 22, 'bold')).pack(side='left')
        ttk.Label(header, text='COMPANION / CONTROL / TOOLS', foreground=MUTED).pack(side='right')
        tabs = ttk.Notebook(root)
        tabs.pack(fill='both', expand=True, padx=20, pady=(0, 18))
        companion, editor_page, tools = [Page(tabs) for _ in range(3)]
        for page, title in [(companion, 'Companion'), (editor_page, 'Apps & Actions'), (tools, 'Tools')]:
            tabs.add(page, text=title)
        self.bridge = Bridge(companion)
        self.editor = profile_editor.Editor(editor_page)
        area = ttk.Frame(tools, padding=28)
        area.pack(fill='both', expand=True)
        ttk.Label(area, text='Utilities', font=('Segoe UI', 22, 'bold')).pack(anchor='w', pady=(0, 16))
        ttk.Button(area, text='Check dependencies & audio', command=self.bridge.diagnostics).pack(anchor='w', pady=8)
        ttk.Label(area, text='Results appear in the Companion log. Stop the bridge first.', foreground=MUTED).pack(anchor='w')
        ttk.Button(area, text='Verify / apply reconnect patch', command=self.patch).pack(anchor='w', pady=(26, 8))
        ttk.Label(area, text='Select the installed BleKeyboard.cpp. Exact fingerprints are required. A backup is created before changes. Rebuild/upload firmware afterward.', wraplength=800, foreground=MUTED).pack(anchor='w')
        ttk.Label(area, text='No external BAT files or Python installation needed for the EXE. Profile editing is local; deck sync remains unavailable. No firmware flashing is performed.', wraplength=800, foreground=MUTED).pack(anchor='w', pady=30)
        root.protocol('WM_DELETE_WINDOW', self.close)

    def patch(self):
        selected = filedialog.askopenfilename(parent=self.root, title='Select installed BleKeyboard.cpp', filetypes=[('BleKeyboard.cpp', 'BleKeyboard.cpp')])
        if not selected: return
        temp = None
        try:
            target = Path(selected).resolve()
            if target.name != 'BleKeyboard.cpp': raise ValueError('Select installed BleKeyboard.cpp.')
            header = target.with_name('BleKeyboard.h')
            if patcher.blob_sha(header.read_text(encoding='utf-8-sig')) != patcher.HEADER:
                raise ValueError('Header fingerprint differs. No change made.')
            original = target.read_bytes()
            source = original.decode('utf-8-sig').replace(chr(13) + chr(10), chr(10))
            updated = patcher.transformed(source)
            if updated == source:
                messagebox.showinfo('Verified', 'The known reconnect patch is already installed.')
                return
            question = chr(10).join(['Modify this exact file?', str(target), '', 'Close Arduino IDE first. A backup will be kept. No firmware is uploaded.'])
            if not messagebox.askyesno('Apply library patch?', question): return
            if target.read_bytes() != original: raise ValueError('File changed during review. Try again.')
            backup = target.with_name(target.name + '.before-rotarydeck-' + datetime.now().strftime('%Y%m%d-%H%M%S-%f') + '.bak')
            with backup.open('xb') as output: output.write(original)
            fd, name = tempfile.mkstemp(prefix='.rotarydeck-', dir=target.parent)
            temp = Path(name)
            with os.fdopen(fd, 'w', encoding='utf-8', newline=chr(10)) as output:
                output.write(updated)
                output.flush()
                os.fsync(output.fileno())
            os.replace(temp, target)
            messagebox.showinfo('Patch applied', chr(10).join(['Backup: ' + str(backup), 'Rebuild/upload from Arduino IDE to update the deck.']))
        except (OSError, ValueError, RuntimeError, UnicodeError) as exc:
            messagebox.showerror('No patch completed', str(exc))
        finally:
            if temp is not None and temp.exists(): temp.unlink()

    def close(self):
        if not self.editor.discard(): return
        self.bridge.stop()
        self.finish_close()

    def finish_close(self):
        if self.bridge.thread is not None and self.bridge.thread.is_alive():
            self.root.after(100, self.finish_close)
        else: self.root.destroy()

def self_test():
    launcher.self_test()
    profile_editor.load_profile(Path(profile_editor.__file__).parent / 'profiles' / 'default.json')
    try: patcher.transformed('// unknown version')
    except RuntimeError: pass
    else: raise AssertionError('Patcher guard failed')
    root = tk.Tk()
    root.withdraw()
    app = Workbench(root)
    root.update()
    assert len(app.editor.rows['apps']) == 6
    assert len(app.editor.rows['actions']) == 6
    root.destroy()

if __name__ == '__main__':
    if '--self-test' in sys.argv: self_test()
    else:
        root = tk.Tk()
        Workbench(root)
        root.mainloop()
