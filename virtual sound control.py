#(-65.25, 0.0, 0.03125)

import cv2
import time
import numpy as np
import handtracking as htm
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume



wcam, hcam = 1280, 720

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, hcam)



devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)


#volume.GetMute()
#volume.GetMasterVolumeLevel()
volrage = volume.GetVolumeRange()
minvol = volrage[0]
#print(minvol)
maxvol = volrage[1]
#print(maxvol)




pTime = 0

detector = htm.handDetector(detectionCon=0.75)


while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmlist, bbox = detector.findPosition(img)
    if len(lmlist) != 0:
        #print(lmlist[4], lmlist[8])
        x1, y1 = lmlist[4][1], lmlist[4][2]
        #print(x1,y1)
        x2, y2 = lmlist[8][1], lmlist[8][2]
        #print(x2,y2)
        cv2.circle(img, (x1,y1), 10, (255,0,0), cv2.FILLED)
        cv2.circle(img, (x2,y2), 10, (255,0,0), cv2.FILLED)

        cv2.line(img,(x1,y1),(x2,y2), (255,0,255),5)

        cx, cy = (x1+x2)//2, (y1+y2)//2
        cv2.circle(img, (cx,cy), 10, (255, 0, 0), cv2.FILLED)

        length = math.hypot(x2-x1 , y2-y1)
        #print("length = ", length)
        vol = np.interp(length, [50,250], [minvol, maxvol])
        volume.SetMasterVolumeLevel(vol, None)


        if length < 30:
            cv2.circle(img, (cx, cy), 10, (0, 0, 255), cv2.FILLED)




    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime=cTime
    cv2.putText(img, f'FPS {int(fps)}' , (40,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,255), 3)


    cv2.imshow("web cam out", img)


    cv2.waitKey(1)