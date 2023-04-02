import pyautogui as mouse
import tkinter as tk
import math
import numpy as np
from pynput.keyboard import Key, Controller
import time

keyboard = Controller()

def controlMouse(thumbX, thumbY, pointerX, pointerY, frameR, camW, camH, data, confidence):
    mouse.FAILSAFE = False
    smoothing = 7
    w, h = mouse.size()
    x = (pointerX + thumbX)/2
    y = (pointerY + thumbY)/2
    dist = math.floor(math.sqrt((abs(pointerX - thumbX)) + (abs(pointerY - thumbY))))

    mouseX = np.interp(x, (frameR, camW - frameR), (0, w))
    mouseY = np.interp(y, (frameR, camH - frameR), (0, h))
    
    mouse.moveTo(mouseX, mouseY)
    print(mouse.position())
    print("(X, Y): (",x , ", ",y, ") distance: ", dist)

    fist = data[0]
    ok = data[1]
    one = data[2]
    palm = data[3]
    thumb = data[4]

    if fist > confidence:
        keyboard.press(Key.media_volume_down)
        keyboard.release(Key.media_volume_down)
        time.sleep(0.5)

    if (ok > confidence and dist <= 5) or dist <= 5:
        mouse.click()

    if one > confidence:
        mouse.hotkey('alt', 'right')
        time.sleep(1)
    
    if palm > confidence:
        keyboard.press(Key.media_volume_up)
        keyboard.release(Key.media_volume_up)
        time.sleep(0.5)
    
    if thumb > confidence:
        mouse.hotkey('alt', 'left')
        time.sleep(1)

    #if x <  and x
    #mouse.dragTo(x, y, button='left')