#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division

from PIL import Image
import numpy as np
import scipy.io as scio
import os
import copy
import pickle
import json
from geometry_msgs.msg import Pose

def get_data():
    wxyzs_path = '/home/well/simulation_data2.0/test4/result.mat'
    data = scio.loadmat(wxyzs_path)
    wxyzs = data['result']
    wxyzs = wxyzs.tolist()
    z = -0.0343643618106141
    zxyzws = []
    zxyzws_path = '/home/well/simulation_data2.0/test4/100zxyzws.txt'

    poses = []
    poses_path = '/home/well/simulation_data2.0/test4/palm_poses.txt'
    for i in range(-5,6):
        temp = z*100 + i
        for j in wxyzs:
            zxyzw = []
            zxyzw.append(temp)
            zxyzw += j[1:4]
            zxyzw.append(j[0])
            zxyzws.append(zxyzw)
#Palm coordinates
            pose = Pose()
            pose.position.x = 2.74984779e-02
            pose.position.y = 2.39839815e-02 
            pose.position.z = temp/100.0
            pose.orientation.x = j[1]
            pose.orientation.y = j[2]
            pose.orientation.z = j[3]
            pose.orientation.w = j[0]
            poses.append(pose)


    print len(zxyzws)
    f = open(zxyzws_path,'w')
    json.dump(zxyzws,f)
    f.close()

    print len(poses)
    f = open(poses_path,'w')
    pickle.dump(poses,f,0)
    f.close()



if __name__=='__main__':
    #get_data()
    f = open('palm_poses.txt','r')
    hand_poses = pickle.load(f)
    f.close()
    print hand_poses[0],hand_poses[1]        
    
