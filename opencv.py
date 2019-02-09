#/usr/bin/python3

import cv2

img = cv2.imread('samples/blocks_color.jpg',0)
edges = cv2.Canny(img,100,200)
cv2.imwrite("result/opencv.jpg", edges)
