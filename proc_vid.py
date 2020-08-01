import tensorflow as tf
import numpy as np
import cv2


IMG_HEIGHT = 640
IMG_WIDTH = 640

tflite_path = 'new_model_0_75/my_model_fp32_640x640.tflite'
tflite_interpreter = tf.lite.Interpreter(model_path=tflite_path)
tflite_interpreter.allocate_tensors()
tflite_input_details = tflite_interpreter.get_input_details()
tflite_output_details = tflite_interpreter.get_output_details()

cam = cv2.VideoCapture('../garbage_detection/drone1.mp4')
fps = 30#round(cam.get(cv2.CAP_PROP_FPS))
writer = cv2.VideoWriter('dout1.mp4',cv2.VideoWriter_fourcc(*'mp4v'), fps,(IMG_WIDTH,IMG_HEIGHT))

cv2.namedWindow("output", cv2.WINDOW_NORMAL)
cv2.resizeWindow("output", 600,600)

while cam.isOpened():
    ret, img = cam.read()
    if not ret:
        print("video finished.")
        break
    oimg = cv2.resize(img, (IMG_HEIGHT, IMG_WIDTH))
#     cv2.imshow("output",oimg)
    img = cv2.cvtColor(oimg, cv2.COLOR_BGR2RGB).astype(np.float32)
    img/= 255
    tflite_interpreter.set_tensor(tflite_input_details[0]['index'], np.expand_dims(img, axis=0))
    tflite_interpreter.invoke()
    pred = tflite_interpreter.get_tensor(tflite_output_details[0]['index']).squeeze()
#     pred[pred<0.9] = 0
    pred = (pred*255).astype(np.uint8)
    mask = cv2.resize(pred, img.shape[1::-1])
#     mult = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)*img
    heatmap_img = cv2.applyColorMap(mask, cv2.COLORMAP_INFERNO)
    heated = cv2.addWeighted(heatmap_img, 0.3, oimg, 1, 0)
    cv2.imshow("output", heated)
    writer.write(heated)
    key = cv2.waitKey(1) & 0xff
    if key == ord('q'):
        break

cv2.destroyAllWindows()
writer.release()
cam.release()