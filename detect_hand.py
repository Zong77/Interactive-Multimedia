# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 10:02:57 2023

@author: Qi
"""

import cv2
import HandTrackingModule_1 as htm #由本地模組檔載入，*該檔案在此程式同位置，此例並非使用CVZone(HandTrackingModule.py直接import mediapipe)

cap = cv2.VideoCapture(0)
detector = htm.handDetector()
 
while True:
    success,img = cap.read()
    img =cv2.flip(img, 1)
    img =detector.findHands(img)
    cv2.imshow("jchen-Hand", img)
    lmList,bbox = detector.findPosition(img)
    if len(lmList) != 0:
       print(lmList[4],lmList[4][1], lmList[4][2])
       detector.fingersUp()
       detector.findDistance(4,8,img)
 
    key =cv2.waitKey(1)
    if key ==ord('q'):
       break
  
cap.release()
cv2.destroyAllWindows()