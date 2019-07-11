

from play_audio import play_audio
import time

def output(id_u):
	path='/home/pi/au/output/'
	if id_u==2:
		play_audio(path+'welcome.wav')
		time.sleep(0.1)
		play_audio(path+'wzw.wav')
	elif id_u==1:
		play_audio(path+'welcome.wav')
		time.sleep(0.1)
		play_audio(path+'wqr.wav')
	elif id_u==0:
		play_audio(path+'unknown.wav')
	elif id_u == 3:
		play_audio(path+'byp.wav')
	return
if __name__ == '__main__':
	try:
		output(1)
	except KeyboardInterrupt:
		if ser!=None:
			ser.close()
