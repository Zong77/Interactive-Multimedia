import cv2
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
cap.set(3, 1920)
cap.set(4, 1020)

detector = HandDetector(detectionCon=0.7, maxHands=2)

startDist = None
scale = 0
cx, cy = 600, 200

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img)

    img1 = cv2.imread("1.jpg")
   
    if len(hands) == 2:
        print(detector.fingersUp(hands[0]), detector.fingersUp(hands[1]))
        if detector.fingersUp(hands[0]) == [1, 1, 0, 0, 0] and detector.fingersUp(hands[1]) == [1, 1, 0, 0, 0]:
            print("Zoom Gesture")
            lmList1 = hands[0]["lmList"]
            lmList2 = hands[1]["lmList"]
            if startDist is None:
                length, info, img = detector.findDistance(hands[0]["center"], hands[1]["center"], img)
                startDist = length
            else:
                length, info, img = detector.findDistance(hands[0]["center"], hands[1]["center"], img)
                scale = int((length - startDist) // 2)
                cx, cy = info[4:]
    else:
        startDist = None
   
    try:
        h1, w1, _ = img1.shape
        newH, newW = int((h1 + scale) / 2) * 2, int((w1 + scale) / 2) * 2
        img1 = cv2.resize(img1, (newW, newH))
        img[cy - int(newH / 2):cy + int(newH / 2), cx - int(newW / 2):cx + int(newW / 2)] = img1
    except:
        pass
   
    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()