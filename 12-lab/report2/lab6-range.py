import win32gui
import win32ui
import win32con
import win32api
def screen_shot(left, top, width, height):
    hdesktop = win32gui.GetDesktopWindow()
    desktop_dc = win32gui.GetWindowDC(hdesktop)
    img_dc = win32ui.CreateDCFromHandle(desktop_dc)
    mem_dc = img_dc.CreateCompatibleDC()
    screenshot = win32ui.CreateBitmap()
    screenshot.CreateCompatibleBitmap(img_dc, width, height)
    mem_dc.SelectObject(screenshot)
    mem_dc.BitBlt((0, 0), (width, height), img_dc, (left, top), win32con.SRCCOPY)
    screenshot.SaveBitmapFile(mem_dc, './screen-range.jpg')
    mem_dc.DeleteDC()
    win32gui.DeleteObject(screenshot.GetHandle())
if __name__ == '__main__':
    left = int(input("请输入要截取区域的左上角横坐标："))
    top = int(input("请输入要截取区域的左上角纵坐标："))
    width = int(input("请输入要截取区域的宽度："))
    height = int(input("请输入要截取区域的高度："))
    screen_shot(left, top, width, height)
