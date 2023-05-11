# Importing all modules
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import numpy as np

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size =(640, 480))
                    
# Specifying upper and lower ranges of color to detect in hsv format
lower = np.array([25, 80, 50])
upper = np.array([45, 255, 255]) # (These ranges will detect Yellow)

#hue: 45° (warm yellow) - 90° (yellow green)
#saturation: white (0) - colour (255)
#value: black (0) - colour (255)

# Capturing webcam footage
for frame in camera.capture_continuous(rawCapture, format = "bgr", use_video_port=True):
    image = frame.array
    

#while True:
    #success, video = webcam_video.read() # Reading webcam footage

    img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV) # Converting BGR image to HSV format

    mask = cv2.inRange(img, lower, upper) # Masking the image to find our color

    mask_contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # Finding contours in mask image

    drive_functs = [0,0,0]
    # Finding position of all contours
    if len(mask_contours) != 0:
        for mask_contour in mask_contours:
            if cv2.contourArea(mask_contour) > 500:
                x, y, w, h = cv2.boundingRect(mask_contour)
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 3) #drawing rectangle


                # Draw circle in the center of the bounding box
                x2 = x + int(w/2)
                y2 = y + int(h/2)
                cv2.circle(image,(x2,y2),4,(0,255,0),-1)
             
                # Print the centroid coordinates (we'll use the center of the
                # bounding box) on the image
                text = "x: " + str(x2) + ", y: " + str(y2)
                cv2.putText(image, text, (x2 - 10, y2 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                
                if x2 < 320:
                    drive_functs = [1,1,0]
                elif x2 > 320:
                    drive_functs = [1,0,1]
                else:
                    drive_functs = [1,0,0]
                


    cv2.putText(image, drive_functs,(0,0), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2 ) 
    cv2.imshow("mask image", mask) # Displaying mask image

    cv2.imshow("window", image) # Displaying webcam image
    
    rawCapture.truncate(0)
    
    if cv2.waitKey(1) == ord('q'):
        break

cv2.destroyAllWindows()
