# -*- coding: utf-8 -*-
"""
Created on Fri Nov  3 11:28:51 2023

@author: Qi
"""

import cv2
import mediapipe as mp
import time

# 開啟Webcam
cap = cv2.VideoCapture(0)
pTime = 0

x_up = 0
y_up = 0
x_down = 0
y_down = 0

mpDraw = mp.solutions.drawing_utils
mpFaceMesh = mp.solutions.face_mesh  # 使用mediapipe(mp)之solutions的face_mesh

faceMesh = mpFaceMesh.FaceMesh(max_num_faces=2)  # 設定偵測facemesh之參數
drawSpec = mpDraw.DrawingSpec(thickness=1, circle_radius=2)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    results = faceMesh.process(imgRGB)  # 執行facemesh偵測

    if results.multi_face_landmarks:
        for faceLms in results.multi_face_landmarks:
            mpDraw.draw_landmarks(img, faceLms, mpFaceMesh.FACE_CONNECTIONS, drawSpec, drawSpec)
            for id, lm in enumerate(faceLms.landmark):
                ih, iw, ic = img.shape
                x, y = int(lm.x * iw), int(lm.y * ih)
                print(id, x, y)
                if id == 0:
                    cv2.circle(img, (x, y), 3, (255, 0, 0), cv2.FILLED)
                    x_up = x
                    y_up = y
                if id == 17:
                    cv2.circle(img, (x, y), 3, (0, 0, 255), cv2.FILLED)
                    x_down = x
                    y_down = y
            cv2.line(img, (x_up, y_up), (x_down, y_down), (255, 0, 255), 1)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    cv2.imshow("Image", img)
    key = cv2.waitKey(1)

    if key == ord('q'):
        break

# 釋放資源
cap.release()
cv2.destroyAllWindows()