#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import rospy
from PIL import Image

import sys
#import h5py
import numpy as np
#import keras
#import keras.backend as K
#from keras.models import Sequential
#from keras.preprocessing import image
import scipy.io as scio
import os
import copy
import pickle
from sr_robot_commander.sr_hand_commander import SrHandCommander
from sr_robot_msgs.msg import ShadowPST
from sensor_msgs.msg import JointState

#from img_nomalize import normalizeImag

 

#load picture and predict hand posesure



# img=np.array([])
# def readimg(data):
    # global img
    # img=cv_bridge.CvBridge().imgmsg_to_cv2(data)
    # cv2.imshow("Image window", img)
    # cv2.waitKey(3)
    # cv2.imshow(window,img)
    # print 2

#PST callback
p = [0, 0, 0, 0, 0]
def pst_callback(data):
    p[0] = data.pressure[0]
    p[1] = data.pressure[1]
    p[2] = data.pressure[2]
    p[3] = data.pressure[3]
    p[4] = data.pressure[4]

j=[0,0,0,0,
   0,0,0,0,
   0,0,0,0,
   0 ,0 ,0 ,0]
def joint_callback(data):
    for i in range(0,16):
       j[i]=data.position[i]
       #  print i,data.position[i]
if __name__ == '__main__':
    rospy.init_node('img2grasp',anonymous=True)
    #first:load picture and processing
    
    #手势预测
    graspit_names = ['rh_RFJ4', 'rh_RFJ3', 'rh_RFJ2', 'rh_RFJ1',
              'rh_MFJ4', 'rh_MFJ3', 'rh_MFJ2', 'rh_MFJ1',
              'rh_FFJ4', 'rh_FFJ3', 'rh_FFJ2', 'rh_FFJ1',
              'rh_THJ5', 'rh_THJ4', 'rh_THJ2', 'rh_THJ1']
    hand_names = ['rh_FFJ1', 'rh_FFJ2', 'rh_FFJ3', 'rh_FFJ4',
                  'rh_MFJ1', 'rh_MFJ2', 'rh_MFJ3', 'rh_MFJ4',
                  'rh_RFJ1', 'rh_RFJ2', 'rh_RFJ3', 'rh_RFJ4',
                  'rh_THJ1', 'rh_THJ2', 'rh_THJ4', 'rh_THJ5']
    hand_names_2 = [ 'rh_FFJ2', 'rh_FFJ3', 'rh_FFJ4',
                   'rh_MFJ2', 'rh_MFJ3', 'rh_MFJ4',
                   'rh_RFJ2', 'rh_RFJ3', 'rh_RFJ4',
                   'rh_THJ2', 'rh_THJ4', 'rh_THJ5']
    ff_names=['rh_FFJ1', 'rh_FFJ2', 'rh_FFJ3', 'rh_FFJ4']
    mf_names=['rh_MFJ1', 'rh_MFJ2', 'rh_MFJ3', 'rh_MFJ4']
    rf_names=['rh_RFJ1', 'rh_RFJ2', 'rh_RFJ3', 'rh_RFJ4']
    th_names=['rh_THJ1', 'rh_THJ2', 'rh_THJ4', 'rh_THJ5']

    #depth_path = '/home/well/depth.jpg'  
    #depth_img = image.img_to_array(image.load_img(depth_path))
    #depth_img0 = normalizeImag(depth_img)

    #patch_path = '/home/well/patch.jpg'
    #patch = image.img_to_array(image.load_img(patch_path))
    #patch_img0 = normalizeImag(patch)

    #zxyzw_path = '/home/well/zxyzws.mat'
    #data = scio.loadmat(zxyzw_path)
    #zxyzw = np.array(data['zxyzws'])

    #patches = []
    #depthes = []
    #zxyzws = []

    #patches.append(patch_img0)
    #depth.append(depth_img0)
    #zxyzws.append(zxyzw)

    #patches = np.array(patches)
    #depthes = np.array(depthes)
    #zxyzws = np.array(zxyzws)
    
    
    #model1 = keras.models.load_model('/home/well/simulation_data1.0/model/m41/m41.h5')
    #a = model1.predict([patches, depthes,zxyzws])


    hand_commander = SrHandCommander(name="right_hand")
    open_hand = {'rh_FFJ1': 0.0, 'rh_FFJ2': 0.0, 'rh_FFJ3': 0.0, 'rh_FFJ4': 0.0,
                 'rh_MFJ1': 0.0, 'rh_MFJ2': 0.0, 'rh_MFJ3': 0.0, 'rh_MFJ4': 0.0,
                 'rh_RFJ1': 0.0, 'rh_RFJ2': 0.0, 'rh_RFJ3': 0.0, 'rh_RFJ4': 0.0,
                 'rh_THJ4': 0.8856136029027907, 'rh_THJ5': -1.0418645860720168, 'rh_THJ1':  0.5164078243515363, 'rh_THJ2':  0.6056523086455713}
    #start_valuse = [0.08594424346941776, 1.4887283546430148, 0.1570938787838334, 0.0034799191762053994, 0.04224253070065953, 1.3820759092096202, 0.24623890506808585, -0.03582943463339506, 0.03445869425502046, 1.331938122462683, 0.17398946511111255, -0.06239579822210881, -0.1792937354983885, -0.1433491138796516, 1.1385443298776026, -0.9160695228533858]
    start_valuse = [0, 0, 0, 0, 0, 0, 0, -0, 0, 0, 0, -0, -0.1792937354983885, -0.1433491138796516, 1.1385443298776026, -0.9160695228533858]

    print('input s to start:')
    if raw_input() =='s':
        pass
    hand_commander.move_to_joint_value_target_unsafe(open_hand,5.0, True)
    #start_hand=dict(zip(hand_names, start_valuse))
    #hand_commander.move_to_joint_value_target_unsafe(start_hand, 2.0, True)

  #ur5到达物体位置
    print 'if shadow hand is ready, please enter ok'
    if raw_input() == 'ok':
        pass
    f = open('/home/well/postures.txt' , 'r')
    a = pickle.load(f)
    f.close() 
    print('predict: ', a)
    pre_hand=dict(zip(graspit_names, a[0]))
    print pre_hand
    for key in pre_hand:
        if key == 'rh_RFJ4' or key == 'rh_MFJ4' or key == 'rh_FFJ4':
            pre_hand[key] = -pre_hand[key]
    print pre_hand
    #shadow手闭合
    hand_commander.move_to_joint_value_target_unsafe(pre_hand, 2.0, True)
    print pre_hand
    print 'input c to continue'
    if raw_input() == 'c':
        pass
    rospy.Subscriber("/rh/tactile", ShadowPST, pst_callback)
    rospy.Subscriber("/joint_states",JointState,joint_callback)
    rospy.sleep(1)
    first = copy.deepcopy(p)
    zl = [0.02, 0.05, 0.1, 0,
          0.02, 0.05, 0.1, 0,
          0.02, 0.05, 0.1, 0,
          0.0, 0.0, 0.0, 0]
    # zl = [0.05, 0.05, 0.05, 0,
    #       0, 0, 0, 0,
    #       0, 0, 0, 0,
    #       0, 0, 0, 0]
    # zeros = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    zl=dict(zip(hand_names,zl))
    flag=0
    th = True
    while flag<16 :
        flag = 0
        # print ("bijiao" + str(cmp(zeros, zl)) + "\n")
        for key in hand_names:
            pre_hand[key]=pre_hand[key]+zl[key]

        hand_commander.move_to_joint_value_target_unsafe(pre_hand, 2.0, True)
        # last_values = copy.deepcopy(j)
        # last_values=dict(zip(hand_names,last_values))
        # for key in hand_names_2:
        #     if pre_hand[key]- last_values[key] >0.05 and zl[key]>0:
        #         zl[key] = 0
        #         print key

        realtime=p
        # print("first:" + str(first[0]) + "realtime:" + str(realtime[0]) + ",zl" + str(zl[0:15]) + "\n")
        if (realtime[0] - first[0]) >= 10 :
            for key in ff_names:
                zl[key]=0
            print 'ff'
        #     zl[0:4] = [0, 0, 0, 0]
        if (realtime[1] - first[1]) >= 10:
            for key in mf_names:
                zl[key]=0
            print realtime[1],first[1]
            print 'mf'
        #     zl[4:8] = [0, 0, 0, 0]
        if (realtime[2] - first[2]) >= 10:
            for key in rf_names:
                zl[key]=0
            print 'rf'
        #     zl[8:12] = [0, 0, 0, 0]
        if (realtime[4] - first[4]) >= 10:
            for key in th_names:
                zl[key]=0
            print 'th'

        for key in  hand_names:
            if zl[key]==0:
                flag+=1
            if flag == 16 and th :      #其他四指完成后,大拇指闭合
                zl['rh_THJ1'] = 0.02
                zl['rh_THJ2'] = 0.05
                zl['rh_THJ4'] = 0.1
                print 'th_s'
                flag = flag -1
                th = False

        print 'flag:',flag
        #     zl[12:16] = [0, 0, 0, 0]
    print 'finish'
    print 'open the object,please enter o'
    if raw_input() == 'o':
        pass
    hand_commander.move_to_joint_value_target_unsafe(open_hand, 5.0, True)
    rospy.spin()
