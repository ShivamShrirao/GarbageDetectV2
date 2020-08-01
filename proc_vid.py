import tensorflow as tf
import numpy as np
import cv2
from time import time

IMG_HEIGHT = 320
IMG_WIDTH = 320

tflite_path = 'new_model_0_75/my_model_fp32.tflite'
tflite_interpreter = tf.lite.Interpreter(model_path=tflite_path)
tflite_interpreter.allocate_tensors()
tflite_input_details = tflite_interpreter.get_input_details()
tflite_output_details = tflite_interpreter.get_output_details()

cam = cv2.VideoCapture('../garbage_detection/drone2.mp4')
fps = 30#round(cam.get(cv2.CAP_PROP_FPS))
# writer = cv2.VideoWriter('sdout3.mp4',cv2.VideoWriter_fourcc(*'mp4v'), fps,(IMG_WIDTH,IMG_HEIGHT))

cv2.namedWindow("output", cv2.WINDOW_NORMAL)
cv2.resizeWindow("output", 1200,600)

start = time()
counter = 0
while cam.isOpened():
    ret, img = cam.read()
    if not ret:
        print("video finished.")
        break
    # img = cv2.rotate(img,cv2.ROTATE_90_CLOCKWISE)
    # img = np.ascontiguousarray(img)
    oimg = cv2.resize(img, (IMG_HEIGHT, IMG_WIDTH))
#     cv2.imshow("output",oimg)
    img = cv2.cvtColor(oimg, cv2.COLOR_BGR2RGB).astype(np.float32)
    img/= 255
    tflite_interpreter.set_tensor(tflite_input_details[0]['index'], np.expand_dims(img, axis=0))
    tflite_interpreter.invoke()
    pred = tflite_interpreter.get_tensor(tflite_output_details[0]['index']).squeeze()
    pred[pred<0.5] = 0
    pred[pred>=0.5] = 1
    pred = (pred*255).astype(np.uint8)
    mask = cv2.resize(pred, (IMG_WIDTH, IMG_HEIGHT))
    # contours,_ = cv2.findContours(mask,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # temp = oimg.copy()
    # if len(contours) > 0:
    #     c = max(contours,key=cv2.contourArea)
    #     if cv2.contourArea(c)>100:
    #         #Getting the bounding rectangle
    #         x,y,w,h = cv2.boundingRect(c)
    #         #Drawing the bounding rectangle
    #         cv2.rectangle(temp,(x,y),(x+w,y+h),(0,255,0),2)
    #         #Getting the moments
    #         m = cv2.moments(c)
    #         #moving mouse to the centroid
    # # cv2.drawContours(temp,contours,-1,(255,0,0),2)
    # cv2.imshow("output",temp)
    # mult = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)*img
    heatmap_img = cv2.applyColorMap(mask, cv2.COLORMAP_JET)
    heated = cv2.addWeighted(heatmap_img, 0.3, oimg, 1, 0)
    cv2.imshow("output", np.concatenate((heated, heatmap_img), axis=1))
    counter+=1
    if (time() - start) > 1:
        print("FPS: ", counter / (time() - start))
        counter = 0
        start = time()
    # writer.write(heated)
    key = cv2.waitKey(1) & 0xff
    if key == ord('q'):
        break

cv2.destroyAllWindows()
# writer.release()
cam.release()