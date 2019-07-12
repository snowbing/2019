#coding:utf-8
import sys
sys.path.append('/home/pi/face/')
sys.path.append('/home/pi/au/output')
sys.path.append('/home/pi/au/')
sys.path.append('/home/pi/sign')
sys.path.append('/home/pi/tcp')
sys.path.append('/home/pi/track/')
from recognition import face
from face_au import *
from one_sentence import au_control
from sign import *
from TCPControl import *
from TCPOrder import *
from find_face import find_face
from detect_light import *
#from client import video

import threading
import cv2
import CAM as CAM







#//红外/超声波/STOP控制了control_flag不让车前进

#//也是一个wait-signal
#orderThread=threading.Thread(target=getOrderFromAndroid)
#def getOrderFromAndroid:
#	if control_flag.get():
#		switch order:
#			case getControlFromAndroid()//手动控制或者重力感应
#			case autoControl()//在里面也要实时监测control_flag以夺回控制权
#			case 倒车入库()

			
def main():

	
	person = -1	#谁在驾驶
	recordingThread=threading.Thread(target=au_control)
	#stopDetectionThread=threading.Thread(target=sign)
	#lightThread=threading.Thread(target=light)
	TCPControlThread=threading.Thread(target=tcp)
	TCPOrderThread=threading.Thread(target=order)
	#VideoThread = threading.Thread(target=video)
	names = ['unknow', 'wuqiurun', 'wangziwei', 'baiyunpeng', 'Z', 'W'] 
	
	
	
	while person == -1:
		person = face(CAM.read())
		if person == 0:
			print(names[person])
			output(person)
			person = -1
	print(names[person])
	#VideoThread.start()
	TCPOrderThread.start()
	TCPControlThread.start()
	output(person)
	findFaceThread=threading.Thread(target=find_face,args=(int(person),))
	findFaceThread.start()
	#stopDetectionThread.start()
	#lightThread.start()
	recordingThread.start()
	while True:
		
		ch=input()
		if(ch == 'q'):
			break;
			
if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		if ser!=None:
			ser.close()
