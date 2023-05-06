import cv2
import numpy as np
import sys

def main():
    if len(sys.argv) <= 1:
        print("Opening webcam...")
        camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not camera.isOpened():
        print("ERROR: Cannot open camera!")
        exit(1)

    windowName = "webcam"
    cv2.namedWindow(windowName)

    i = 0
    j = 3000
    key = -1
    while i < 1:
        ret, frame = camera.read()

        frame = cv2.flip(frame, 1)

        out_filename = "Beans" + str(i) + ".png"
        directory = "C:\\Users\\Phoenyx\\Downloads"+"/"+out_filename

        cv2.imshow(windowName, frame)
        #key = cv2.waitKey(1)
        cv2.imwrite(directory, frame)
        print(i)
        j+=1
        i+=1
    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()