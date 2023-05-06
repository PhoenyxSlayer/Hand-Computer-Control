import pyautogui as mouse
import math
import numpy as np
from pynput.keyboard import Key, Controller
keyboard = Controller()

def mouseControl(thumbX, thumbY, pointerX, pointerY, middleX, middleY, ringX, ringY, frameR, camW, camH):
    mouse.FAILSAFE = False
    w, h = mouse.size()
    x = (pointerX + thumbX)/2
    y = (pointerY + thumbY)/2
    dist = math.floor(math.sqrt((abs(pointerX - thumbX)) + (abs(pointerY - thumbY))))
    midDist = math.floor(math.sqrt((abs(middleX - thumbX)) + (abs(middleY - thumbY))))
    rDist = math.floor(math.sqrt((abs(ringX - thumbX)) + (abs(ringY - thumbY))))

    mouseX = np.interp(x, (frameR, camW - frameR), (0, w))
    mouseY = np.interp(y, (frameR, camH - frameR), (0, h))
    
    mouse.moveTo(mouseX, mouseY)

    if dist <= 6:
        mouse.click()

    if dist <= 7 and midDist <= 7:
        mouse.doubleClick()

    if midDist <= 6:
        mouse.dragTo(mouseX, mouseY)

    if rDist <= 6:
        mouse.rightClick()

def volumeControl(thumbX, thumbY, pointerX, pointerY, palm, fist):
    dist = math.floor(math.sqrt((abs(pointerX - thumbX)) + (abs(pointerY - thumbY))))

    #Volume up
    if palm and dist <= 5:
        keyboard.press(Key.media_volume_up)
        keyboard.release(Key.media_volume_up)
    
    #Volume down
    if fist and dist <= 5:
        keyboard.press(Key.media_volume_down)
        keyboard.release(Key.media_volume_down)
    
def tabControl(thumbX, thumbY, pointerX, pointerY, thumb, one):
    dist = math.floor(math.sqrt((abs(pointerX - thumbX)) + (abs(pointerY - thumbY))))

    #Tab back
    if thumb and dist <= 5:
        mouse.hotkey('alt', 'left')

    #Tab forward
    if one and dist <= 5:
        mouse.hotkey('alt', 'right')