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
    # 循环监听键盘事件，直到按下 Enter 键后退出循环
    while True:
        if keyboard.is_pressed('esc'):
            break
    recorded = [e.name for e in recorded]
    print("The recorder: ", recorded)

if __name__ == '__main__':
    recorder()
