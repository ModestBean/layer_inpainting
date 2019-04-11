# -*- coding:utf-8 -*-
"""
功能：绘制曲率直方图
"""

import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import os
import scipy.io as sio

# 读入曲率文本数据
f = open(".\\data\\mean_curvature_vertex.txt")
line = f.readline()
data_list = []
while line:
    num = list(map(float, line.split()))
    data_list.append(num)
    line = f.readline()
f.close()
data_array = np.array(data_list)
column_nums = int(len(data_array)/4)
data_array = data_array.reshape(column_nums, 4)
# # 取得x，y，z列表
x_value = data_array[:, 0]
y_value = data_array[:, 1]
z_value = data_array[:, 2]
# 获得多孔合金极值
min_x = min(x_value)
max_x = max(x_value)
min_y = min(y_value)
max_y = max(y_value)
min_z = min(z_value)
max_z = max(z_value)
print(str(min_x) + '|||' + str(max_x))
print(str(min_y) + '|||' + str(max_y))
print(str(min_z) + '|||' + str(max_z))
# 过滤元素
data_array = data_array[data_array[:, 0] < max_x]
data_array = data_array[data_array[:, 0] > min_x]
data_array = data_array[data_array[:, 1] < max_y]
data_array = data_array[data_array[:, 1] > min_y]
data_array = data_array[data_array[:, 2] < max_z]
data_array = data_array[data_array[:, 2] > min_z]
print(data_array[0])
print(data_array.shape)

# 取得曲率值
quality_value = data_array[:, 3]
newNums = list(filter(lambda x: x <= 3.7, quality_value))
newNums = list(filter(lambda x: x >= -3, newNums))
min_quality = min(newNums)
max_quality = max(newNums)
print(str(min_quality) + '更新后' + str(max_quality))

outputDir = ".\\result\\"
fileName = "mean_curvature_filter.mat"
sio.savemat(os.path.join(outputDir, fileName), {"data": newNums})






