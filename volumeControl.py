import mediapipe as mp
import HandTrackingModule as ht
import cv2
import math
import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Initialize the HandDetector
detector = ht.HandDetector(detection_conf=0.7)

# Initialize the camera
cap = cv2.VideoCapture(0)

# Initialize the volume control interface
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

# Initialize volume variables
volume_range = volume.GetVolumeRange()
min_volume, max_volume = volume_range[0], volume_range[1]
current_volume = volume.GetMasterVolumeLevelScalar()

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if lmList:
        # Get the positions of landmarks 4 and 8
        print(lmList[4], lmList[8])
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]

        cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)

        # Calculate the distance between landmarks 4 and 8
        distance = math.hypot(x2 - x1, y2 - y1)
        print(distance)

        # Map the distance to the volume range (you may need to adjust the min and max distance according to your setup)
        # These values are experimental, adjust them as needed for sensitivity
        min_distance = 30  # minimum distance for volume to be at min_volume
        max_distance = 100  # maximum distance for volume to be at max_volume
        volume_level = np.interp(distance, [min_distance, max_distance], [min_volume, max_volume])
        volume.SetMasterVolumeLevel(volume_level, None)

        # Optional: Display the distance and volume level for debugging
        cv2.putText(img, f'Dist: {int(distance)}, Vol: {int(volume_level)}', (10, 50), cv2.FONT_HERSHEY_PLAIN, 2,
                    (255, 0, 0), 2)

    if not success:
        print("Failed to read frame from camera.")
        break

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
