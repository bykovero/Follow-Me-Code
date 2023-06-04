#----------IMPORTING MODULES----------
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import numpy as np
import serial
import time

#----------INITIATING SERIAL----------
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout = 1) #ttyUSB0 is the port on which arduino is connected
ser.reset_input_buffer()

#----------SETTING CAMERA SETTINGS----------
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size =(640, 480))

#----------SETTING UPPER AND LOWER RANGES FOR COLOR DETECTION (HSV)----------
lower = np.array([25, 80, 50])
upper = np.array([45, 255, 255])

#hue: 45° (warm yellow) - 90° (yellow green) -> divide by 2 for 8-bit numbers
#saturation: white (0) - colour (255)
#value: black (0) - colour (255)


#----------CAPTURING WEBCAM FOOTAGE----------
for frame in camera.capture_continuous(rawCapture, format = "bgr", use_video_port=True):
    image = frame.array
    

    img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV) #Converting BGR image to HSV format

    mask = cv2.inRange(img, lower, upper) #Masking the image to find our color

    mask_contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #Finding contours in mask image

    
    # Finding position of all contours
    if len(mask_contours) != 0:     #checking if there are countours
        for mask_contour in mask_contours:
            if cv2.contourArea(mask_contour) <= 1500:
                #if the area of the contour is smaller than 1500 -> stop
                ser.write(b"[0,0,0,0]\n")
            
            elif cv2.contourArea(mask_contour) > 1500:
                #if the area of the contour is larger than 1500 -> draw a rectangle over the contour
                x, y, w, h = cv2.boundingRect(mask_contour)
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 3) #drawing rectangle (for visuals (when connected to a monitor))
                
                area = w*h  #calculate area of rectangle -> later necessary for determining driving forwards speed

                # Draw circle in the center of the bounding box (for visuals (when connected to a monitor))
                x2 = x + int(w/2)
                y2 = y + int(h/2)
                cv2.circle(image,(x2,y2),4,(0,255,0),-1)

                # Print the centroid coordinates (necessary for determining when to drive right, left and forwards)
                text = "x: " + str(x2) + ", y: " + str(y2) + ", " + str(area)
                cv2.putText(image, text, (x2 - 10, y2 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                

                #Template for ser.write: [0,0,0,0] = left, right, forwards, speed
                #speed only relevant for forwards movement
                
                if x2 < 256:
                  #if the circle in the middle of the rectangle is in the left 2/5 of the image -> 
                  #send a message to turn left
                    ser.write(b"[1,0,0,1]\n")
                
                elif x2 > 384:
                  #if the circle in the middle of the rectangle is in the right 2/5 of the image -> 
                  #send a message to turn right
                    ser.write(b"[0,1,0,1]\n")
                
                else:
                  #if the circle in the middle of the rectangle is in the middle 1/5 of the image -> 
                  #determine how fast to drive forwards
                  
                    #if the area is very large, robot should stop to avoid collision with object,
                    #or drive very slowly; the smaller the area the faster the speed
                    if area >= 70000:
                        ser.write(b"[0,0,1,0]\n")
                    elif area >= 20000:
                        ser.write(b"[0,0,1,80]\n")
                    elif area >= 10000:
                        ser.write(b"[0,0,1,80]\n")
                    elif area >= 8000:
                        ser.write(b"[0,0,1,90]\n")
                    elif area >= 6000:
                        ser.write(b"[0,0,1,100]\n")
                    elif area >= 4000:
                        ser.write(b"[0,0,1,110]\n")
                    elif area >= 2000:
                        ser.write(b"[0,0,1,120]\n")
                    else:
                        ser.write(b"[0,0,1,0]\n")

                area = 0 #set area to 0 to avoid bugs


    cv2.imshow("mask image", mask) # Displaying mask image -> for visual check & testing

    cv2.imshow("camera capture", image) # Displaying webcam image -> for visual check & testing
    
    rawCapture.truncate(0) #releasing the frame, required by the module/system
    
