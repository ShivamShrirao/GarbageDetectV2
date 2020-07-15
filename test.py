import cv2
import numpy as np
import matplotlib.pyplot as plt

IMG_SIZE = 320

path = "/home/archer/machine_learning/garbage_detection/garbage_dataset/"
filename,width,height,label,xmin,ymin,xmax,ymax = 'c5e12690-679e-11e5-b0d3-40f2e96c8ad8.jpg',1300,1175,'garbage',128.57142857142856,394.2857142857142,955.7142857142856,1014.2857142857141

img = cv2.imread(path+filename)								# No need to read image btw.

wid_r = IMG_SIZE/width
hgt_r = IMG_SIZE/height

a_xmin = int(wid_r*xmin)
a_xmax = int(wid_r*xmax)
a_ymin = int(hgt_r*ymin)
a_ymax = int(hgt_r*ymax)

img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))

len_grid = IMG_SIZE//20

for y in range(0, IMG_SIZE, len_grid):
	img = cv2.line(img, (0, y), (IMG_SIZE, y), (0, 255, 0), 1, 1)

for x in range(0, IMG_SIZE, len_grid):
	img = cv2.line(img, (x, 0), (x, IMG_SIZE), (0, 255, 0), 1, 1)

img = cv2.rectangle(img, (a_xmin,a_ymin), (a_xmax,a_ymax), (0,0,255), 2)

arr = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

arr = np.asarray(arr, np.float32)
arr[a_ymin:a_ymax,a_xmin:a_xmax][:] = -1

OUT_SIZE = 20
area_thresh = OUT_SIZE*OUT_SIZE/2

label = np.zeros((OUT_SIZE, OUT_SIZE), dtype=np.bool)

idy = 0
for y in range(0, IMG_SIZE, len_grid):
	idx = 0
	for x in range(0, IMG_SIZE, len_grid):
		if (arr[y:y+len_grid, x:x+len_grid] == -1).sum() >= area_thresh:
			label[idy,idx] = True
		idx+=1
	idy+=1

plt.imshow(label)
plt.show()
plt.imshow(img)
plt.show()

cv2.waitKey(0)
cv2.destroyAllWindows()