import cv2
import sys
from udp_streamer import *
from imutils.video import VideoStream
from time import sleep

IP=sys.argv[1]
PORT=int(sys.argv[2])
fps = 30
tdiff = 1/fps

handler = udp_handler()

# cam = cv2.VideoCapture(0)
cam = cv2.VideoCapture('../garbage_detection/vid.mp4')

# handler.connect(IP,PORT)

while cam.isOpened():
	ret,img = cam.read()
	if not ret:
		print("video finished.")
		break
	try:
		ret,img = cam.read()
		img = cv2.resize(img, (320, 320))
		encoded, enimg = cv2.imencode('.jpg',img)
		handler.send_data(enimg,IP,PORT)
	except KeyboardInterrupt:
		cam.release()
		cv2.destroyAllWindows()
		break
	except Exception as e:
		pass
	sleep(tdiff)

cam.release()
handler.close()