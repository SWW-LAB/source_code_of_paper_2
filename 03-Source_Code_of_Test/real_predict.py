#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division

from PIL import Image

import sys
import h5py
import numpy as np
import keras
import keras.backend as K
from keras.models import Sequential
from keras.preprocessing import image
import scipy.io as scio
import os
import copy
import pickle
''
def normalizeImag(img):
    img_max = 255.0
    img_min = 0
    if img_max == img_min:
        return img[:, :, 0:1]
    img_normal = (img[:, :, 0:1]-img_min)/(img_max-img_min)
    return img_normal

if __name__ == '__main__':

    #first:load picture and processing

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
    model1 = keras.models.load_model('/home/well/simulation_data2.0/models/m47/m47.h5')
    
    while True:
        print('input s to start:')
        if input() == 's':
            pass
        else:
            break
        depth_path = '/home/well/depth.jpg'  
        depth_img = image.img_to_array(image.load_img(depth_path))
        depth_img0 = normalizeImag(depth_img)

        patch_path = '/home/well/patch.jpg'
        patch = image.img_to_array(image.load_img(patch_path))
        patch_img0 = normalizeImag(patch)      

        zxyzw_path = '/home/well/zxyzws.mat'
        data = scio.loadmat(zxyzw_path)
        zxyzws = np.array(data['zxyzws'])

        patches = []
        depthes = []
     

        patches.append(patch_img0)
        depthes.append(depth_img0)


        patches = np.array(patches)
        depthes = np.array(depthes)
    
    
    

        a = model1.predict([patches, depthes,zxyzws])
        f = open('/home/well/postures.txt' , 'wb')
        pickle.dump(a, f, 0)
        f.close()    
        print('predict: ', a)
    #pre_hand=dict(zip(graspit_names, a[0]))
    #print(pre_hand)
    #for key in pre_hand:
    #    if key == 'rh_RFJ4' or key == 'rh_MFJ4' or key == 'rh_FFJ4':
    #        pre_hand[key] = -pre_hand[key]
    #print(pre_hand)


