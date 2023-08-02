import cv2
import mediapipe as mp
import math
import pyautogui
cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
x1 = 0
y1 = 0
y2 = 0
x2 = 0
def uzunlikni_hisoblash(x1, y1, x2, y2):
    a = abs(x2 - x1)
    b = abs(y2 - y1)
    uzunlik = math.sqrt(a**2 + b**2)
    return uzunlik
def uzunlikni_topish(x1, y1, x2, y2):
    x = (x1 + x2) / 2


    y = (y1 + y2) / 2
    return (x,y)


import time

interval = 2
next_time = time.time() + interval



while True:

    def mouse_click_and_press_enter(x, y):
        current_time = time.time()
        global next_time
        if current_time >= next_time:
            pyautogui.moveTo(x, y)  # Mausni berilgan x va y nuqtaga olib ketamiz
            pyautogui.click()  # Mausni bosing
            pyautogui.press('enter')
            next_time += interval
        else:
            pass

    success, image = cap.read()
    image = cv2.flip(image, 1)
    imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(imageRGB)
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks: # working with each hand
            for id, lm in enumerate(handLms.landmark):
                h, w, c = image.shape
                # cx, cy = int(lm.x * w), int(lm.y * h)
                if id == 8 :
                    x1, y1 = int(lm.x * w), int(lm.y * h)
                    cv2.circle(image, (x1, y1), 5, (0, 0, 255), cv2.FILLED)
                    pyautogui.moveTo(x1, y1)
                if id == 4 :
                    x2, y2 = int(lm.x * w), int(lm.y * h)
                    cv2.circle(image, (x2, y2), 5, (0, 0, 255), cv2.FILLED) 
                if x1 > 0 and y1 > 0 and x2 > 0 and y2 > 0:
                    # cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 2)
                    masofa = uzunlikni_topish(x1, y1, x2, y2)
                    uzunligi = uzunlikni_hisoblash(x1, y1, x2, y2)
                    cv2.circle(image, (int(masofa[0]),(int(masofa[1]))), 10, (0, 0, 255), cv2.FILLED)
                    print(uzunligi)
                    if uzunligi < 40:
                        cv2.circle(image, (int(masofa[0]),(int(masofa[1]))), 15, (255, 255, 0), cv2.FILLED)  
                        mouse_click_and_press_enter(x1,y1)
            mpDraw.draw_landmarks(image, handLms, mpHands.HAND_CONNECTIONS)
    cv2.imshow("Output", image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break