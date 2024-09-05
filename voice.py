# -*- coding: utf-8 -*-
"""
Created on Fri Nov  3 11:04:19 2023

@author: Qi
"""

import cv2  # 我們將使用它來捕獲網絡攝像頭的圖像並將其轉換為RGB。
import numpy as np  # NumPy將幫助我們處理數組。
# import HandTrackingModule as htm # 使用本地模組文件
from cvzone.HandTrackingModule import HandDetector  # 使用CVZone
import math
from ctypes import cast, POINTER  # pycaw庫的用法
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# detector = htm.handDetector(detectionCon=0.7) # 使用本地模組文件
detector = HandDetector(detectionCon=0.8)  # 使用CVZone

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

# volume.GetMute() # volume.SetMute(1, None) 為靜音，0為不靜音
# volume.GetMasterVolumeLevel() # 獲取音量值，0.0代表最大，-65.25代表最小
volRange = volume.GetVolumeRange()  # 獲取音量範圍，如(-65.25, 0.0, 0.75)，第一個代表最小值，第二個代表最大值，第三個為增減量間隔，單位為db
minVol = volRange[0]
maxVol = volRange[1]
vol = 0
volBar = 400
volPer = 0

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    # img = detector.findHands(img) # 使用本地模組文件-找出手特徵點位置
    hands, img = detector.findHands(img)  # 使用CVZone-找出手特徵點位置--開始

    if len(hands) > 0:
        lmList = hands[0]["lmList"]
    else:
        lmList = []  # 使用CVZone-找出手特徵點位置--結束

    # lmList, _ = detector.findPosition(img) # 使用本地模組文件-找出手特徵點位置；findPosition() return self.lmList, bbox

    if len(lmList) != 0:
        x1 = lmList[4][0]  # 4是拇指尖
        y1 = lmList[4][1]
        x2 = lmList[8][0]  # 4是食指尖
        y2 = lmList[8][1]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        length = math.hypot(x2 - x1, y2 - y1)  # 計算4點和8點之間的距離
        print(length)

        vol = np.interp(length, [50, 170], [minVol, maxVol])  # 將手的範圍轉換為音量範圍。手的範圍為50 - 170；音量範圍為-65 - 0
        volBar = np.interp(length, [50, 170], [400, 150])  # 2指距離對應到音量條高度
        volPer = np.interp(length, [50, 170], [0, 100])  # 2指距離對應到0-100
        print(int(length), vol)

        volume.SetMasterVolumeLevel(vol, None)  # 設定音量：0.0代表音量100，-65.25最小音量

        if length < 50:
            cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)
            cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)  # 畫出音量條外框
            cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED)  # 畫出2指距離對應到音量條高度
            cv2.putText(img, f'{int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)

    cv2.imshow("Img", img)
    key = cv2.waitKey(1)

    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()