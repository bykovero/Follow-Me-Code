import numpy as np
import cv2 as cv


cap = cv.VideoCapture(0)

while True:
    ret, frame = cap.read()

    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)


    #hue: 45°(Warm Yellow) - 90° (Yellow Green) divide by 2 for opencv
    #saturation: white (0) - color (255)
    #value: black (0) - color (255)
    lower_color = np.array([25, 80, 50])
    upper_color = np.array([45, 255, 255])

    mask = cv.inRange(hsv, lower_color, upper_color)

    result = cv.bitwise_and(frame, frame, mask = mask)



    
    cv.imshow('frame', frame)
    cv.imshow('hsv', hsv)
    cv.imshow('result', result)

    if cv.waitKey(1) == ord('q'):
        break

cap.release()

cv.destroyAllWindows()

