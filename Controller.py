import math
import cv2
import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

class VolumeControl:
    def __init__(self):
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = cast(interface, POINTER(IAudioEndpointVolume))
        self.volume_range = self.volume.GetVolumeRange()
        self.min_volume, self.max_volume = self.volume_range[0], self.volume_range[1]

    def run(self, img, lmList):
        if len(lmList) != 0:
            x1, y1 = lmList[4][1], lmList[4][2]
            x2, y2 = lmList[8][1], lmList[8][2]

            distance = math.hypot(x2 - x1, y2 - y1)

            volume_level = np.interp(distance, [30, 100], [self.min_volume, self.max_volume])
            self.volume.SetMasterVolumeLevel(volume_level, None)

            cv2.putText(img, f'Dist: {int(distance)}, Vol: {int(volume_level)}', (10, 50), cv2.FONT_HERSHEY_PLAIN, 2,
                        (255, 0, 0), 2)
        return img
