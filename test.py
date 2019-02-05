def dyeingAndSection(saveRoad, imageStacks):
    '''
    功能：对标记的三维结构进行染色，给每个晶粒分配一个独特的颜色，然后将三维结构切片，每一层截面图片按照label染上相应的颜色，生成RGB图像，用于后续的可视化。首先生成与晶粒个数相等个数的颜色，然后进行颜色分配和切片。
    :param saveRoad: 生成的系列rgb图像保存地址，最好为绝对地址
    :param imageStacks: 待处理的三维结构，是一个三维标记数组，其中值相同的像素点为同一个晶粒 [w, h, depth]
    :return: "success"
    '''
    #     print(saveRoad)
    w, h, depth = imageStacks.shape

    labels = np.unique(imageStacks)  # [1, 2, 3, 4, 5]
    labels = list(map(str, labels))  # ['1', '2', '3', '4', '5']
    label_num = len(labels)

    # 生成不重复的颜色序列
    color_list = []
    while len(color_list) < label_num:
        R = random.randint(1, 255)
        G = random.randint(1, 255)
        B = random.randint(1, 255)
        RGB = str(R) + "," + str(G) + "," + str(B)
        color_list.append(RGB)
        color_list = list({}.fromkeys(color_list).keys())

    # 给每个晶粒分配一个独特的颜色
    label_color_dict = dict(zip(labels,
                                color_list))  # {'1': '113,148,191', '2': '171,242,3', '3': '198,243,70', '4': '226,150,130', '5': '6,186,66'}

    # 切片
    for item in range(0, depth):
        image_label = imageStacks[:, :, item]
        image_label_num = np.unique(image_label)
        #         print(image_label_num)
        image_rgb = np.zeros((w, h, 3))
        for num in image_label_num:
            image_rgb[image_label == num] = label_color_dict[str(num)].split(",")  # ['113', '148', '191']
        image_rgb[image_label == 0] = [0, 0, 0]
        cv2.imwrite(os.path.join(saveRoad, str(item + 1).zfill(3) + ".png"), image_rgb)

    return "success"