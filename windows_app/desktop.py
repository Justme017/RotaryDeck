import sys
sys.coinit_flags = 0
import os
import json
import queue
import webbrowser
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
import workbench

PROJECT = 'https://github.com/Justme017/RotaryDeck'
PUBLISHER = 'Shubham Mehta'
VERSION = '0.3.0-preview'
RUN_KEY = r'Software\Microsoft\Windows\CurrentVersion\Run'
RUN_NAME = 'RotaryDeck Companion'
BG, PANEL, FG, MUTED, ACCENT = '#0c1423', '#162238', '#edf3fc', '#a6b6cd', '#58d9e8'
workbench.BG, workbench.PANEL, workbench.FG, workbench.MUTED = BG, PANEL, FG, MUTED
HELP = {
    'Quick start': 'Pair Rotary Deck in Windows Bluetooth settings. Close old companion processes. In Companion, select its paired name or exact device ID and click Start bridge. Read the log for discovery and Sync active; Starting is not a connected indicator. Keep the app running for clock/media/output-volume telemetry.',
    'Uses & limits': 'Companion supplies clock, media title/state and Windows default-output volume/mute. Apps & Actions edits six Apps and six Actions locally. Tools provides dependency/audio diagnostics and a guarded reconnect patch. This preview does not sync edited profiles to the deck, flash firmware or implement arbitrary app/shortcut execution. v2.2 deck app shortcuts may require your existing PC bindings.',
    'Profiles & backups': 'Edit labels (maximum 16 characters), types and targets. Load/import/save/restore never runs actions. Save as preserves an imported original. Overwriting JSON creates timestamped backups beside the file, retaining ten per filename. Recover by importing a backup and using Save as. Restore default loads the bundled example, not a saved backup. Suggested path: %APPDATA%/RotaryDeck/profiles.',
    'PC tests': 'Only URL and folder Test on PC actions are implemented, with confirmation. URLs must be absolute HTTP/HTTPS without credentials or whitespace. Folders must be existing absolute paths. Other listed types are editable data, not working execution in this preview. Local profile changes do not change the deck.',
    'Tools': 'Stop the bridge before dependency/audio diagnostics; results appear in Companion and do not prove Bluetooth connection. Reconnect patching is advanced: close Arduino IDE, select installed BleKeyboard.cpp with its matching header, and review the exact target. Unknown fingerprints are refused and a backup precedes replacement. Rebuild/upload separately afterward. Do not reapply unnecessarily to a working setup.',
    'Tray & startup': 'Closing the window hides it only after a tray icon has been created. Use the tray menu to Open, Start/Stop or Exit. Exit checks for unsaved profile edits and stops the bridge. Settings can enable startup for an installed EXE. Startup opens quietly in the tray and starts telemetry with the last saved device selection. Windows Startup Apps can also disable it. Installation offers a startup checkbox; uninstall removes this app startup entry. Profiles are retained.',
    'FAQ & troubleshooting': 'The EXE needs no separate Python/BAT files. Basic HID media controls are separate from telemetry. Sync is disabled because end-to-end profile transfer is not enabled; repeated pairing/patching does not fix it. No deck: check pairing/name or exact ID and stop old processes. No volume: run diagnostics and check the default output endpoint. No title: not every application exposes a compatible Windows media session. This build targets Windows x64.',
    'Firmware & privacy': 'USB updates are not enabled until a compiled XIAO ESP32-S3 package with validated offsets and integrity information is available. The source ZIP is not flashable firmware. Do not unplug during any future flash. Logs may show device IDs/media titles/paths; redact before sharing. Profiles contain local targets. Device-selection preferences are saved under %APPDATA%/RotaryDeck. Publisher metadata is not code signing: this preview is unsigned and Windows may warn.'
}

def startup_enabled():
    import winreg
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, RUN_KEY) as key:
            return bool(winreg.QueryValueEx(key, RUN_NAME)[0])
    except FileNotFoundError: return False

def set_startup(enabled):
    import winreg
    if enabled:
        expected = Path(os.environ['LOCALAPPDATA']) / 'Programs' / 'RotaryDeck'
        if not getattr(sys, 'frozen', False) or Path(sys.executable).resolve().parent != expected.resolve():
            raise ValueError('Install RotaryDeck first so startup points to a stable installed EXE.')
    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, RUN_KEY) as key:
        if enabled: winreg.SetValueEx(key, RUN_NAME, 0, winreg.REG_SZ, '"' + sys.executable + '" --background')
        else:
            try: winreg.DeleteValue(key, RUN_NAME)
            except FileNotFoundError: pass

class Desktop(workbench.Workbench):
    def __init__(self, root, use_tray=True):
        self.commands = queue.Queue()
        self.tray = None
        self.tray_ready = False
        self.notified = False
        self.exiting = False
        super().__init__(root)
        style = ttk.Style(root)
        style.map('TNotebook.Tab', background=[('selected', '#21394f')], foreground=[('selected', ACCENT)])
        style.configure('Accent.TButton', background=ACCENT, foreground=BG, padding=(18, 10))
        style.map('Accent.TButton', background=[('active', '#8ce8f2'), ('disabled', '#25364a')], foreground=[('disabled', MUTED)])
        self.bridge.start_btn.configure(style='Accent.TButton', command=self.start_bridge)
        self.preferences = Path(os.environ.get('APPDATA', str(Path.home()))) / 'RotaryDeck' / 'companion.json'
        try:
            settings = json.loads(self.preferences.read_text(encoding='utf-8'))
            self.bridge.name.set(str(settings.get('device_name', 'Rotary Deck')))
            self.bridge.device_id.set(str(settings.get('device_id', '')))
        except (OSError, ValueError, AttributeError): pass
        tabs = next(c for c in root.winfo_children() if isinstance(c, ttk.Notebook))
        page = ttk.Frame(tabs, padding=24)
        tabs.add(page, text='Help')
        ttk.Label(page, text='Help & answers', font=('Segoe UI', 20, 'bold')).pack(anchor='w')
        query = tk.StringVar()
        ttk.Entry(page, textvariable=query).pack(fill='x', pady=12)
        article = ScrolledText(page, wrap='word', bg=PANEL, fg=FG, relief='flat', padx=20, pady=16, font=('Segoe UI', 11))
        article.pack(fill='both', expand=True)
        article.tag_configure('heading', font=('Segoe UI', 16, 'bold'), foreground=ACCENT, spacing3=10)
        def render(*args):
            words = query.get().casefold().split()
            article.configure(state='normal')
            article.delete('1.0', 'end')
            for title, body in HELP.items():
                if all(w in (title + ' ' + body).casefold() for w in words):
                    article.insert('end', title + chr(10), 'heading')
                    article.insert('end', body + chr(10) * 3)
            if not article.get('1.0', 'end').strip(): article.insert('end', 'No matching topics.')
            article.configure(state='disabled')
        query.trace_add('write', render)
        render()
        root.bind('<F1>', lambda event: tabs.select(page))
        settings_page = ttk.Frame(tabs, padding=24)
        tabs.add(settings_page, text='Settings & About')
        ttk.Label(settings_page, text='RotaryDeck ' + VERSION, font=('Segoe UI', 20, 'bold')).pack(anchor='w')
        ttk.Label(settings_page, text='Publisher: ' + PUBLISHER + ' | Unsigned preview', foreground=MUTED).pack(anchor='w', pady=12)
        ttk.Button(settings_page, text='Visit GitHub project', command=lambda: webbrowser.open(PROJECT)).pack(anchor='w', pady=10)
        self.startup = tk.BooleanVar(value=startup_enabled() if os.name == 'nt' else False)
        ttk.Checkbutton(settings_page, text='Start with Windows (installed app only)', variable=self.startup, command=self.toggle_startup).pack(anchor='w', pady=12)
        ttk.Label(settings_page, text='Background startup starts the bridge using your saved device selection. Windows may still warn: publisher text is not a digital signature.', wraplength=800).pack(anchor='w', pady=10)
        ttk.Button(settings_page, text='Exit companion', command=self.exit_app).pack(anchor='w', pady=20)
        firmware = ttk.Frame(tabs, padding=24)
        tabs.add(firmware, text='Firmware')
        ttk.Label(firmware, text='USB firmware update', font=('Segoe UI', 20, 'bold')).pack(anchor='w')
        ttk.Label(firmware, text='Not enabled yet. No validated flashable firmware package is bundled. Your existing source ZIP cannot be flashed directly. This preview does not modify device firmware.', wraplength=800).pack(anchor='w', pady=20)
        ttk.Button(firmware, text='Update firmware - unavailable', state='disabled').pack(anchor='w')
        if use_tray: self.create_tray()
        root.after(100, self.poll_commands)

    def start_bridge(self):
        try:
            self.preferences.parent.mkdir(parents=True, exist_ok=True)
            temp = self.preferences.with_suffix('.tmp')
            temp.write_text(json.dumps({'device_name': self.bridge.name.get(), 'device_id': self.bridge.device_id.get()}), encoding='utf-8')
            os.replace(temp, self.preferences)
        except OSError as exc: workbench.launcher.logging.warning('Preferences not saved: %s', exc)
        self.bridge.start()

    def toggle_startup(self):
        try: set_startup(self.startup.get())
        except (OSError, ValueError) as exc:
            self.startup.set(startup_enabled())
            messagebox.showerror('Startup setting not changed', str(exc))

    def create_tray(self):
        try:
            import pystray
            from PIL import Image
            def command(name): return lambda icon, item: self.commands.put(name)
            menu = pystray.Menu(pystray.MenuItem('Open RotaryDeck', command('open'), default=True), pystray.MenuItem('Start bridge', command('start')), pystray.MenuItem('Stop bridge', command('stop')), pystray.MenuItem('Exit', command('exit')))
            self.tray = pystray.Icon('RotaryDeck', Image.open(Path(__file__).parent / 'assets' / 'rotarydeck.png').copy(), 'RotaryDeck Companion', menu)
            def ready(icon):
                icon.visible = True
                self.commands.put('ready')
            self.tray.run_detached(setup=ready)
        except Exception as exc:
            self.tray = None
            workbench.launcher.logging.error('Tray unavailable; window remains visible: %s', exc)

    def poll_commands(self):
        for _ in range(30):
            try: cmd = self.commands.get_nowait()
            except queue.Empty: break
            if cmd == 'ready':
                self.tray_ready = True
                if '--background' in sys.argv:
                    self.root.withdraw()
                    self.start_bridge()
            elif cmd == 'open':
                self.root.deiconify()
                self.root.lift()
            elif cmd == 'start': self.start_bridge()
            elif cmd == 'stop': self.bridge.stop()
            elif cmd == 'exit': self.exit_app()
        if not self.exiting: self.root.after(100, self.poll_commands)

    def close(self):
        if self.tray_ready and self.tray is not None:
            if not self.notified:
                messagebox.showinfo('Still running', 'RotaryDeck will stay in the system tray. Use its menu or Settings to Exit.')
                self.notified = True
            self.root.withdraw()
        else: self.exit_app()

    def exit_app(self):
        if not self.editor.discard(): return
        self.exiting = True
        if self.tray is not None: self.tray.stop()
        self.bridge.stop()
        self.finish_close()

def self_test():
    workbench.self_test()
    import pystray
    root = tk.Tk()
    root.withdraw()
    app = Desktop(root, use_tray=False)
    root.update()
    assert len(HELP) == 8
    root.destroy()

if __name__ == '__main__':
    if '--self-test' in sys.argv: self_test()
    else:
        import ctypes
        from ctypes import wintypes
        ctypes.windll.kernel32.CreateMutexW.argtypes = [ctypes.c_void_p, wintypes.BOOL, wintypes.LPCWSTR]
        ctypes.windll.kernel32.CreateMutexW.restype = wintypes.HANDLE
        ctypes.windll.kernel32.CloseHandle.argtypes = [wintypes.HANDLE]
        mutex = ctypes.windll.kernel32.CreateMutexW(None, False, 'Local' + chr(92) + 'RotaryDeckCompanion')
        if not mutex: raise ctypes.WinError()
        if ctypes.windll.kernel32.GetLastError() == 183:
            ctypes.windll.user32.MessageBoxW(None, 'RotaryDeck is already running. Open it from the system tray.', 'RotaryDeck', 0)
            raise SystemExit(0)
        try:
            root = tk.Tk()
            Desktop(root)
            root.mainloop()
        finally:
            if mutex: ctypes.windll.kernel32.CloseHandle(mutex)
