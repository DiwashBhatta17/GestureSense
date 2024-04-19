import cv2
import numpy as np
import HandTrackingModule as htm
#import autopy

wCam, hCam = 640, 480
detector = htm.HandDetector()


cap = cv2.VideoCapture(0)

cap.set(3, wCam)
cap.set(4, hCam)
while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img)

    heads = detector.detectFingers(img)


    #Find hands landmaks
    if len(lmList)!=0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

        print(x1, y1, x2, y2)
        print(heads)

    cv2.imshow("Image", img)
    cv2.waitKey(1)

cap.release()
cv2.destroyAllWindows()

