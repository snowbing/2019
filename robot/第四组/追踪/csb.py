#trig 黄 l4
#gnd 蓝 l5
#echo 绿 l6


import time

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

GPIO.setup(4, GPIO.OUT)
GPIO.output(4, GPIO.LOW)

GPIO.setup(17, GPIO.IN)

def getDistance():
		GPIO.output(4, GPIO.HIGH)
		time.sleep(0.00015)
		GPIO.output(4, GPIO.LOW)
		while not GPIO.input(17):
			pass
		t1 = time.time()
		while GPIO.input(17):
			pass
		t2 = time.time()
		return (t2-t1)*340*100/2

try:
    while True:
        print(getDistance())
        time.sleep(2)
except KeyboardInterrupt:
    GPIO.cleanup()