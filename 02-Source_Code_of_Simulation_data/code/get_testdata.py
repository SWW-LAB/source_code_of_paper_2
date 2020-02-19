# -*- coding:utf-8 -*-
import pickle
import os
from get_pose import get_pose,get_wTo,pose2patch
from get_patch import get_patch

def index2num(index):
    '''
    从总的下标到模型序列号的转换
    :param index: 总的下标
    :return: 模型序列号
    '''
    sum_num = -1
    for i in range(65):
        dir_path = '/home/well/simulation_data/patches/' + str(i) + '/'
        files = os.listdir(dir_path)
        files_num = len(files)
        sum_num += files_num
        if sum_num < index:
            continue
        else:
            return i

def get_testdata(index, model,save_path):
    '''
    生成测试样本
    :param index: 选择的抓取位姿
    :param model: 选择的模型
    :return: zxyzw
    '''
    index = index  # 选择的抓取位姿
    num = index2num(index)
    model = model  # 选择的模型
    if num == model:
        print('num is model,please input new model')
        model += 1
        if model == 65:
            model -= 2
    pose_file = open('/home/well/simulation_data/grasps_pose.txt', 'rb')
    poses = pickle.load(pose_file)
    pose_file.close()
    pose = get_pose(poses[index])
    zxyzw = []
    zxyzw.append(poses[index].position.z)
    zxyzw.append(poses[index].orientation.x)
    zxyzw.append(poses[index].orientation.y)
    zxyzw.append(poses[index].orientation.z)
    zxyzw.append(poses[index].orientation.w)

    sdf_path = '/home/well/simulation_data/gazebo_data/sdf_file/o' + str(model) + '.sdf'
    wTo = get_wTo(sdf_path)
    center, angle = pose2patch(pose, wTo)

    #origin_depth = '/home/well/simulation_data/depth/' + str(num) + '.jpg'
    depth_path = '/home/well/simulation_data/depth/' + str(model) + '.jpg'
    patch_size = [128, 64]
    #o_img = get_patch(origin_depth, angle, center, patch_size)
    img = get_patch(depth_path, angle, center, patch_size)
    img.save(save_path)
    #o_img.save('/home/well/simulation_data/test/origin.jpg')

    return zxyzw


if __name__=='__main__':
    index = 740 #选择的抓取位姿
    num = index2num(index)
    print(num)
    model = 49 #选择的模型

    pose_file =open('/home/well/simulation_data/grasps_pose.txt','rb')
    poses = pickle.load(pose_file)
    pose_file.close()
    pose = get_pose(poses[index])
    print(poses[index])
    zxyzw = []
    zxyzw.append(poses[index].position.z)
    zxyzw.append(poses[index].orientation.x)
    zxyzw.append(poses[index].orientation.y)
    zxyzw.append(poses[index].orientation.z)
    zxyzw.append(poses[index].orientation.w)
    print(zxyzw)

    sdf_path = '/home/well/simulation_data/gazebo_data/sdf_file/o' + str(num) + '.sdf'
    wTo = get_wTo(sdf_path)
    center, angle = pose2patch(pose, wTo)

    origin_depth = '/home/well/simulation_data/depth/' + str(num) + '.jpg'
    depth_path = '/home/well/simulation_data/depth/' + str(model) + '.jpg'
    patch_size = [128, 64]
    o_img = get_patch(origin_depth, angle, center, patch_size)
    img = get_patch(depth_path, angle, center, patch_size)
    save_path = '/home/well/simulation_data/test/0.jpg'
    img.save(save_path)
    o_img.save('/home/well/simulation_data/test/origin.jpg')
