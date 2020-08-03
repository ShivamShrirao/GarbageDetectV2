import tensorflow as tf
import numpy as np
import cv2
from time import time
from udp_streamer import *
from threading import Thread

IMG_HEIGHT = 320
IMG_WIDTH = 320

handler = udp_handler()
handler.make_listener('0.0.0.0',5555)

# tflite_path = 'new_model_0_75/my_model_fp32.tflite'
tflite_path = 'new_model_0_75_-1to1/my_model_fp32_320x320.tflite'
tflite_interpreter = tf.lite.Interpreter(model_path=tflite_path)
tflite_interpreter.allocate_tensors()
tflite_input_details = tflite_interpreter.get_input_details()
tflite_output_details = tflite_interpreter.get_output_details()

# cam = cv2.VideoCapture('../garbage_detection/vid.mp4')
fps = 40#round(cam.get(cv2.CAP_PROP_FPS))
# writer = cv2.VideoWriter('segout_bb2.mp4',cv2.VideoWriter_fourcc(*'mp4v'), fps,(IMG_WIDTH,IMG_HEIGHT))

cv2.namedWindow("output", cv2.WINDOW_NORMAL)
cv2.resizeWindow("output", 600,600)

def get_img():
	global handler,oimg
	buffer = handler.get_data()
	if buffer is not None:
		try:
			npimg = np.frombuffer(buffer, dtype=np.uint8)
			oimg = cv2.imdecode(npimg, 1)
		except Exception as e:
			print(e)

buffer = handler.get_data_small()
oimg=prev_img=None
try:
	npimg = np.frombuffer(buffer, dtype=np.uint8)
	oimg = cv2.imdecode(npimg, 1)
except:
	pass

start = time()
counter = 0
while True:
	get_img()
	if id(oimg)==id(prev_img):
		continue
	if oimg is None:
		continue
	# oimg = cv2.rotate(oimg,cv2.ROTATE_90_CLOCKWISE)
	# oimg = np.ascontiguousarray(oimg)
	oimg = cv2.resize(oimg, (IMG_HEIGHT, IMG_WIDTH)).astype(np.uint8)
#     cv2.imshow("output",oimg)
	img = cv2.cvtColor(oimg, cv2.COLOR_BGR2RGB).astype(np.float32)
	img = img/127.5 - 1
	tflite_interpreter.set_tensor(tflite_input_details[0]['index'], np.expand_dims(img, axis=0))
	tflite_interpreter.invoke()
	pred = tflite_interpreter.get_tensor(tflite_output_details[0]['index']).squeeze()
	pred[pred<0.86] = 0
	# pred[pred>=0.5] = 1
	pred = (pred*255).astype(np.uint8)
	mask = cv2.resize(pred, (IMG_WIDTH, IMG_HEIGHT))
	# mult = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)#*img
	# mult[:,:,0] = 0
	# mult[:,:,2] = 0
	# heatmap_img = mult
	heatmap_img = cv2.applyColorMap(mask, cv2.COLORMAP_INFERNO)
	heated = cv2.addWeighted(heatmap_img, 0.6, oimg, 1, 0)
	cv2.putText(heated, str(fps)[:5]+" FPS", (0, 15),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,255), 1)
	contours,_ = cv2.findContours(mask,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	if len(contours) > 0:
		c = max(contours,key=cv2.contourArea)
		cArea = cv2.contourArea(c)
		if cArea > 2900:
			#Getting the bounding rectangle
			# x,y,w,h = cv2.boundingRect(c)
			#Drawing the bounding rectangle
			# cv2.rectangle(heated,(x,y),(x+w,y+h),(0,255,0),2)
			# min rect
			rect = cv2.minAreaRect(c)
			box = cv2.boxPoints(rect)
			box = np.int0(box)
			cv2.drawContours(heated,[box],0,(0,255,0),2)
			#Getting the moments
			# m = cv2.moments(c)
			#moving mouse to the centroid
	# # cv2.drawContours(heated,contours,-1,(255,0,0),2)
	# cv2.imshow("output",heated)
	cv2.imshow("output", heated)
	# cv2.imshow("output", np.concatenate((heated, heatmap_img), axis=1))
	counter+=1
	if (time() - start) > 1:
		fps = counter / (time() - start)
		# print("FPS:", fps)
		counter = 0
		start = time()
	# writer.write(heated)
	key = cv2.waitKey(1) & 0xff
	if key == ord('q'):
		break

cv2.destroyAllWindows()
# cam.release()
# writer.release()