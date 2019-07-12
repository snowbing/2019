import sys
sys.path.append('/home/pi/')
import CAM as CAM
import numpy as np 
import cv2
import serial
ser = serial.Serial("/dev/ttyAMA0",9600)



lower_green = np.array([50, 100, 100])
upper_green = np.array([70, 255, 255])
# 在HSV空间中定义红色
lower_red = np.array([0, 100, 100])
upper_red = np.array([10, 255, 255])

lower_blue = np.array([78, 43, 46])
upper_blue = np.array([110, 255, 255])


# Detect blobs.
red = 0
blue = 0
def detect_light(img,lower,upper,r):
    global red, blue
    blur_image = cv2.medianBlur(img, 3)
    hsv = cv2.cvtColor(blur_image, cv2.COLOR_BGR2HSV)
    maskx = cv2.inRange(hsv, lower, upper)
    res = cv2.bitwise_and(blur_image, blur_image, mask = maskx)
    gray = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)
    if r == 0:
        ret, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY )
    else :
        ret, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY )
    mask = cv2.erode(binary, None, iterations=2)
	# 膨胀操作，先腐蚀后膨胀以滤除噪声
    mask = cv2.dilate(mask, None, iterations=2)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    if cnts  :
        if r == 0:
            blue += 1
        else:
            red += 1
    else :
         if r == 0:
            blue = 0
         else:
            red = 0




def light():
  while 1:
    ret, img = CAM.readi()

    detect_light(img,lower_blue,upper_blue,0)
    detect_light(img,lower_red,upper_red,1)
    if red >2:
        print("stop for light")
        ser.write(b'7\n')
        CAM.setReason(1)
    if blue >5 :
        print("发现蓝光")
        #ser.write(b'1\n')
        if(CAM.removeReason(1) > 0):
            ser.write(b'1\n')
            print('launch for light')
  return 0



