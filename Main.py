import cv2
import mediapipe as mp
import numpy as np
import time
import pyautogui
import math
import autopy

def main():
    wcam, hcam = 640, 480
    frameR = 150
    wScr, hScr = autopy.screen.size()

    cap = cv2.VideoCapture(0)
    cap.set(3, wcam)
    cap.set(4, hcam)

    pTime = 0
    cTime = 0
    prevx, prevy = 0, 0
    curx, cury = 0, 0

    hands = HandDetector(maxHands=1, detectCoor=0.8)

    while True:
        isTrue, frame = cap.read()
        frame = hands.findHands(frame)
        lmList = hands.findPosition(frame, draw=False)
        if len(lmList)!=0:

            finger1x, finger1y = lmList[8][1:]
            finger2x, finger2y = lmList[12][1:]

            cv2.rectangle(frame, (frameR, frameR), (wcam - frameR, hcam - frameR), (255,255,0), 5)
            fingers = hands.fingersUp(lmList)



            if fingers[1]==1 and fingers[2]==0:
                cv2.circle(frame, (finger1x, finger1y), 10, (255, 0, 255), cv2.FILLED)
                x3 = np.interp(finger1x, (frameR, wcam-frameR), (0, wScr))
                y3 = np.interp(finger1y, (frameR, hcam-frameR), (0, hScr))

                curx = prevx + (x3 - prevx)/4
                cury = prevy + (y3 - prevy)/4

                autopy.mouse.move(wScr - curx, cury)
                prevx, prevy = curx, cury

            if fingers[1]==1 and fingers[2]==1: #Lest Click
                dist, frame, info = hands.fingerdistance(frame, lmList)
                print(dist)
                print(info[4], info[5])
            
                if dist < 30:
                    autopy.mouse.click()
                    cv2.circle(frame, (info[4], info[5]), 15, (0, 0, 255),cv2.FILLED)

            if fingers[0]==1 and fingers[1]==1 and fingers[2]==1: #Right Click
                dist, frame, info = hands.fingerdistance(frame, lmList)
                print(dist)
                print(info[4], info[5])
            
                if dist < 30:
                    pyautogui.click(button='right')
                    cv2.circle(frame, (info[4], info[5]), 15, (0, 0, 255),cv2.FILLED)
    
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        cv2.putText(frame, str(int(fps)), (10,50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (200,255,127), 2)
    
        cv2.imshow('Webcam', frame)
        cv2.waitKey(1)
    
        if cv2.waitKey(20) & 0xFF==ord('e'):
            break

    exit(0)
    cap.release()
    cv2.destroyAllWindows()


if __name__=='__main__':
    main()
