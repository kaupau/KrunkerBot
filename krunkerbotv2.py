import cv2
import numpy as np
import pyautogui
#from mss import mss
from PIL import ImageGrab

def resizeVid(percent):
    ret, frame = cap.read()
    return (int(frame.shape[1]*percent/100), int(frame.shape[0]*percent/100))
def distance(v1, v2):
    return (v1[0]-v2[0],v1[1]-v2[1])
def killtarget(v1):
    pyautogui.move( int(v1[0]*10/3), int(v1[1]*10/3) )
    pyautogui.click()
CENTER_POINT_ALTERED = (int(958*.3-103), int(576*.3-76))

cap = cv2.VideoCapture("test.mp4")
resizeDim = resizeVid(30)
resizeDim2 = resizeVid(35)
ret, frame = cap.read()


while True:
    ret, frame = cap.read()
    #frame = cv2.cvtColor(np.array(ImageGrab.grab()), cv2.COLOR_RGB2BGR)

    if ret:
        frame = cv2.resize(frame, resizeDim, interpolation=cv2.INTER_AREA)
        frame = frame[76:254, 103:423]

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        lower_bound = np.array([156, 156, 156])
        upper_bound = np.array([244, 247, 249])
        reds = cv2.inRange(hsv, lower_bound, upper_bound)

        contours, hier = cv2.findContours(reds, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            if 10 < cv2.contourArea(cnt) < 5000:
                (x, y, w, h) = cv2.boundingRect(cnt)
                # proper bounding boxes, might rewrite later
                w = 42 if(h >= 4) else 33
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255,0,0), 2)
                #print(h,w)
                cv2.circle(frame, (x + int(w/2), y + h + h), 3, (255, 0, 0), 1)
                #killtarget( distance((x + int(w/2), y + h + h), CENTER_POINT_ALTERED) )

        cv2.circle(frame, (86, 185), 3, (255,0,0), 2)
        frame = cv2.resize(frame, resizeDim2, interpolation=cv2.INTER_AREA)
        cv2.imshow("Original", frame)
        #cv2.imshow("Reds", reds)

        if cv2.waitKey(30) & 0xFF == ord('q'):
            break
    else:
        break