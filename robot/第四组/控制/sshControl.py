import serial
import time

ser = serial.Serial("/dev/ttyAMA0",9600)

def main():
	while True:
		ch=input()
		
		ch=ch.encode()
		ch+=b'\n'
		ser.write(ch)

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		if ser!=None:
			ser.close()
