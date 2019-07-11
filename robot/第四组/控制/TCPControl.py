
import serial
import time
import socket
import sys
sys.path.append('/home/pi/')
import CAM as CAM

ip_port = ('192.168.137.218',7788)     #ip改成服务器上的ip，不能是localhost
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1) 
server.bind(ip_port)
server.listen(1)
ser = serial.Serial("/dev/ttyAMA0",9600)

def controlForward():
	ser.write(b'1\n')
def controlBack():
	ser.write(b'2\n')
def controlUp():
	ser.write(b'3\n')
def controlDown():
	ser.write(b'4\n')
def controlLeft():
	ser.write(b'5\n')
def controlRight():
	ser.write(b'6\n')
def controlStop():
	ser.write(b'7\n')

controlSwitch = {'1':controlForward, '2':controlBack, '3':controlUp, '4':controlDown, '5':controlLeft, '6':controlRight, '7':controlStop}

def tcp():
	con, address = server.accept()
	while 1:
		if_control = CAM.get()
		if(if_control != 1):
			continue
		try:
			msg = con.recv(4)
			print(msg)
			#controlSwitch.get(msg.decode('utf-8'))
			ch=msg.decode('utf-8')
			if ch!='':
				ch=ch.encode()
				ch+=b'\n'
				ser.write(ch)
		except Exception as e:
			break
	server.close()







