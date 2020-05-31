# -*- coding: utf-8 -*-
'''
Batch processing of depth iamges in data sets
'''
import os
import pickle
import numpy as np
from get_pose import (
     get_pose,
     get_wTo,
     pose2patch,
)
from get_patch import get_patch

def grasp2pose(grasp_path,save_path):
    '''
    Convert grasp data into pose file
    :param grasp_file:Data format in graspit
    :param save_file:the file to be stored in pose
    :return:
    '''
    f = open(grasp_path,'r')
    grasps = pickle.load(f)
    f.close()
    poses = []
    for grasp in grasps:
        poses.append(grasp.pose)
    f = open(save_path,'w')
    pickle.dump(poses,f,0)
    f.close()

def grasp2dof(grasp_path,save_path):
    '''
    Convert grasp data into pose file
    :param grasp_file:Data format in graspit
    :param save_file:the file to be stored in pose
    :return:
    '''
    f = open(grasp_path,'r')
    grasps = pickle.load(f)
    f.close()
    dofs = []
    for grasp in grasps:
        dofs.append(grasp.dofs)
    f = open(save_path,'w')
    pickle.dump(dofs,f,0)
    f.close()

def save_poseAnddofs():
    '''
    Convert grasp data to pose and dofs
    :return:
    '''
    grasps_pose = []
    grasps_dofs = []
    sum = 0
    data_path = '/home/well/simulation_data/graspit_data/'
    for index in range(65):
        grasp_path = data_path + str(index) + '/'
        grasp_files = os.listdir(grasp_path)
        grasp_files.sort()
    # grasp_files = sorted(grasp_files, key=lambda x: os.path.getmtime(os.path.join(grasp_path, x)))  #  Sorted by file time
        files_num = len(grasp_files)
    # print(files_num)


        for i in range(files_num):
            grasp_file = grasp_path + grasp_files[i]
            print(grasp_file)
            f = open(grasp_file, 'r')
            grasps = pickle.load(f)
            sum += len(grasps)

            for j in range(len(grasps)):
                grasps_pose.append(grasps[j].pose)
                grasps_dofs.append(grasps[j].dofs)
            f.close()
    f = open('/home/well/simulation_data/grasps_pose.txt', 'w')
    pickle.dump(grasps_pose, f, 0)
    f.close()
    f = open('/home/well/simulation_data/grasps_dofs.txt', 'w')
    pickle.dump(grasps_dofs, f, 0)
    f.close()
    print(sum)

def test(index):
    '''
    Test whether the data in graps_pose and grass_dofs corresponds to the data in the grass_data folder
    :param index: index in grasp_pose
    :return:
    '''
    g_index = index
    data_path = '/home/well/simulation_data/graspit_data/'
    sum = 0
    for index in range(65):
        grasp_path = data_path + str(index) + '/'
        grasp_files = os.listdir(grasp_path)
        grasp_files.sort()
    # grasp_files = sorted(grasp_files, key=lambda x: os.path.getmtime(os.path.join(grasp_path, x)))  # Sorted by file time
        files_num = len(grasp_files)

        for i in range(files_num):
            grasp_file = grasp_path + grasp_files[i]
            print(grasp_file)
            f = open(grasp_file, 'r')
            grasps = pickle.load(f)
            sum += len(grasps)
            print(len(grasps))
            f.close()
            if sum < g_index:
                continue
            else:
                sum -= len(grasps)
                print(grasps[g_index-sum-1].pose)
                print(grasps[g_index-sum-1].dofs)
                f = open('/home/well/simulation_data/grasps_pose.txt', 'r')
                poses = pickle.load(f)
                g = open('/home/well/simulation_data/grasps_dofs.txt', 'r')
                dofs = pickle.load(g)

                print(len(poses),len(dofs))
                print(poses[g_index-1],dofs[g_index-1])
                f.close()
                g.close()
                exit()

def get_patches():

    f = open('/home/well/simulation_data/grasps_pose.txt', 'r')
    poses = pickle.load(f)
    f.close()

    sum_index = 0
    patch_size = [128, 64]
    data_path = '/home/well/simulation_data/graspit_data/'
    for index in range(65):
        grasp_path = data_path + str(index) + '/'
        grasp_files = os.listdir(grasp_path)
        grasp_files.sort()
        # grasp_files = sorted(grasp_files, key=lambda x: os.path.getmtime(os.path.join(grasp_path, x)))  # Sorted by file time
        files_num = len(grasp_files)
        # print(files_num)
        length = []
        for i in range(files_num):
            grasp_file = grasp_path + grasp_files[i]
            print(grasp_file)
            f = open(grasp_file, 'r')
            grasps = pickle.load(f)
            f.close()
            length.append(len(grasps))
            print(length)

        depth_path = '/home/well/simulation_data/depth/' + str(index) + '.jpg'
        sdf_path = '/home/well/simulation_data/gazebo_data/sdf_file/o' + str(index) + '.sdf'
        if index < 5:
            wTo = np.array([[0, 0, -1,0],
                            [-1, 0, 0,0],
                            [0, 1, 0,0],
                            [0, 0, 0,1]])
        # Since the 0 to 4 models are drawn by hand, their object coordinate and the world coordinate in gazebo are coincident
        else:
            wTo = get_wTo(sdf_path)
        sum_length = sum(length)
        for j in range(sum_length):
            pose = get_pose(poses[sum_index+j])
            center, angle = pose2patch(pose,wTo)
            img = get_patch(depth_path,angle,center,patch_size)
            save_path = '/home/well/simulation_data/patches/' +str(index) +'/' +str(j) + '.jpg'
            img.save(save_path)
        sum_index += sum_length

def getPatches(patch_size,pose_file,index,depth_path='/home/well/simulation_data/depth/',save_path='/home/well',sdf_path='/home/well/simulation_data/gazebo_data/sdf_file/o'):
    '''
   This is written for the data set.If it is for testing purposes, remember to modify the condition of index <
   since the test set is generated by yourself, so we don't need get_wTo (sdf_path)
    :param patch_size:
    :param pose_file:
    :param index:
    :param depth_path:
    :param save_path:
    :param sdf_path:
    :return:
    '''
    f = open(pose_file, 'r')
    poses = pickle.load(f)
    f.close()

    patch_size = patch_size
    depth_path = depth_path + str(index) + '.jpg'
    sdf_path = sdf_path + str(index) + '.sdf'
    if index < 5:
        wTo = np.array([[0, 0, -1, 0],
                            [-1, 0, 0, 0],
                            [0, 1, 0, 0],
                            [0, 0, 0, 1]])
     # Since the 0 to 4 models are drawn by hand, their object coordinate and the world coordinate in gazebo are coincident
    else:
        wTo = get_wTo(sdf_path)
    for i,j in enumerate(poses):
        pose = get_pose(j)
        center, angle = pose2patch(pose, wTo)
        angle = 0 # only for test5
        center[1] -= 50 # only for test5
        img = get_patch(depth_path, angle, center, patch_size)
        dir_path = save_path + str(index) + '/'
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        path = dir_path + str(i) + '.jpg'
        img.save(path)

def getZerosPatches():
    patch_size = [200, 200]
    pose_file = '/home/well/simulation_data3.0/modify_grasps/poses/65.txt'
    f = open(pose_file, 'r')
    poses = pickle.load(f)
    f.close()

    for index, j in enumerate(poses):
        depth_path = '/home/well/simulation_data3.0/test5/train_dataset2.0/depth/65.jpg'
        sdf_path = '/home/well/simulation_data/gazebo_data/sdf_file/o' + str(index) + '.sdf'
        if index < 5:
            wTo = np.array([[0, 0, -1, 0],
                        [-1, 0, 0, 0],
                        [0, 1, 0, 0],
                        [0, 0, 0, 1]]) 
        # Since the 0 to 4 models are drawn by hand, their object coordinate and the world coordinate in gazebo are coincident
        else:
            wTo = get_wTo(sdf_path)

        pose = get_pose(j)
        center, angle = pose2patch(pose, wTo)
        img = get_patch(depth_path, angle, center, patch_size)
        path = '/home/well/simulation_data3.0/test5/train_dataset2.0/depth_patches/65/' + str(index)+'.jpg'
        img.save(path)

def test2():
    patch_size = [128, 64]
    pose_path = '/home/well/simulation_data3.0/test2/poses/3.txt'
    getPatches(patch_size,pose_path,3,depth_path='/home/well/simulation_data3.0/test2/new_depth/',
               sdf_path='/home/well/simulation_data3.0/test2/o',
               save_path='/home/well/simulation_data3.0/test2/patches/')

def test3():
    patch_size = [128, 64]
    pose_path = '/home/well/simulation_data3.0/test3/poses/3.txt'
    getPatches(patch_size,pose_path,3,depth_path='/home/well/simulation_data3.0/test3/new_depth/',
               sdf_path='/home/well/simulation_data3.0/test3/o',
               save_path='/home/well/simulation_data3.0/test3/patches/')

def test1():
    patch_size = [100, 40]
    pose_path = '/home/well/simulation_data1.0/test1/1/pose.txt'
    getPatches(patch_size,pose_path,0,depth_path='/home/well/simulation_data1.0/test2/depth/',
               sdf_path='/home/well/simulation_data1.0/test2/o',
               save_path='/home/well/simulation_data2.0/test2/old_patches/')

def test4():
    patch_size = [128, 64]
    pose_path = '/home/well/simulation_data3.0/test4/hand_poses.txt'
    getPatches(patch_size, pose_path, 3, depth_path='/home/well/simulation_data3.0/test4/depth/',
               sdf_path='/home/well/simulation_data3.0/test2/o',
               save_path='/home/well/simulation_data3.0/test4/patches/')

def test5():

    for i in range(4):
        patch_size = [200, 200]
        pose_path = '/home/well/simulation_data3.0/test2/poses/' + str(i) + '.txt'
        getPatches(patch_size, pose_path, i, depth_path='/home/well/simulation_data3.0/test5/test_dataset2.0/depth/',
               sdf_path='/home/well/simulation_data3.0/test2/o',
               save_path='/home/well/simulation_data3.0/test5/test_dataset2.0/depth_patches/')


def sim5_train():
    patch_size = [200, 200]
    for i in range(65):
        pose_file = '/home/well/simulation_data5.0/bad_hand_pose/' + str(i) + '.txt'
        getPatches(patch_size,pose_file,i,depth_path='/home/well/simulation_data5.0/new_depthes/',
              sdf_path='/home/well/simulation_data/gazebo_data/sdf_file/o',
              save_path='/home/well/simulation_data5.0/bad_depth_patches/')

if __name__ == '__main__':
    # getZerosPatches()
    # patch_size = [100,40]
    # for i in range(65):
    #    pose_file = '/home/well/simulation_data3.0/modify_grasps/poses/' + str(i) + '.txt'
    #    getPatches(patch_size,pose_file,i,depth_path='/home/well/simulation_data3.0/new_depthes/',
    #               sdf_path='/home/well/simulation_data/gazebo_data/sdf_file/o',
    #               save_path='/home/well/simulation_data3.0/100*40patches/')

    #sim5_train()
    # test5()
#test5,train_data
    # patch_size = [200,200]
    # for i in range(65):
    #    pose_file = '/home/well/simulation_data3.0/modify_grasps/poses/' + str(i) + '.txt'
    #    getPatches(patch_size,pose_file,i,depth_path='/home/well/simulation_data3.0/new_depthes/',
    #               sdf_path='/home/well/simulation_data/gazebo_data/sdf_file/o',
    #               save_path='/home/well/simulation_data5.0/good_depth_patches/')
    #sim5 test_data
    patch_size = [200,200]
    for i in range(4):
       pose_file = '/home/well/simulation_data3.0/test2/poses/' + str(i) + '.txt'
       getPatches(patch_size,pose_file,i,depth_path='/home/well/simulation_data3.0/test2/new_depth/',
                  sdf_path='/home/well/simulation_data3.0/test2/o',
                  save_path='/home/well/simulation_data5.0/test_depth_patches/')
    # test2()
    # test4()
    # get_patches()
    # save_poseAnddofs()
    # test(28)
    # file_path = '/home/well/simulation_data/graspit_data/8.txt'
    # f = open(file_path, 'r')
    # grasps = pickle.load(f)
    # wTo = get_wTo('/home/well/simulation_data/gazebo_data/sdf_file/o8.sdf')
    # pose = get_pose(grasps[0])
    # center, angle = pose2patch(pose,wTo)
    # print center,angle
    #
    # f=open('/home/well/simulation_data2.0/test2/graspit_data/2.txt','rb')
    # graspit = pickle.load(f)
    # f.close()
    # print len(graspit)
    # f=open('/home/well/simulation_data2.0/test2/graspit_data/more/2.txt','rb')
    # graspit += pickle.load(f)
    # f.close()
    # print len(graspit)
    # f = open('/home/well/simulation_data2.0/test2/graspit_data/2.txt','w')
    # pickle.dump(graspit,f,0)
    # f.close()
    exit()
