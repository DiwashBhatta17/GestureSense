import cv2
import numpy as np
import HandTrackingModule as htm
import pyautogui
from volumeControl import VolumeControl
import time

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

        if fingers is not None and fingers[0]== 0 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] ==0:
            dist = detector.find_distance(img, lmList, 8,12)
            if dist < 30:
                pyautogui.click()
                time.sleep(1)

                print("Clicked")



        if fingers is not None and fingers[0]== 1 and fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] ==0:
            dist = detector.find_distance(img, lmList, 4,5)
            if dist < 30:
                pyautogui.rightClick()
                time.sleep(1)

                print("right Clicked")
        # vloume
        if fingers is not None and fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0:
            print("Volume")
            volume = VolumeControl()
            img = volume.run(img, lmList)
        # alt tab
        if fingers is not None and fingers[0] == 0 and fingers[4] == 1 and fingers[3] == 1:
            dist = detector.find_distance(img, lmList, 4,17)
            print(dist)
            if dist < 58:
                pyautogui.hotkey('alt', 'tab')
                time.sleep(1)
                print("next")
        # ctrl tab
        if fingers is not None and fingers[0] == 0 and fingers[4] == 1 and fingers[3] == 0:
            print("tab")
            dist = detector.find_distance(img, lmList, 4,16)
            print(dist)
            if dist < 40:
                pyautogui.hotkey('ctrl', 'tab')
                print("next")
        # Scroll up
        if fingers is not None and fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and \
                fingers[4] == 1:
            dist = detector.find_distance(img, lmList, 4,5)
            print(dist)
            if dist <= 57:
                pyautogui.scroll(60)
        # function to scroll down
        if fingers is not None and fingers[0] == 0 and fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 0 and \
                fingers[4] == 0:
            print("Scroll down")
            pyautogui.scroll(-60)  # Adjust duration as needed for desired speed

    cv2.imshow("Image", img)
    cv2.waitKey(1)

cap.release()
cv2.destroyAllWindows()
