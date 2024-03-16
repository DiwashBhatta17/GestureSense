import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

cTime = 0
pTime = 0

while True:
    success, img = cap.read()
    if not success:
        print("Failed to read frame from camera.")
        break

    imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    #print(results.multi_hand_landmarks)

    #for the fps


    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(img,handLms,mpHands.HAND_CONNECTIONS)
            for id, lm in enumerate(handLms.landmark):
                #height width and channel of image
                h, w, c = img.shape
                #cx and cy is the center point multiply by wdth and height
                cx, cy = int(lm.x*w), int(lm.y*h)
                print(id ,cx,cy)
                if id == 8 or id == 4:
                    cv2.circle(img,(cx,cy),10,(255,0,255),cv2.FILLED)

    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    # Replace this with the calculated frames per second (fps) value

    # Convert fps to string and place it on the image at position (10, 70)


    cv2.imshow("Image", img)
    cv2.waitKey(1)
