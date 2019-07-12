import serial
import time

ser = serial.Serial("/dev/ttyAMA0",9600)

def control(cmd):
	#ch=input()
	if(cmd == 0):
		return
	ch=str(cmd)
	print('control:')
	print(ch)
	ch=ch.encode()
	ch+=b'\n'
	ser.write(ch)

# if __name__ == '__main__':
# 	try:
# 		control()
# 	except KeyboardInterrupt:
# 		if ser!=None:
# 			ser.close()
