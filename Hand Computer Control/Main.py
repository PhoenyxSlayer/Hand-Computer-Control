from tensorflow.keras.models import load_model as lm
import MouseControl as mouse
import multiprocessing as mp
import numpy as np
import time
import cv2
import os
import math
import HandDetection

camW, camH = 640, 480
imgR = 100

cap = cv2.VideoCapture(0)
cap.set(3, camW)
cap.set(4, camH)

detector = HandDetection
pTime = 0

def detection(pipe):
    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        img = detector.findHands(img)
        lmlist = detector.findPos(img)

        pipe.send((img, lmlist))

def main():
    global pTime
    key = -1
    p_con, c_con = mp.Pipe()
    detection_process = mp.Process(target=detection, args=(c_con,))
    detection_process.start()
    model = lm(os.path.join('CNN', 'Models', 'Model.h5'))

    try:
        while key == -1:
            if p_con.poll():
                img, lmlist = p_con.recv()
                image = cv2.resize(img, (100,100))
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

                if len(lmlist) != 0:
                    data = model.predict(np.expand_dims(image/255, 0))[0]
                    fist, ok, one, palm, thumb = data[0], data[1], data[2], data[3], data[4]

                    pointerTip = lmlist[8]
                    thumbTip = lmlist[4]
                    thumbX, thumbY = thumbTip[1:]
                    pointerX, pointerY = pointerTip[1:]
                    
                    mouse.controlMouse(thumbX, thumbY, pointerX, pointerY, imgR, camW, camH, data, confidence=.8)

                    if fist > .8:
                        cv2.putText(img, f'fist: {math.floor(fist*100)}%', (320, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)
                    elif ok > .8:
                        cv2.putText(img, f'ok: {math.floor(ok*100)}%', (320, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)
                    elif one > .8:
                        cv2.putText(img, f'one: {math.floor(one*100)}%', (320, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)
                    elif palm > .8:
                        cv2.putText(img, f'palm: {math.floor(palm*100)}%', (320, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)
                    elif thumb > .8:
                        cv2.putText(img, f'thumb: {math.floor(thumb*100)}%', (320, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)
                    #if distY or dist
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

if __name__ == "__main__":
    main()