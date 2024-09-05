# -*- coding: utf-8 -*-
"""
Created on Fri Nov  3 12:37:42 2023

@author: Qi
"""

import cv2
import mediapipe as mp
import time

# 初始化 MediaPipe Pose 模型
mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()

# 開啟 Webcam
cap = cv2.VideoCapture(0)
pTime = 0

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)

    # 如果有偵測到人體姿勢
    if results.pose_landmarks:
        mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
        for id, lm in enumerate(results.pose_landmarks.landmark):
            h, w, c = img.shape
            print(id, lm)  # 印出：特徵點編號、XY座標
            cx, cy = int(lm.x * w), int(lm.y * h)
            cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    cv2.imshow("Image", img)
    key = cv2.waitKey(1)

    if key == ord('q'):
        break

# 釋放 Webcam 資源
cap.release()
cv2.destroyAllWindows()
