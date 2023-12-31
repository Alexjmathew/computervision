import cv2
import mediapipe as mp
import time
cap = cv2.VideoCapture(0)

mphan = mp.solutions.hands
hands = mphan.Hands()
mpdrow = mp.solutions.drawing_utils

pTime=0
cTime=0

while True:
    success,img = cap.read()
    imgRGB =cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    result =hands.process(imgRGB)
    #print(result.multi_hand_landmarks)
    if result.multi_hand_landmarks:
        for handlms in result.multi_hand_landmarks:
            for id,lm in enumerate(handlms.landmark):
                # print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x *w),int(lm.y * h)
                print(id,cx,cy)
                if id ==4:
                     cv2.circle(img, (cx, cy), 15,(255,0,255), cv2.FILLED)
                if id ==8:
                     cv2.circle(img, (cx, cy), 15,(0,0,255), cv2.FILLED)

            mpdrow.draw_landmarks(img,handlms,mphan.HAND_CONNECTIONS)

    cTime= time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img,str(int(fps)),(20,98),
                cv2.FONT_HERSHEY_SIMPLEX,3,(255,0,255),3)
    # print(img)
    cv2.imshow("VIDEO",img)
    #cv2.imshow("RGB",imgRGB)
    cv2.waitKey(1)