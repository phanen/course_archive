from datetime import datetime
import win32gui
import win32ui
import win32con
import win32api

def screen_shot():
    hdesktop = win32gui.GetDesktopWindow()
    # 获得显示器尺寸
    width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
    height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
    left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
    top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)
    desktop_dc = win32gui.GetWindowDC(hdesktop)
    img_dc = win32ui.CreateDCFromHandle(desktop_dc)
    mem_dc = img_dc.CreateCompatibleDC()
    screenshot = win32ui.CreateBitmap()
    screenshot.CreateCompatibleBitmap(img_dc, width, height)
    mem_dc.SelectObject(screenshot)
    mem_dc.BitBlt((0, 0), (width, height), img_dc, (left, top),win32con.SRCCOPY)
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"./screen_{timestamp}.jpg"
    screenshot.SaveBitmapFile(mem_dc, filename)
    mem_dc.DeleteDC()
    win32gui.DeleteObject(screenshot.GetHandle())

if __name__ == '__main__':
    screen_shot()
