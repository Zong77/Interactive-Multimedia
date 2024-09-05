# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 09:25:21 2023

@author: Qi
"""

import cv2
from cvzone.HandTrackingModule import HandDetector
cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8)
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands,img = detector.findHands(img)
    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()
