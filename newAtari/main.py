import gym
import keyboard
import numpy as np
import time


def preprocess(img):
    img_temp = img.mean(axis=2)
    x = -1
    y = -1
    if len(np.where((img_temp[100:189, 8:152]) != 0)[0]) != 0:
        x = np.where((img_temp[100:189, 8:152]) != 0)[0][0]
        y = np.where((img_temp[100:189, 8:152]) != 0)[1][0]
    if len(np.where((img_temp[193:, 8:152]) != 0)[0]) != 0:
        x = -2
        y = -2
    p = int(np.where(img_temp[191:193, 8:152])[1].mean() - 7.5)
    # return img_temp
    return (x, y, p)


def abc(x):
    global action
    if x.event_type == "down" and x.name == 's':
        action = 0
    elif x.event_type == "down" and x.name == 'w':
        action = 1
    elif x.event_type == "down" and x.name == 'd':
        action = 2
    elif x.event_type == "down" and x.name == 'a':
        action = 3
    elif x.event_type == "down" and (action == 4 or x.name == 'p'):
        action = 4

    elif action != 4:
        action = 0


def main():
    keyboard.hook(abc)
    total_reward = 0
    for j in range(1000):
        while action == 4:
            time.sleep(0.1)
        next_state, reward, done, _ = env.step(action)
        print(_)
        total_reward += reward
        (x2, y2, p2) = preprocess(next_state)
        print(action, total_reward, done, x2, y2, p2)
        if done:
            env.reset()
            total_reward = 0
            break


if __name__ == '__main__':
    env = gym.make('ALE/SpaceInvaders-v5', render_mode="human")
    state = env.reset()
    action = 0
    main()
