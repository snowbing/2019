
import socket


import sys
sys.path.append('/home/pi/')
import CAM as CAM
ip_port = ('192.168.137.218',8899)     #ip改成服务器上的ip，不能是localhost
BUFSIZE = 1024   #一次接受的字节数
def order():
	while True:
		server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1) 
		server.bind(ip_port)
		server.listen(1)
		conn, address = server.accept()
		try:
			msg = conn.recv(BUFSIZE)
			order = int(msg.decode('utf-8'))
			CAM.set(order)
			print(CAM.get())
		except ConnectionResetError as e:
			print(e)
		conn.close()
		server.close()
	return 0





