"""
功能：根据骨架对相场模型进行标记
注意：index为索引例如体素索引为68971236，position为 196*198*200  举例：68971236 = 196*198*200
"""
import numpy as np
import imageUtility as utility
import random
import cv2

# def dyeingAndSection(imageStacks, outputDir, ext=".png"):
#     w, h, depth = imageStacks.shape
#     label_num = len(imageStacks)
#     color_list = []
#     while len(color_list) < label_num:
#         R = random.randint(1, 255)
#         G = random.randint(1, 255)
#         B = random.randint(1, 255)
#         RGB = str(R) + "," + str(G) + "," + str(B)
#         color_list.append(RGB)  # ['198,2,243', '171,30,224', '219,21,204', '3,34,254',
#         # 去重复
#         color_list = list({}.fromkeys(color_list).keys())  # ['83,141,49', '127,181,148', '239,247,145', '128,66,223', '243,69,87'
#
#     image_gray = np.argwhere(imageStacks[:, :, 0] == 1)
#     utility.mkoutdir(outputDir)
#     for i in range(depth):
#         image_label = imageStacks[:, :, i]
#         image_rgb = np.zeros((w, h, 3))
#         image_rgb[image_label == 1] = np.array([1, 0, 0])
#         image_rgb[image_label == 0] = np.array([0, 1, 0])
#         fileName = str(i).zfill(3) + ext
#         cv2.imwrite(outputDir + fileName, image_rgb)


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

if __name__ == "__main__":
    modelInputAddress = '.\\data\\original\\mat\\Pha1_00001_value.mat'
    modelStack = utility.getLabelStackFromMat(modelInputAddress)
    skelInputAddress = '.\\data\\original\\mat\\Pha1_00001_skel.mat'
    skelStack = utility.getLabelStackFromMat(skelInputAddress)
    skelPostionInputAddress = '.\\data\\original\\mat\\Pha1_00001_skeleton_postion.mat'
    skelPositionStack = utility.getLabelStackFromMat(skelPostionInputAddress)
    skelPositionStack = skelPositionStack[0, :]

    # 得到骨架对象列表，list
    # 每条骨架体素个数
    edge_voxel_num = [30, 30, 27, 30, 31, 33]
    edge_num = len(edge_voxel_num)  # 骨架总数
    edgeList = []  # 骨架列表
    startIndex = 0 # 辅助切割临时变量
    for i in range(edge_num):
        edgeVoxel = skelPositionStack[startIndex: startIndex+edge_voxel_num[i]]  # 数组切割
        startIndex += edge_voxel_num[i]  # 临时变量叠加
        edge = SkeletonEdge(i, edgeVoxel, edge_voxel_num[i])  # 创建骨架对象
        edgeList.append(edge)  # 送入list


    # 计算最小距离
    # 体素位置
    modelVoxelPosition = np.argwhere(modelStack == 1)  # 此示例为69476个
    voxelLabel = []  # 体素标记
    voxelIndex = []  # 体素索引

    for everyPosition in modelVoxelPosition:
        allEdgeMinDistance = []
        for i in range(len(edgeList)):
            voxelPosition = indexToPosition(edgeList[i].point)
            d = calculateMinDistance(everyPosition, voxelPosition)
            allEdgeMinDistance.append(d)
        minDistance = min(allEdgeMinDistance)
        edgeIndex = allEdgeMinDistance.index(minDistance)
        # 存入列表
        voxelLabel.append(edgeIndex)
        index = everyPosition[0]*everyPosition[1]*everyPosition[2]
        voxelIndex.append(index)
    print(voxelLabel)
    # print(voxelIndex)
