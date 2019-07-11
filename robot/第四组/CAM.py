import cv2
import threading

# flag =1 手动驾驶,语音驾驶
# flag = 0 禁止驾驶
# flag = 2 自动驾驶 -车牌跟踪
# flag = 3 自动驾驶 - 光源跟踪
# flag = 4 

#reason = 2 STOP停止
#reason = 1 红绿灯停止
#reason = 4

#oldControlFlag记录了变0之前的控制方法
class controlFlag:
	flagMutex=threading.Lock()
	__control_flag=1
	__reason = 0
	__oldControlFlag = 1
	def get(self):
		self.flagMutex.acquire()
		i = self.__control_flag
		self.flagMutex.release()
		return i
	def setFlag(self,i):
		self.flagMutex.acquire()
		if self.__control_flag == 0:
			self.__oldControlFlag = i
		else:
			self.__control_flag=i
		self.flagMutex.release()
		print('Set flag to')
		print(self.__control_flag)
		return 0
	def setReason(self,i):
		self.flagMutex.acquire()
		self.__reason|=i
		if self.__reason!= 0 and self.__control_flag!=0:
			self.__oldControlFlag = self.__control_flag
			self.__control_flag = 0
		self.flagMutex.release()
		print('当前停止reason为')
		print(self.__reason)
		print('当前oldControlFlag为')
		print(self.__oldControlFlag)
		print('当前control为')
		print(self.__control_flag)
		return self.__reason
	def removeReason(self,i):  #返回值是能否control_flag
		flag = 0
		self.flagMutex.acquire()
		self.__reason&=~i
		print('当前reason为')
		print(self.__reason)
		print('当前oldControlFlag为')
		print(self.__oldControlFlag)
		print('当前control为')
		print(self.__control_flag)
		if self.__reason == 0:
			if self.__control_flag==0:
				self.__control_flag = self.__oldControlFlag
				flag = self.__control_flag
		self.flagMutex.release()
		return flag
ControlFlag=controlFlag()
class CAM:
	cam=cv2.VideoCapture(0)
	def __init__(self):
		cam.set(3, 320) # set video widht
		cam.set(4, 240) # set video height
def read():
		return CAM.cam
def readi():
		return CAM.cam.read()
def get():
		return ControlFlag.get()
def set(i):  #仅限TCPOrder和找到主人之后使用,检查当前是否是停止状态
		ControlFlag.setFlag(i)
		return 0
def setReason(i):
		return ControlFlag.setReason(i)
		
def removeReason(i):
		return ControlFlag.removeReason(i)