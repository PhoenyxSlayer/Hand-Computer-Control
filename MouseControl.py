import pyautogui as mouse
import tkinter as tk
import math
import numpy as np

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

    isFist = False
    print(isFist)
    if fist > confidence:
        isFist = True

    if (ok > confidence and dist <= 5) or dist <= 5:
        mouse.click()

    if one > confidence:
        return
    
    if palm > confidence:
        return
    
    if thumb > confidence:
        mouse.hotkey('alt', 'left')
        
    print(isFist)

    #if x <  and x
    #mouse.dragTo(x, y, button='left')