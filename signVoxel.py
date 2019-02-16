"""
功能：根据骨架对相场模型进行标记
注意：index为索引例如体素索引为68971236，position为 196*198*200  举例：68971236 = 196*198*200
"""
import numpy as np
import imageUtility as utility
import cv2
import os
import time

class SkeletonEdge(object):
    """
    point内容为1~400*400*400
    """
    def __init__(self, label, point, length):
        self.label = label
        self.point = point
        self.length = length

def indexToPosition(voxel):
    """
    功能：索引转换为体素坐标，例如 31267896 = 198 * 193 * 200
    @voxel： 输入为索引，例如31267896
    @return： 输出为[[198,197,200],[201,202,203].....]
    """
    x_pos = np.trunc(voxel / 160000)
    remainder = (voxel % 160000)
    y_pos = np.trunc(remainder / 400)
    z_pos = np.trunc(remainder % 400)
    listTemp = []
    for i in range(len(x_pos)):
        listTemp.append([x_pos[i], y_pos[i], z_pos[i]])
    return listTemp

def calculateMinDistance(onePoint, voxelPosition):
    """
    功能：计算体素距离骨架的最小距离
    @onePoint : 体素坐标
    @voxelPosition : 输入为[[198,197,200],[201,202,203].....]
    @return : float距离最小值
    """
    distance = []
    for one in voxelPosition:
        d = np.linalg.norm(one - onePoint)
        distance.append(d)
    minDistance = min(distance)
    return minDistance

def dyeingAndSectionSkeleton(imageStacks, outputDir, ext=".png"):
    utility.mkoutdir(outputDir)
    w, h, depth = imageStacks.shape
    label_num = len(imageStacks)
    for item in range(label_num):
        image_label = imageStacks[:, :, item]
        image_rgb = np.zeros((w, h, 3))
        image_rgb[image_label == 0] = [0, 0, 0]
        image_rgb[image_label == 1] = [255, 0, 0]
        image_rgb[image_label == 2] = [0, 255, 0]
        image_rgb[image_label == 3] = [0, 0, 255]
        image_rgb[image_label == 4] = [255, 255, 0]
        image_rgb[image_label == 5] = [0, 255, 255]
        image_rgb[image_label == 6] = [255, 0, 255]
        cv2.imwrite(os.path.join(outputDir, str(item + 1).zfill(3) + ".png"), image_rgb)


if __name__ == "__main__":
    # 相场模型原始数据
    modelInputAddress = '.\\data\\original\\mat\\Pha1_00001_value.mat'
    modelStack = utility.getLabelStackFromMat(modelInputAddress)
    # 读取骨架Stack数据
    skelInputAddress = '.\\data\\original\\mat\\Pha1_00001_skel.mat'
    skelStack = utility.getLabelStackFromMat(skelInputAddress)
    # 由方法生成骨架体素数据
    skelPostionInputAddress = '.\\data\\original\\mat\\Pha1_00001_skeleton_postion.mat'
    skelPositionStack = utility.getLabelStackFromMat(skelPostionInputAddress)
    skelPositionStack = skelPositionStack[0, :]

    # 得到骨架对象列表，list[edge0,edge1,edge2........]
    # 每条骨架体素个数
    edge_voxel_num = [30, 30, 27, 30, 31, 33]
    edge_num = len(edge_voxel_num)  # 骨架总数
    edgeList = []  # 骨架列表
    startIndex = 0  # 辅助切割临时变量
    for i in range(edge_num):
        edgeVoxel = skelPositionStack[startIndex: startIndex+edge_voxel_num[i]]  # 数组切割
        startIndex += edge_voxel_num[i]  # 临时变量叠加
        edge = SkeletonEdge(i, edgeVoxel, edge_voxel_num[i])  # 创建骨架对象
        edgeList.append(edge)  # 送入list

    # 计算最小距离并设置标记值
    modelVoxelPosition = np.argwhere(modelStack == 1)  # 体素位置
    labelStack = np.zeros((400, 400, 400))  # 初始化空矩阵
    startTime = time.time()
    for everyPosition in modelVoxelPosition:  # [198, 197, 163]
        allEdgeMinDistance = []
        for i in range(len(edgeList)):
            voxelPosition = indexToPosition(edgeList[i].point)
            d = calculateMinDistance(everyPosition, voxelPosition)
            allEdgeMinDistance.append(d)
        minDistance = min(allEdgeMinDistance)
        edgeIndex = allEdgeMinDistance.index(minDistance)+1
        labelStack[everyPosition[0], everyPosition[1], everyPosition[2]] = edgeIndex
    endTime = time.time()
    print("Erode duration:{}'s".format(endTime - startTime))
    # 生成切片
    outputDir = '.\\result\\slicerColor\\'
    dyeingAndSectionSkeleton(labelStack, outputDir)
