import cv2
import numpy as np
import matplotlib.pyplot as plt

IMG_SIZE = 20

path = "/home/archer/machine_learning/garbage_detection/garbage_dataset/"
garbage = "garbage"
filename,width,height,label,xmin,ymin,xmax,ymax = 'ba01cf5a-679e-11e5-b0d3-40f2e96c8ad8.jpg',636,546,garbage,103.0,306.0,612.0,527.0

img = cv2.imread(path+filename)								# No need to read image btw.
plt.imshow(img)
plt.show()

wid_r = IMG_SIZE/width
hgt_r = IMG_SIZE/height

a_xmin = int(wid_r*xmin)
a_xmax = int(wid_r*xmax)
a_ymin = int(hgt_r*ymin)
a_ymax = int(hgt_r*ymax)

img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))

len_grid = IMG_SIZE//20

# for y in range(0, IMG_SIZE, len_grid):
# 	img = cv2.line(img, (0, y), (IMG_SIZE, y), (0, 255, 0), 1, 1)

# for x in range(0, IMG_SIZE, len_grid):
# 	img = cv2.line(img, (x, 0), (x, IMG_SIZE), (0, 255, 0), 1, 1)

# img = cv2.rectangle(img, (a_xmin,a_ymin), (a_xmax,a_ymax), (255, 0, 0), 1)

arr = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY).astype(np.float32)

arr[a_ymin:a_ymax,a_xmin:a_xmax][:] = -1

OUT_SIZE = 20
# area_thresh = OUT_SIZE*OUT_SIZE * 0.5

# label = np.zeros((OUT_SIZE, OUT_SIZE), dtype=np.bool)

label = (arr == -1)

# idy = 0
# for y in range(0, IMG_SIZE, len_grid):
# 	idx = 0
# 	for x in range(0, IMG_SIZE, len_grid):
# 		iou = (arr[y:y+len_grid, x:x+len_grid] == -1).sum()
# 		if iou >= area_thresh:
# 			label[idy,idx] = True
# 		elif iou > 150:
# 			print(idy, idx, iou)
# 		idx+=1
# 	idy+=1

plt.imshow(img)
plt.imshow(cv2.resize(label.astype(np.uint8), (IMG_SIZE, IMG_SIZE)), alpha=0.3)
plt.show()

cv2.waitKey(0)
cv2.destroyAllWindows()