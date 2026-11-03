import sys
sys.coinit_flags = 0
import asyncio
import importlib
import logging
import queue
import threading
from argparse import Namespace
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
import rotary_deck_sync as backend

class LogHandler(logging.Handler):
    def __init__(self, events):
        super().__init__()
        self.events = events
    def emit(self, record):
        try:
            self.events.put_nowait(self.format(record))
        except queue.Full:
            pass

class App:
    def __init__(self, root):
        self.root = root
        self.thread = None
        self.loop = self.task = None
        self.stop_requested = threading.Event()
        self.events = queue.Queue(maxsize=500)
        self.closing = False
        root.title('RotaryDeck Companion - preview')
        root.geometry('800x540')
        panel = ttk.Frame(root, padding=16)
        panel.pack(fill='both', expand=True)
        ttk.Label(panel, text='RotaryDeck Companion', font=('Segoe UI', 20)).pack(anchor='w')
        ttk.Label(panel, text='v2.2 clock / media / volume bridge. Profile sync not included.').pack(anchor='w', pady=8)
        self.name = tk.StringVar(value='Rotary Deck')
        self.device_id = tk.StringVar()
        for label, var in [('Paired device name', self.name), ('Exact device ID (optional)', self.device_id)]:
            ttk.Label(panel, text=label).pack(anchor='w')
            ttk.Entry(panel, textvariable=var).pack(fill='x', pady=4)
        bar = ttk.Frame(panel)
        bar.pack(fill='x', pady=10)
        self.start_btn = ttk.Button(bar, text='Start bridge', command=self.start)
        self.start_btn.pack(side='left')
        self.stop_btn = ttk.Button(bar, text='Stop', command=self.stop, state='disabled')
        self.stop_btn.pack(side='left', padx=8)
        self.status = tk.StringVar(value='Stopped - no connection claimed')
        ttk.Label(panel, textvariable=self.status).pack(anchor='w')
        self.log = ScrolledText(panel, state='disabled', height=15)
        self.log.pack(fill='both', expand=True, pady=8)
        ttk.Label(panel, text='Stop other companion instances first. Logs stay in memory and may contain private device/media details.', wraplength=740).pack(anchor='w')
        handler = LogHandler(self.events)
        handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
        logging.getLogger().addHandler(handler)
        logging.getLogger().setLevel(logging.INFO)
        root.protocol('WM_DELETE_WINDOW', self.close)
        self.poll()

    def start(self):
        if self.thread and self.thread.is_alive():
            return
        name, device_id = self.name.get().strip(), self.device_id.get().strip()
        if not name and not device_id:
            messagebox.showerror('Device required', 'Enter a paired device name or exact device ID.')
            return
        self.stop_requested.clear()
        self.status.set('Bridge starting - connection not yet verified')
        self.start_btn.configure(state='disabled')
        self.stop_btn.configure(state='normal')
        self.thread = threading.Thread(target=self.worker, args=(name, device_id), daemon=True)
        self.thread.start()

    def worker(self, name, device_id):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        task = loop.create_task(backend.run(Namespace(device_name=name, device_id=device_id or None, list=False, diagnose=False)))
        self.loop, self.task = loop, task
        if self.stop_requested.is_set():
            task.cancel()
        try:
            loop.run_until_complete(task)
        except asyncio.CancelledError:
            pass
        except (Exception, SystemExit) as exc:
            logging.error('%s: %s', type(exc).__name__, exc)
        finally:
            for pending in asyncio.all_tasks(loop):
                pending.cancel()
            pending = asyncio.all_tasks(loop)
            if pending:
                loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
            loop.run_until_complete(loop.shutdown_asyncgens())
            self.loop = self.task = None
            loop.close()

    def stop(self):
        self.stop_requested.set()
        loop, task = self.loop, self.task
        if loop and task:
            try:
                loop.call_soon_threadsafe(task.cancel)
            except RuntimeError:
                pass
        self.status.set('Stopping...')

    def poll(self):
        for _ in range(100):
            try:
                text = self.events.get_nowait()
            except queue.Empty:
                break
            self.log.configure(state='normal')
            self.log.insert('end', text + '\n')
            if int(self.log.index('end-1c').split('.')[0]) > 600:
                self.log.delete('1.0', '101.0')
            self.log.see('end')
            self.log.configure(state='disabled')
        alive = self.thread is not None and self.thread.is_alive()
        if self.thread is not None and not alive:
            self.start_btn.configure(state='normal')
            self.stop_btn.configure(state='disabled')
            self.status.set('Stopped - inspect session log for errors')
        if self.closing and not alive:
            self.root.destroy()
            return
        self.root.after(100, self.poll)

    def close(self):
        self.closing = True
        self.stop()

def self_test():
    for module in ['winrt.windows.foundation', 'winrt.windows.foundation.collections', 'winrt.windows.devices.bluetooth', 'winrt.windows.devices.enumeration', 'winrt.windows.devices.bluetooth.genericattributeprofile', 'winrt.windows.storage.streams', 'winrt.windows.media.control', 'pycaw.pycaw']:
        importlib.import_module(module)
    assert backend.volume_packet(0, 50, False) == bytes((4, 0, 50, 0))
    root = tk.Tk()
    root.withdraw()
    root.update()
    root.destroy()

if __name__ == '__main__':
    if '--self-test' in sys.argv:
        self_test()
    else:
        root = tk.Tk()
        App(root)
        root.mainloop()
