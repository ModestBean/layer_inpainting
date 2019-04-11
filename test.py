# -*- coding:utf-8 -*-
import numpy as np
import cv2
imageInputAddress = '.\\data\\width\\width_image.png'
data1 = cv2.imread(imageInputAddress, 0)
data1 = (data1 == 255)
print(data1)
