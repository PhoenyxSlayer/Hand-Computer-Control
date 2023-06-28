from tensorflow.keras.models import load_model as lm
import ComputerControl as mouse
import multiprocessing as mp
import numpy as np
import time
import cv2
import os
import HandDetection
import math
import GUI

camW, camH = 640, 480
imgR = 100

cap = cv2.VideoCapture(0)
cap.set(3, camW)
cap.set(4, camH)

detector = HandDetection
pTime = 0

isFist = False
isOk = False
isOne = False
isPalm = False
isThumb = False
windowKilled = False

def detection(pipe):
    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        img = detector.findHands(img)
        lmlist = np.array(detector.findPos(img))

        pipe.send((img, lmlist))

def functionToggle():
    global pTime
    key = -1
    p_con, c_con = mp.Pipe()
    detection_process = mp.Process(target=detection, args=(c_con,))
    detection_process.start()
    model = lm(os.path.join('CNN', 'Models', 'Model.h5'))
    global isFist
    global isOk
    global isOne
    global isPalm
    global isThumb
    global windowKilled

    try:
        while not(isFist or isOk or isOne or isPalm or isThumb) or key == -1:
            if p_con.poll():
                img, lmlist = p_con.recv()
                image = cv2.resize(img, (100,100))
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

                if len(lmlist) != 0:
                    data = model.predict(np.expand_dims(image/255, 0))[0]
                    ok, one, palm, thumb = data[1], data[2], data[3], data[4]

                    if ok > .8:
                        isOk = True
                        break
                    elif one > .8:
                        isOne = True
                        break
                    elif palm > .8:
                        isPalm = True
                        break
                    elif thumb > .8:
                        isThumb = True
                        break
                else:
                    data = model.predict(np.expand_dims(image/255,0))[0]
                    fist = data[0]

                    if fist > .8:
                        isFist = True
                        GUI.killWindow()
                        break

                cv2.rectangle(img, (imgR, imgR), (camW - imgR, camH - imgR), (0, 255, 0), 2)
                cTime = time.time()
                fps = 1/(cTime-pTime)
                pTime = cTime
                cv2.putText(img, f'FPS:{int(fps)}', (20, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
                cv2.imshow("TEST", img)
                key = cv2.waitKey(1)

        print("Fist: ", isFist)
        print("Ok: ", isOk)
        print("One: ", isOne)
        print("Palm: ", isPalm)
        print("Thumb: ", isThumb)

    finally:
        detection_process.terminate()
        cap.release()
        cv2.destroyAllWindows()
        detection_process.join()
        p_con.close()

    if not windowKilled:
        windowKilled = True
        GUI.killWindow
    
    handTracking()

def handTracking():
    global pTime
    key = -1
    p_con, c_con = mp.Pipe()
    detection_process = mp.Process(target=detection, args=(c_con,))
    detection_process.start()
    global isFist
    global isOk
    global isOne
    global isPalm
    global isThumb

    try:
        while key == -1:
            if p_con.poll():
                img, lmlist = p_con.recv()

                if len(lmlist) != 0:
                    thumbTip = lmlist[4]
                    pointerTip = lmlist[8]
                    middleTip = lmlist[12]
                    ringTip = lmlist[16]
                    pinkyTip = lmlist[20]
                    thumbX, thumbY = thumbTip[1:]
                    pointerX, pointerY = pointerTip[1:]
                    middleX, middleY = middleTip[1:]
                    ringX, ringY = ringTip[1:]
                    pinkyX, pinkyY = pinkyTip[1:]

                    dist = math.floor(math.sqrt((abs(pinkyX - thumbX)) + (abs(pinkyY - thumbY))))
                    midDist = math.floor(math.sqrt((abs(middleX - thumbX)) + (abs(middleY - thumbY))))
                    rDist = math.floor(math.sqrt((abs(ringX - thumbX)) + (abs(ringY - thumbY))))
                   
                    if dist <= 6:
                        break

                    if midDist <= 6 and rDist <= 6:
                        exit(0)
                    
                    if isOk:
                        mouse.mouseControl(thumbX, thumbY, pointerX, pointerY, middleX, middleY, ringX, ringY, imgR, camW, camH)
                    elif isPalm or isFist:
                        mouse.volumeControl(thumbX, thumbY, pointerX, pointerY, isPalm, isFist)
                    elif isThumb or isOne:
                        mouse.tabControl(thumbX, thumbY, pointerX, pointerY, isThumb, isOne)

                if isOk:
                    cv2.putText(img, f'Mouse Control', (320, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)
                elif isOne:
                    cv2.putText(img, f'Tab Forward', (320, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)
                elif isPalm:
                    cv2.putText(img, f'Volume Control', (320, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)
                elif isThumb:
                    cv2.putText(img, f'Tab Back', (320, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)

                cv2.rectangle(img, (imgR, imgR), (camW - imgR, camH - imgR), (0, 255, 0), 2)
                cTime = time.time()
                fps = 1/(cTime-pTime)
                pTime = cTime
                cv2.putText(img, f'FPS:{int(fps)}', (20, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
                cv2.imshow("TEST", img)
                key = cv2.waitKey(1)

    finally:
        detection_process.terminate()
        cap.release()
        cv2.destroyAllWindows()
        detection_process.join()
        p_con.close()

    isFist = False
    isOk = False
    isOne = False
    isPalm = False
    isThumb = False
    
    functionToggle()

if __name__ == "__main__":
    GUI.buildGui()