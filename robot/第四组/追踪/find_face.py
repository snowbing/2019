#trig 黄 L4  GPIO4
#gnd 蓝 L5  GND
#echo 绿 L6  GPIO 17
#找到 绿灯 L7 GPIO 27
#找到 绿灯 L8 GPIO22
# 3v3
#未找到 黄灯 L10 GPIO10
#未找到 黄灯 L11 GPIO9

import sys
sys.path.append('/home/pi/face/')
sys.path.append('/home/pi/')

from recognition import face
import CAM as CAM

import time
import numpy as np
import cv2
import serial
ser = serial.Serial("/dev/ttyAMA0",9600)
import RPi.GPIO as GPIO


faceCascade = cv2.CascadeClassifier('/home/pi/track/face.xml')
dt = 80
mind = 80
cam=CAM.read()
width=cam.get(3)
height=cam.get(4)
 
#超声波相关
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT)
GPIO.output(4, GPIO.LOW)
GPIO.setup(17, GPIO.IN)

#布灵布灵相关
GPIO.setup(27, GPIO.OUT)
GPIO.output(27, GPIO.LOW)
GPIO.setup(22, GPIO.OUT)
GPIO.output(22, GPIO.LOW)
GPIO.setup(9, GPIO.OUT)
GPIO.output(9, GPIO.LOW)
GPIO.setup(10, GPIO.OUT)
GPIO.output(10, GPIO.LOW)

def getDistance():
		print('finding distance')
		GPIO.setmode(GPIO.BCM)
		GPIO.output(4, GPIO.HIGH)
		time.sleep(0.00015)
		GPIO.output(4, GPIO.LOW)
		timetest=time.time()
		while not GPIO.input(17):
			if time.time()-timetest>1:
				return 9999
		t1 = time.time()
		while GPIO.input(17):
			pass
		t2 = time.time()
		return (t2-t1)*340*100/2

def bulingbuling(way):
	GPIO.setmode(GPIO.BCM)
	if way == 1: #寻找失败
		GPIO.output(27, GPIO.HIGH)
		for i in range(15):
			time.sleep(0.4)
			GPIO.output(27, not GPIO.input(27))
			GPIO.output(22, not GPIO.input(22))
		time.sleep(0.4)
		GPIO.output(27, GPIO.LOW)
		GPIO.output(22, GPIO.LOW)
	elif way == 2:
		GPIO.output(10, GPIO.HIGH)
		for i in range(15):
			time.sleep(0.4)
			GPIO.output(10, not GPIO.input(10))
			GPIO.output(9, not GPIO.input(9))
		time.sleep(0.4)
		GPIO.output(9, GPIO.LOW)
		GPIO.output(10, GPIO.LOW)
	return 0
		
def find_face(host_face = 1):
	change = 0
	while True:
		if_control = CAM.get()
		if(if_control!=2):
			continue
		ret,img = CAM.readi()
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		faces = faceCascade.detectMultiScale(
			gray,     
			scaleFactor=1.2,
			minNeighbors=5,     
			minSize=(20, 20)
		)
		
		#寻找人脸
		if not len(faces):
			if change < 5:
				change+= 1
				continue
			else:
			#左转寻找下一个目标
				change = 0
				ser.write(b'1\n')
				time.sleep(0.1)
				ser.write(b'5\n')
				time.sleep(0.4)
				ser.write(b'7\n')
				time.sleep(0.1)
				ser.write(b'2\n')
				time.sleep(0.1)
				ser.write(b'7\n')
				continue
		change = 0
		(x,y,w,h) = faces[0]
		ax = x+w/2
		
		#校准过程
		if ax - width/2 >dt :
			print('go right')
			ser.write(b'1\n')
			time.sleep(0.08)
			ser.write(b'6\n')
			time.sleep(0.2)
			ser.write(b'7\n')
			time.sleep(0.1)
			ser.write(b'2\n')
			time.sleep(0.1)
			ser.write(b'7\n')
			continue
		elif width/2 - ax >dt:
			print('go left')
			ser.write(b'1\n')
			time.sleep(0.08)
			ser.write(b'5\n')
			time.sleep(0.2)
			ser.write(b'7\n')
			time.sleep(0.1)
			ser.write(b'2\n')
			time.sleep(0.1)
			ser.write(b'7\n')
			continue
		elif  ax - width/2 >dt/2:
			print('go right a little')
			ser.write(b'1\n')
			time.sleep(0.05)
			ser.write(b'6\n')
			time.sleep(0.05)
			ser.write(b'7\n')
			time.sleep(0.05)
			ser.write(b'2\n')
			time.sleep(0.05)
			ser.write(b'7\n')
			continue
		elif width/2 - ax >dt/2:
			print('go left a little')
			ser.write(b'1\n')
			time.sleep(0.05)
			ser.write(b'5\n')
			time.sleep(0.05)
			ser.write(b'7\n')
			time.sleep(0.05)
			ser.write(b'2\n')
			time.sleep(0.05)
			ser.write(b'7\n')
			continue
			
		#开始追踪人脸
		print('go for face')
		if getDistance() > mind :
			ser.write(b'1\n')
			time.sleep(0.5)
			ser.write(b'7\n')
			continue
		
		#足够近,开始识别
		print('stop')
		
		faceId =face(CAM.read())
		
		if faceId != host_face: 
			print('failed, tring to fine the next face')
			bulingbuling(2)
			#倒车 & 右转向 ->车头左转
			ser.write(b'2\n')
			time.sleep(0.5)
			ser.write(b'6\n')
			time.sleep(0.8)
			ser.write(b'7\n')
			
		else:
			print('找到主人啦,请控制我')
			CAM.set(1)
			bulingbuling(1)
