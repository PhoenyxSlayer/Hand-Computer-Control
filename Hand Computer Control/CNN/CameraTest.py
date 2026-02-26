from tensorflow.keras.models import load_model
import cv2
import numpy as np
import os
import sys
import math

if len(sys.argv) <= 1:
    print("Opening webcam...")
    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
if not camera.isOpened():
    print("ERROR: Cannot open camera!")
    exit(1)

model = load_model(os.path.join('CNN', 'Models', 'Model.h5'))

windowName = "webcam"
cv2.namedWindow(windowName)

i = 0
j = 3000
key = -1
while key == -1:
    ret, frame = camera.read()

    frame = cv2.flip(frame, 1)
    test = cv2.resize(frame, (100,100))
    test = cv2.cvtColor(test, cv2.COLOR_BGR2RGB)
    print(test.shape)
    data = model.predict(np.expand_dims(test/255, 0))[0]
    if data[0] > .8:
        cv2.putText(frame, f'fist: {math.floor(data[0]*100)}%', (20, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
    elif data[1] > .8:
        cv2.putText(frame, f'ok: {math.floor(data[1]*100)}%', (20, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
    elif data[2] > .8:
        cv2.putText(frame, f'one: {math.floor(data[2]*100)}%', (20, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
    elif data[3] > .8:
        cv2.putText(frame, f'palm: {math.floor(data[3]*100)}%', (20, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
    elif data[4] > .8:
        cv2.putText(frame, f'thumb: {math.floor(data[4]*100)}%', (20, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
    '''elif data[5] > .8:
        cv2.putText(frame, f'thumb: {data[5]}', (20, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
    elif data[6] > .8:
        cv2.putText(frame, f'two: {data[6]}', (20, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)'''
    
    key = cv2.waitKey(1)
    cv2.imshow(windowName, frame)
camera.release()
cv2.destroyAllWindows()
print(model)