import cv2
import mediapipe
import numpy
import autopy
import pyautogui


cap = cv2.VideoCapture(0)
initHand = mediapipe.solutions.hands
mainHand = initHand.Hands(max_num_hands=1, min_detection_confidence=0.9, min_tracking_confidence=0.9)
draw = mediapipe.solutions.drawing_utils
wScr, hScr = autopy.screen.size()
pX, pY = 0, 0
cX, cY = 0, 0

def handLandmarks(colorImg):
    landmarkList = []
    landmarkPositions = mainHand.process(colorImg)
    landmarkCheck = landmarkPositions.multi_hand_landmarks
    if landmarkCheck:
        for hand in landmarkCheck:
            for index, landmark in enumerate(hand.landmark):
                draw.draw_landmarks(img, hand, initHand.HAND_CONNECTIONS)
                h, w, c = img.shape
                centerX, centerY = int(landmark.x * w), int(landmark.y * h)
                landmarkList.append([index, centerX, centerY])

    return landmarkList

def fingers(landmarks):
    fingerTips = []
    tipIds = [4, 8, 12, 16, 20]

    # Check if thumb is up
    if landmarks[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
        fingerTips.append(1)
    else:
        fingerTips.append(0)

    for id in range(1, 5):
        if landmarks[tipIds[id]][2] < landmarks[tipIds[id] - 3][2]:
            fingerTips.append(1)
        else:
            fingerTips.append(0)

    return fingerTips


while True:
    check, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    lmList = handLandmarks(imgRGB)
    results = mainHand.process(img)
    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        finger = fingers(lmList)
    if results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[0]

        if results.multi_hand_landmarks != None:
            if lmList[2][1] > lmList[17][1]:

                if finger[0] == 1 and finger[1] == 1 and finger[2] == 1 and finger[3] == 1 and finger[4] == 1:
                    x3 = numpy.interp(x1, (100, 590 - 100), (0, wScr))
                    y3 = numpy.interp(y1, (100, 390 - 100), (0, hScr))

                    cX = pX + (x3 - pX) / 10
                    cY = pY + (y3 - pY) / 10

                    autopy.mouse.move(wScr - cX, cY)
                    pX, pY = cX, cY

                elif finger[0] == 1 and finger[1] == 1 and finger[2] == 0 and finger[3] == 0 and finger[4] == 0:
                    pyautogui.leftClick(interval=0.9)

                elif finger[0] == 1 and finger[1] == 1 and finger[2] == 1 and finger[3] == 0 and finger[4] == 0:
                    pyautogui.doubleClick(interval=0.4)

                elif finger[0] == 0 and finger[1] == 1 and finger[2] == 1 and finger[3] == 1 and finger[4] == 0:
                    pyautogui.rightClick(interval=0.9)

                elif finger[0] == 0 and finger[1] == 1 and finger[2] == 1 and finger[3] == 1 and finger[4] == 1:
                    pyautogui.mouseDown(button="left")
                    autopy.mouse.move(wScr - cX, cY)

                elif finger[0] == 1 and finger[1] == 1 and finger[2] == 0 and finger[3] == 0 and finger[4] == 0:
                    pyautogui.mouseUp(button="left")

            if lmList[2][1] < lmList[17][1]:
                if finger[0] == 0 and finger[1] == 1 and finger[2] == 1 and finger[3] == 1 and finger[4] == 1:
                    x3 = numpy.interp(x1, (100, 600 - 100), (0, wScr))
                    y3 = numpy.interp(y1, (100, 400 - 100), (0, hScr))

                    cX = pX + (x3 - pX) / 10
                    cY = pY + (y3 - pY) / 10

                    autopy.mouse.move(wScr - cX, cY)
                    pX, pY = cX, cY

                elif finger[0] == 1 and finger[1] == 1 and finger[2] == 1 and finger[3] == 1 and finger[4] == 1:
                    pyautogui.keyDown("win")
                    pyautogui.press("tab", interval=0.9)
                    pyautogui.keyUp("win")

                elif finger[0] == 1 and finger[1] == 1 and finger[2] == 0 and finger[3] == 0 and finger[4] == 0:
                    pyautogui.leftClick(interval=0.9)

                elif finger[0] == 0 and finger[1] == 0 and finger[2] == 0 and finger[3] == 0 and finger[4] == 0:
                    pyautogui.vscroll(100)

                elif finger[0] == 1 and finger[1] == 0 and finger[2] == 0 and finger[3] == 0 and finger[4] == 0:
                    pyautogui.vscroll(-100)

                elif finger[0] == 1 and finger[1] == 0 and finger[2] == 0 and finger[3] == 0 and finger[4] == 1:
                    pyautogui.hotkey('win', 'd', interval=0.2)

                elif finger[0] == 1 and finger[1] == 1 and finger[2] == 1 and finger[3] == 0 and finger[4] == 0:
                    pyautogui.press("playpause", interval=0.5)

    cv2.imshow("Webcam", img)
    k = cv2.waitKey(1)
    if k == 13 or k == 27:
        break

cap.release()  # release software / hardware resource
cv2.destroyAllWindows()
