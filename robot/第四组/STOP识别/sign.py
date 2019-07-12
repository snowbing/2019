import cv2
import os
import serial
ser = serial.Serial("/dev/ttyAMA0",9600)

import sys
sys.path.append('/home/pi/')
import CAM as CAM

def sign():
	face_detector = cv2.CascadeClassifier('/home/pi/sign/Cascades/stop_sign.xml')
	count = 0
	change = 0
	stop = 0
	while(True):
		ret, img = CAM.readi()
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		faces = face_detector.detectMultiScale( gray,
				scaleFactor=1.1,
				minNeighbors=5,
				minSize=(30, 30))
		if len(faces):#识别累加中
			count+=1
			change = 0
		elif change == 0:#未识别保持
			change = 1
		elif stop == 1 and change == 1:#未识别,车辆试图启动
			change = 0
			count = 0
			stop = 0
			if(CAM.removeReason(2) > 0):#还原
				#ser.write(b'1\n')
				print('launch for sign')
		if count >= 5 :
			stop = 1
			ser.write(b'7\n')
			print('stop for sign')
			CAM.setReason(2)
	   # for (x,y,w,h) in faces:
	   #     cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)     
			
	 
		#cv2.imshow('image', img)
	 
		#k = cv2.waitKey(100) & 0xff # Press 'ESC' for exiting video
		#if k == 27:
		   # break
	return
