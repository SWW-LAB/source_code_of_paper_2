# coding:utf-8

import pickle
import numpy as np
import math
import re
from geometry_msgs.msg import Pose
from graspit_interface.msg import (
    Body,
    Energy,
    GraspableBody,
    Grasp,
    Planner,
    Robot,
    SearchContact,
    SearchSpace,
    SimAnnParams,
    PlanGraspsAction,
    PlanGraspsGoal
)

def get_pose(pose):
    '''
    :param grasp: 一次抓取的pose
    :return: 手掌坐标系相对于世界坐标系的转换矩阵
    '''
    orientation = pose.orientation
    position = pose.position

    quat = [orientation.x, orientation.y, orientation.z, orientation.w]
    wRh = quat2rotm(quat)

    trans = np.array([position.x, position.y, position.z])
    trans.transpose()
    trans.shape = (3,1)

    wTh = np.concatenate((wRh, trans), axis=1)
    temp = np.array([0, 0, 0, 1])
    temp.shape = (1,4)
    wTh = np.concatenate((wTh, temp), axis=0)  #graspit中灵巧手相对于世界坐标系的转换矩阵
    hTp = np.array([[1, 0, 0, 0.068],
                    [0, 1, 0, -0.020],
                    [0, 0, 1, 0.012],
                    [0, 0, 0, 1]])            #手掌坐标系相对于灵巧手坐标系的转换矩阵
    wTp = np.dot(wTh, hTp)
    return wTp  #手掌坐标系相对于世界坐标系(物体坐标系)oTp

def get_hand_pose(pose):
    '''
    手掌坐标到手坐标的转换
    :param pose:手掌的pose
    :return:graspit中手的pose
    '''
    orientation = pose.orientation
    position = pose.position

    quat = [orientation.x, orientation.y, orientation.z, orientation.w]
    wRp = quat2rotm(quat)

    trans = np.array([position.x, position.y, position.z])
    trans.transpose()
    trans.shape = (3, 1)

    wTp = np.concatenate((wRp, trans), axis=1)
    temp = np.array([0, 0, 0, 1])
    temp.shape = (1, 4)
    wTp = np.concatenate((wTp, temp), axis=0)  # graspit中灵巧手手掌相对于世界坐标系的转换矩阵
    pTh = np.array([[1, 0, 0, -0.068],
                    [0, 1, 0, 0.020],
                    [0, 0, 1, -0.012],
                    [0, 0, 0, 1]])  # 手坐标系相对于灵巧手掌坐标系的转换矩阵
    wTh = np.dot(wTp, pTh)
    return wTh  # 手坐标系相对于世界坐标系(物体坐标系)oTh

#从文件中获取物体坐标系相对于世界坐标系的转换矩阵,注意前5种自己画的模型的wTo是单位矩阵
def get_wTo(file_path):
    '''
    :param file_path: 物体的sdf文件位置
    :return: wTo,物体坐标系相对于世界坐标系的转换矩阵
    '''
    wTo = np.array([[0,0,-1],
                    [-1,0,0],
                    [0,1,0],
                    [0,0,0]])# 需要从物体的sdf文件中读取
    with open(file_path,'r') as f:
        line = f.readline()
        while 'pose' not in line:
            line = f.readline()
    trans = list(map(float, re.findall(r"-?\d+\.?\d*", line)))[:3]
    trans.append(1)
    trans = np.array(trans)
    trans.transpose()
    trans.shape = (4,1)
    wTo = np.concatenate((wTo,trans),axis=1)
    return wTo



def pose2patch(pose,wTo):
    '''
    :param pose: 手掌坐标系相对于世界坐标系的转换矩阵,以及gazebo中物体坐标系相对于世界坐标系的转换矩阵
    :return: patch的中心位置和角度
    '''

    iTc = np.array([[554.254691191187, 0.0, 320.5, -0.0],
                    [0.0, 554.254691191187, 240.5, 0.0],
                    [0.0, 0.0, 1.0, 0.0],
                    [0,0,0,1]]) #内参矩阵没问题

    csimTc = np.array([[0,0,1,0],
                       [-1,0,0,0],
                       [0,-1,0,0],
                       [0,0,0,1]])   #也没有问题
    #
    # wTcsim = np.array([[-0.9991, 0.0005, -0.0433, 0.8632],
    #                 [-0.0007, -1, 0.0054, 0],
    #                 [-0.0433, 0.0054, 0.9990, 0.2859],
    #                 [0, 0, 0, 1]])                     #也没问题,旋转矩阵的原因???

    wTcsim = np.array([[-1, 0.000, -0.0, 0.8632],
                    [-0.000, -1, 0.0, 0],
                    [-0.0, 0.0, 1,0.2859 ],
                    [0, 0, 0, 1]])  #test


    wTc = np.dot(wTcsim,csimTc)
    cTw = np.linalg.inv(wTc)
    wTo = wTo

    wTp = np.dot(wTo, pose)
    cTp = np.dot(cTw, wTp)
    # iTp = np.dot(iTc, cTp)
    iTw = np.dot(iTc, cTw)

    w_origin_p = wTp[:, 3]
    i_origin_p = np.dot(iTw, w_origin_p)
    i_origin_p = i_origin_p / i_origin_p[2]
    # center = iTp[:,3]/iTp[2,3]
    center = i_origin_p
    tan_angle = (wTp[2,0]/wTp[1,0])
    angle = math.degrees(math.atan(tan_angle))

    return center,angle

def test_pose2patch(pose,wTo):
    '''
    :param pose: 手掌坐标系相对于世界坐标系的转换矩阵,以及gazebo中物体坐标系相对于世界坐标系的转换矩阵
    :return: patch的中心位置和角度
    '''

    iTc = np.array([[554.254691191187, 0.0, 320.5, -0.0],
                    [0.0, 554.254691191187, 240.5, 0.0],
                    [0.0, 0.0, 1.0, 0.0]]) #内参矩阵没问题
    csimTc = np.array([[0,0,1,0],
                       [-1,0,0,0],
                       [0,-1,0,0],
                       [0,0,0,1]])   #也没有问题
    #
    # wTcsim = np.array([[-0.9991, 0.0005, -0.0433, 0.8632],
    #                 [-0.0007, -1, 0.0054, 0],
    #                 [-0.0433, 0.0054, 0.9990, 0.2859],
    #                 [0, 0, 0, 1]])                     #也没问题,旋转矩阵的原因???

    wTcsim = np.array([[-1, 0.000, -0.0, 0.8632],
                    [-0.000, -1, 0.0, 0],
                    [-0.0, 0.0, 1,0.2859 ],
                    [0, 0, 0, 1]])  #test


    wTc = np.dot(wTcsim,csimTc)
    cTw = np.linalg.inv(wTc)
    wTo = wTo

    wTp = np.dot(wTo, pose)
    cTp = np.dot(cTw, wTp)
    iTp = np.dot(iTc, cTp)
    iTw = np.dot(iTc,cTw)

    p_origin = wTp[:,3]
    p_x = wTp[:,0]
    print('wTp',wTp)
    print('p_origin',p_origin)
    print('iTw',iTw)
    i_origin_p = np.dot(iTw,p_origin)
    i_origin_p = i_origin_p/i_origin_p[2]

    i_x_p = np.dot(iTw,p_x)
    i_x_p = i_x_p/i_x_p[2]
    print('i_origin_p',i_origin_p)
    center = iTp[:,3]/iTp[2,3]
    # center = iTp[:, 3]
    # p_x = np.dot(iTp,np.array([[1],[0],[0],[1]])) #手掌坐标系的x轴在图像中的像素位置
    # p_x = p_x/p_x[2][0]
    # tan_angle = (center[1]-i_x_p[1])/(i_x_p[0]-center[0])
    # angle = math.degrees(math.atan(tan_angle))
    print('iTp',iTp)
    tan_angle = (wTp[2,0]/wTp[1,0])
    angle = math.degrees(math.atan(tan_angle))
    # print(wTp)

    return center,angle

def quat2rotm(quat):
    '''
    :param quat: 四元素(x,y,z,w)
    :return: 旋转矩阵
    '''
    x = quat[0]
    y = quat[1]
    z = quat[2]
    w = quat[3]
    # R = [[2*(w**2+x**2)-1, 2*(x*y-w*z), 2*(x*z+w*y)],
    #      [2*(x*y+w*z), 2*(w**2+y**2)-1, 2*(y*z-w*x)],
    #      [2*(x*z-w*y), 2*(y*z+w*x), 2*(w**2+z**2)-1]]
    R = np.array([[w**2+x**2-y**2-z**2, 2*(x*y-w*z), 2*(x*z+w*y)],
         [2*(x*y+w*z), w**2-x**2+y**2-z**2, 2*(y*z-w*x)],
         [2*(x*z-w*y), 2*(y*z+w*x), w**2-x**2-y**2+z**2]])
    return R

if __name__ == '__main__':
    #   file_path = '/home/well/simulation_data/graspit_data/64/0.txt'
    #  f = open(file_path, 'r')
    #  grasps = pickle.load(f)
    # # wTo = get_wTo('/home/well/simulation_data/gazebo_data/sdf_file/o64.sdf')
    #  wTo = np.array([[0, 0, -1, 0],
    #                  [-1, 0, 0, 0],
    #                  [0, 1, 0, 0],
    #                  [0, 0, 0, 1]])  # 由于0到4模型是自己画的,所以他们的物体坐标系和gazebo中的世界坐标系是重合的
    #  print(wTo)
    #  print(grasps[0])
    #  pose = get_pose(grasps[0].pose)
    #  center, angle = pose2patch(pose,wTo)
    #  print (center,angle)
    #  exit()

    # pose = Pose()
    # pose.position.x = 0.0613685511675
    # pose.position.y = 0.00172123089848
    # pose.position.z = -0.0937376560948
    # pose.orientation.x = 0.454316432973
    # pose.orientation.y = 0.105399191172
    # pose.orientation.z = 0.882919146794
    # pose.orientation.w = -0.0542343936537
    # print get_pose(pose)

    #
    # palm_poses_path = '/home/well/simulation_data3.0/test4/palm_poses.txt'
    # f = open(palm_poses_path,'r')
    # palm_poses = pickle.load(f)
    # hand_poses = []
    # for it in palm_poses:
    #     pose = Pose()
    #     wTh = get_hand_pose(it)
    #     pose.position.x = wTh[0][3]
    #     pose.position.y = wTh[1][3]
    #     pose.position.z = wTh[2][3]
    #     pose.orientation.x = it.orientation.x
    #     pose.orientation.y = it.orientation.y
    #     pose.orientation.z = it.orientation.z
    #     pose.orientation.w = it.orientation.w
    #     hand_poses.append(pose)
    # print(len(hand_poses))
    # hand_poses_path = '/home/well/simulation_data3.0/test4/hand_poses.txt'
    # f = open(hand_poses_path,'w')
    # pickle.dump(hand_poses,f,0)
    # f.close()

    # wTo = np.array([[0, 0, -1, 0],
    #                 [-1, 0, 0, 0],
    #                 [0, 1, 0, 0],
    #                 [0, 0, 0, 1]])
    # pose1 = quat2rotm([0.23988375567,0.588800997471,-0.748434582296,0.188718958151])
    # pose2 = quat2rotm([0.119849425074,0.611074029394,-0.776746197622,0.094286745561])
    # p1 = np.array([[-8.13681877e-01,  5.64975178e-01, -1.36838775e-01,0],
    #    [ 1.01130215e-12, -2.35397080e-01, -9.71899282e-01,0],
    #    [-5.81310419e-01, -7.90816832e-01,  1.91538338e-01,0],
    #                [0,0,0,1]]),
    # p2 = np.array([[-9.53492250e-01,  2.92947484e-01, -7.09528074e-02,0],
    #    [-2.72531997e-13, -2.35397080e-01, -9.71899282e-01,0],
    #    [-3.01417533e-01, -9.26698433e-01,  2.24449292e-01,0],
    #                [0,0,0,1]])

    # f = open('/home/well/simulation_data2.0/test4/hand_poses.txt', 'r')
    # hand_poses = pickle.load(f)
    # f.close()
    # # print hand_poses[0], hand_poses[1]
    # pose0 = get_pose(hand_poses[0])
    # pose1 = get_pose(hand_poses[1])
    #
    # a = 0.707106781
    # pose0 = np.array([[-a,-a,0,0],
    #                   [a,-a,0,0],
    #                   [0,0,1,0],
    #                   [0,0,0,1]])
    # # # print(pose0,pose1)
    # # print(test_pose2patch(pose0, wTo),test_pose2patch(pose1, wTo))
    # print(pose2patch(pose0, wTo))
    exit()