import mediapipe as mp
import cv2
import time

class HandDetector():
    def __init__(self, mode=False, maxHands=2, detectCoor=0.5, trackCoor=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectCoor = detectCoor
        self.trackCoor = trackCoor


        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.detectCoor, self.trackCoor)
        self.mpFace = mp.solutions.face_mesh
        self.face = self.mpFace.FaceMesh()
        self.mpDrawHand = mp.solutions.drawing_utils
        self.tipId = [4, 8, 12, 16, 20]



    def findHands(self, frame, draw=True):
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        faceResults = self.face.process(img)
        self.results = self.hands.process(img)
        #print(results.multi_handedness)
        #print(faceResults.multi_face_landmarks)

        if self.results.multi_hand_landmarks:
            for handlm in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDrawHand.draw_landmarks(frame, handlm, self.mpHands.HAND_CONNECTIONS)
                    #mpDrawHand.plot_landmarks(handlm, mpHands.HAND_CONNECTIONS)
        return frame


    def findPosition(self, frame, handNo=0, draw=True, drawId=0):
        self.landmarkList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for Id, lm in enumerate(myHand.landmark):
                h, w, c = frame.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                self.landmarkList.append([Id, cx, cy])
                #print(Id, cx, cy)
                if draw:
                    if Id==drawId:
                        cv2.circle(frame, (cx,cy), 17, (255,255,0), cv2.FILLED)
        return self.landmarkList

    def fingersUp(self, landmarkList):
        self.fingers = []
        #po0x, po0y = landmarkList[0][1:]
        #finger1x, finger1y = landmarkList[8][1:]
        #finger2x, finger2y = landmarkList[12][1:]
        #finger1knucklex, finger1knuckley = landmarkList[5][1:]
        #finger2knucklex, finger2knuckley = landmarkList[9][1:]
        
        if landmarkList[self.tipId[0]][1] > landmarkList[self.tipId[0]-1][1]:
            self.fingers.append(1)
        else:
            self.fingers.append(0)
        
        for Id in range(1,5):
            if math.hypot((landmarkList[self.tipId[Id]][1] - landmarkList[0][1]), (landmarkList[self.tipId[Id]][2] - landmarkList[0][2])) > math.hypot((landmarkList[self.tipId[Id] - 3][1] - landmarkList[0][1]), (landmarkList[self.tipId[Id] - 3][2] - landmarkList[0][2])):
                self.fingers.append(1)
            else:
                self.fingers.append(0)

        return self.fingers

    def fingerdistance(self, frame, landmarkList, draw=True):
        finger1x, finger1y = landmarkList[8][1:]
        finger2x, finger2y = landmarkList[12][1:]
        self.dist = math.hypot((finger2x - finger1x), (finger2y - finger1y))
        midx, midy = (finger1x + finger2x)//2, (finger1y + finger2y)//2
        
        if draw:
            cv2.line(frame, (finger2x, finger2y), (finger1x, finger1y), (0,255,0), 3)
            cv2.circle(frame, (midx, midy), 10, (255, 0, 0), cv2.FILLED)

        return self.dist, frame, [finger1x, finger1y, finger2x, finger2y, midx, midy]
