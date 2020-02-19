# coding:utf-8
from __future__ import division
import numpy as np
import pickle
import json
import h5py
import os
import random
# from PIL import Image
import keras
from keras.preprocessing import image
from keras.layers import Conv2D,Input,Dense
from keras.layers import MaxPooling2D,Activation
from keras.layers import Flatten,Concatenate
from keras.layers.normalization import BatchNormalization
from keras.optimizers import Adam, SGD
from keras.models import Model
from keras.callbacks import History, ModelCheckpoint,TensorBoard
from keras.utils import plot_model
import matplotlib.pyplot as plt
#由于keras中训练时是先划分数据集再打乱,所以我们要先打乱数据集合
import sys


def normalizeImag(img):
    img_max = 255.0
    img_min = 0.0
    img_normal = (img[:, :, 0:1]-img_min)/(img_max-img_min)
    return img_normal


def shuffle_data(*params):
    '''
    :param params:数据列表
    :return: 打乱后的数据
    '''
    params_num = len(params)
    length = len(params[0])
    index = np.random.permutation(length)
    result = []
    for i in range(params_num):
        result.append([])
    for i in index:
        for j in range(params_num):
            result[j].append(params[j][i])

    return result


if __name__ == "__main__":
    # patch = image.img_to_array(image.load_img('/home/well/simulation_data/patches/14/4.jpg'))
    # patch = normalizeImag(patch)
    # print(patch) #
    # print(patch.shape)
    # if input()== 'f':
    #     exit()
   
    #(64, 128, 3)
    patches = []
    postures = []
    zxyzws = []
    depthes = []
    for i in range(66):
        patches_path = '/home/user4/well/simulation_data3.0/patches/' + str(i) +'/'
        patch_files = os.listdir(patches_path)
        depthes_path = '/home/user4/well/simulation_data3.0/overall/' + str(i) + '.jpg'
        for j in patch_files:
            patch_path = patches_path + j
            patch = image.img_to_array(image.load_img(patch_path))
            patch = normalizeImag(patch)#(64,128,1)
            patches.append(patch)
            
            depth = image.img_to_array(image.load_img(depthes_path))
            depth = normalizeImag(depth) #(128,128,1)            
            depthes.append(depth)

        graps_dofs_path = '/home/user4/well/simulation_data3.0/noTh3dofs/' +str(i)+ '.txt'
        f = open(graps_dofs_path,'rb')
        postures += pickle.load(f)
        f.close()

        zxyzws_path = '/home/user4/well/simulation_data3.0/100zxyzws/'+str(i)+ '.txt'
        f = open(zxyzws_path,'rb')
        zxyzws += json.load(fp=f)
        f.close()
    
    #zeros = [0]*17
    #for i in range(45):
     #   temp_index = random.randrange(0,1111)
      #  postures.append(zeros)
       # zxyzws.append(zxyzws[temp_index])


    print(len(patches),len(postures),len(zxyzws))
    #for it in good:
     #   good_patches.append(patches[it])
     #   good_zxyzws.append(np.dot(zxyzws[it],np.array([[10,0,0,0,0],[0,1,0,0,0],[0,0,1,0,0],[0,0,0,1,0],[0,0,0,0,1]])))  #因为z的值太小0.02
     #   good_postures.append(postures[it])
    #print(zxyzws[4],good_zxyzws[0])
    data = shuffle_data(patches,zxyzws,postures,depthes)
    #data = shuffle_data(good_patches,good_zxyzws,good_postures)
    img = np.array(data[0])
    pose = np.array(data[1])
    posture = np.array(data[2])
    img1 = np.array(data[3])

    img_input = Input(shape=(64, 128, 1))
    x = Conv2D(32, (6, 6),strides=(2, 2))(img_input)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)
    x = Conv2D(8, (3, 3),strides=(2, 2))(x)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)
    #x = Conv2D(16, (3, 3))(x)
    #x = BatchNormalization()(x)
    #x = Activation('relu')(x)
    #x = Conv2D(128, (3, 3))(x)
    #x = BatchNormalization()(x)
    #x = Activation('relu')(x)
    x = MaxPooling2D((2, 2))(x)
    img_out = Flatten()(x)

    img_input1 = Input(shape=(128, 128, 1))
    x1 = Conv2D(32, (12, 12),strides=(2, 2))(img_input1)
    x1 = BatchNormalization()(x1)
    x1 = Activation('relu')(x1)
    x1 = Conv2D(8, (6, 6),strides=(2, 2))(x1)
    x1 = BatchNormalization()(x1)
    x1 = Activation('relu')(x1)
    #x1 = Conv2D(16, (3, 3))(x1)
    #x1 = BatchNormalization()(x1)
    #x1 = Activation('relu')(x1)
    #x = Conv2D(128, (3, 3))(x)
    #x = BatchNormalization()(x)
    #x = Activation('relu')(x)
    x1 = MaxPooling2D((2, 2))(x1)
    img_out1 = Flatten()(x1)

    pose_input = Input(shape=(5,))
    y = BatchNormalization()(pose_input)
    y = Dense(32)(y)
    y = BatchNormalization()(y)
    y = Activation('relu')(y)
    y = Dense(32)(y)
    y = BatchNormalization()(y)
    y = Activation('relu')(y)
    pose_out = Dense(32, activation='relu')(y)

    merged = keras.layers.concatenate([img_out,img_out1, pose_out])

    z = Dense(256)(merged)
    z = BatchNormalization()(z)
    z = Activation('relu')(z)
    z = Dense(256)(z)
    z = BatchNormalization()(z)
    z = Activation('relu')(z)
    z = Dense(256)(z)
    z = BatchNormalization()(z)
    z = Activation('relu')(z)
    out = Dense(16, activation='linear')(z)

    adam =Adam()
    model = Model(inputs=[img_input, img_input1, pose_input], outputs=out)
    model.compile(optimizer=adam, loss='mean_squared_error')

    #修改
    plot_model(model,to_file='m47.png')
    #修改
    checkpoint = ModelCheckpoint('m47.h5', monitor='val_loss', verbose=1, save_best_only=True, mode=min)
    tb_callback = TensorBoard(log_dir='./m47',histogram_freq=0,write_images=False,write_graph=True)
    history = model.fit([img, img1, pose], posture, batch_size=20, epochs=1000, validation_split=0.2, callbacks=[checkpoint,tb_callback])
