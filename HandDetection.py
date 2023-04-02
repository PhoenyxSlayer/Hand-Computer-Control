import cv2
import mediapipe as mp
import numpy as np

results = None
mpHands = mp.solutions.hands
hands = mpHands.Hands(static_image_mode = False, max_num_hands = 1, min_detection_confidence = 0.5, min_tracking_confidence =0.5)
mpDraw = mp.solutions.drawing_utils

def findHands(img, draw = True):
    global results, hands, mpDraw, mpHands
    results = hands.process(img)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            if draw:
                mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
    return img

def findPos(img, handNo = 0, draw = True):
    lmlist = []
    if results.multi_hand_landmarks:
        myHand = results.multi_hand_landmarks[handNo]
        for id, lm in enumerate(myHand.landmark):
            h, w, c = img.shape
            cx, cy = int(lm.x*w), int(lm.y*h)
            lmlist.append([id, cx, cy])
            if draw:
                cv2.circle(img, (cx, cy), 3, (255,0,255), cv2.FILLED)
    return np.array(lmlist)
