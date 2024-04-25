import cv2
import numpy as np
import HandTrackingModule as htm
import pyautogui

# variables here
wCam, hCam = 640, 480
frame_requction = 100

detector = htm.HandDetector(max_hand=1, detection_conf=0.5)

cap = cv2.VideoCapture(0)

cap.set(3, wCam)
cap.set(4, hCam)
wScr, hScr = pyautogui.size()
print(wScr, hScr)

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img)

    cv2.rectangle(img, (frame_requction,frame_requction),(wCam - frame_requction, hCam - frame_requction), (255,0,255),2)
    # Find hands landmarks
    if len(lmList)!= 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

        fingers = detector.detectFingers(img)
        print(fingers)

        if fingers is not None and fingers[1] == 1 and fingers[2] == 0:
            pos1 = np.interp(x1, [frame_requction, wCam - frame_requction], [0, wScr])
            pos2 = np.interp(y1, [frame_requction, hCam - frame_requction], [0, hScr])

            # Move the mouse cursor smoothly
            pyautogui.moveTo(wScr - pos1, pos2, duration=0.1)
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)

        if fingers is not None and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0:
            dist = detector.find_distance(img, lmList, 8,12)
            print(dist)
            if dist < 30:
                pyautogui.click()
                print("Clicked")

        if fingers is not None and fingers[1] == 1 and fingers[0] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
            dist = detector.find_distance(img, lmList, 4,8)
            print(f"Thumb to index finger distance: {dist}")
            if dist <= 50:
                print("Right clicked")
                pyautogui.rightClick()

    cv2.imshow("Image", img)
    cv2.waitKey(1)

cap.release()
cv2.destroyAllWindows()