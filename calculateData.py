#-*- coding:utf-8 -*
"""
功能：相场模型三维特征分析，计算枝晶长度、宽度等
"""
import imageUtility as utility
import numpy as np
if __name__ == "__main__":
    # 相场模型原始数据
    modelInputAddress = '.\\data\\mat\\Pha1_00001_value.mat'
    modelStack = utility.getLabelStackFromMat(modelInputAddress)
    labelInputAddress = '.\\data\\mat\\Pha1_00001_label.mat'
    labelStack = utility.getLabelStackFromMat(labelInputAddress)
    allLabel = []
    centerPosition = [198, 202, 197]
    for x in range(6):
        labelIndex = np.argwhere(labelStack[:, 3] == (x+1))
        allLabel.append(labelIndex)
    allMaxLength = []
    for oneLabel in allLabel:
        allDistance = []
        for onePoint in oneLabel:
            x = labelStack[onePoint, 0]
            y = labelStack[onePoint, 1]
            z = labelStack[onePoint, 2]
            everyPoint = np.array([x, y, z])
            d = np.linalg.norm(centerPosition - everyPoint)
            allDistance.append(d)
        maxLength = max(allDistance)
        allMaxLength.append(maxLength)
    print(allMaxLength)





