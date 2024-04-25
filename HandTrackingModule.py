import math

import cv2
import mediapipe as mp
import time




class HandDetector():
    def __init__(self, mode = False, max_hand = 2, model_complexity=1, detection_conf = 0.5, tracking_conf = 0.5):
        self.mode = mode
        self.max_hand = max_hand
        self.model_complexity = model_complexity
        self.detection_conf = detection_conf;
        self.tracking_conf = tracking_conf

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.max_hand, self.model_complexity,self.detection_conf, self.tracking_conf)
        self.mpDraw = mp.solutions.drawing_utils



    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)

        # for the fps

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                if draw:
                     self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)

        return img

    def findPosition(self, img, handId=0, draw=False):
        lmList = []
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.hands.process(imgRGB)
        if results.multi_hand_landmarks:
            handLms = results.multi_hand_landmarks[handId]
            for id, lm in enumerate(handLms.landmark):
                # height width and channel of image
                h, w, c = img.shape
                # cx and cy is the center point multiply by wdth and height
                cx, cy = int(lm.x * w), int(lm.y * h)

                lmList.append([id,cx,cy])
                if draw:
                    print(id, cx, cy)

        return lmList

    def find_distance(self, img, lmList, point1_id, point2_id):
        x1, y1 = lmList[point1_id][1:]
        x2, y2 = lmList[point2_id][1:]
        distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

        # Draw line between points
        cv2.line(img, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 255), 3)

        # Calculate midpoint
        mx, my = (x1 + x2) // 2, (y1 + y2) // 2

        # Draw small circle at midpoint
        cv2.circle(img, (int(mx), int(my)), 5, (0, 255, 255), cv2.FILLED)

        return distance
    def detectFingers(self, img, handId=0):
        lmList = self.findPosition(img, handId, draw=False)
        if len(lmList) != 0:
            fingers = []

            # Thumb (check if x-coordinate of thumb tip is to the right of thumb base)
            if lmList[4][1] > lmList[3][1]:
                fingers.append(1)
            else:
                fingers.append(0)

            # Other fingers (check if y-coordinate of finger tip is higher than finger base)
            for finger_tip_id, finger_base_id in [(8, 6), (12, 10), (16, 14), (20, 18)]:
                if lmList[finger_tip_id][2] < lmList[finger_base_id][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            return fingers


def main():
    cap = cv2.VideoCapture(0)
    detector = HandDetector()

    cTime = 0
    pTime = 0

    while True:
        success, img = cap.read()
        img= detector.findHands(img)
        lmList = detector.findPosition(img)
        if len(lmList)>0:
            print(lmList[4])


        if not success:
            print("Failed to read frame from camera.")
            break

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
