# -*- coding:utf-8 -*-
from __future__ import print_function
import numpy as np
import random
import pickle
import os
from keras.preprocessing import image
import keras
from keras.models import Model
from get_testdata import get_testdata
from get_pose import get_pose,get_wTo,pose2patch
from get_patch import get_patch
import json
import tensorflow as tf


def normalizeImag(img):
    img_max = 255.0
    img_min = 0.0
    img_normal = (img[:, :, 0:1]-img_min)/(img_max-img_min)
    return img_normal

def normalize_imag(img):
    img_max = 255.0
    img_min = 0.0
    img_normal = img
    for i in range(3):
        img_normal[:,:,i] = (img[:,:,i]-img_min)/(img_max-img_min)
    return img_normal


def normalizeImag_old(img):
    img_max = np.max(img)
    img_min = np.min(img)
    img_normal = (img[:, :, 0:1]-img_min)/(img_max-img_min)
    return img_normal

def main():
    zxyzws = []
    models = []
    poses = []

    for i in range(100):
        save_path = '/home/well/simulation_data/test/' + str(i) +'.jpg'
        index = random.randrange(0,1112)
        model = random.randrange(0,65)
        zxyzw = get_testdata(index, model,save_path)
        zxyzws.append(zxyzw)
        models.append(model)
        poses.append(index)
    f = open('/home/well/simulation_data/test/test_zxyzws.txt', 'wb')
    pickle.dump(zxyzws, f,0)
    f.close()

    f = open('/home/well/simulation_data/test/models.txt', 'wb')
    pickle.dump(models, f,0)
    f.close()

    f = open('/home/well/simulation_data/test/poses.txt', 'wb')
    pickle.dump(poses, f,0)
    f.close()
    # patch_path = '/home/well/simulation_data/test/0.jpg'
    # patch = image.img_to_array(image.load_img(patch_path))
    # patch =  normalizeImag(patch)
    # patch = np.expand_dims(patch, axis=0)
    # patch = np.array(patch)
    #
    # zxyzw = np.array(zxyzw)
    # model = keras.models.load_model('./m5/m5.h5')
    # posture = model.predict([patch, zxyzw])
    # print(posture)
def test():
    f = open('/home/well/simulation_data/test0/poses.txt', 'rb')
    indexes = pickle.load(f)
    f.close()

    f = open('/home/well/simulation_data/test0/models.txt', 'rb')
    models = pickle.load(f)
    f.close()

    for i in range(100):
        save_path = '/home/well/simulation_data/test/' + str(i) + '.jpg'
        index = indexes[i]
        model = models[i]
        zxyzw = get_testdata(index, model, save_path)

def test1():
    f = open('/home/well/simulation_data/test1/poses.txt','r')
    poses = pickle.load(f)
    f.close()
    flag = -1
    z_size = [0.06, 0.03, 0.06, 0.035, 0.05]
    for i in range(65):
        if i == 45 or i == 57:
            print(i)
            continue
        if i < 5:
            poses[i].position.z += z_size[i]
        flag += 1
        save_path = '/home/well/simulation_data/test1/' + str(flag) + '.jpg'
        pose = get_pose(poses[flag])
        sdf_path = '/home/well/simulation_data/gazebo_data/sdf_file/o' + str(i) + '.sdf'
        if i < 5:
            wTo = np.array([[0, 0, -1,0],
                            [-1, 0, 0,0],
                            [0, 1, 0,0],
                            [0, 0, 0,1]])
        else:
            wTo = get_wTo(sdf_path)
        center, angle = pose2patch(pose, wTo)
        depth_path = '/home/well/simulation_data/depth/' + str(i) + '.jpg'
        patch_size = [128, 64]
        img = get_patch(depth_path, angle, center, patch_size)
        img.save(save_path)

def test2():
    model1 = keras.models.load_model('/home/well/simulation_data3.0/models/m54/m54.h5')

    for i in range(4):
        patches = []
        # zxyzws = []
        depthes = []
        # postures = []

        patches_path = '/home/well/simulation_data3.0/test2/patches/' + str(i)+'/'
        patch_files = os.listdir(patches_path)
        patch_files.sort(key=lambda x: int(x[:-4]))
        depthes_path = '/home/well/simulation_data3.0/test2/overall/'+str(i)+'.jpg'
        for j in patch_files:
            print(j)
            patch_path = patches_path + j
            patch = image.img_to_array(image.load_img(patch_path))
            patch = normalizeImag(patch)
            patches.append(patch)

            depth = image.img_to_array(image.load_img(depthes_path))
            depth = normalizeImag(depth)
            depthes.append(depth)

        zxyzws_path = '/home/well/simulation_data3.0/test2/100zxyzws/'+str(i)+'.txt'
        f = open(zxyzws_path,'rb')
        zxyzws = json.load(fp=f)
        f.close()

        postures_path = '/home/well/simulation_data3.0/test2/postures/m54/'+str(i)+'.txt'
        a = model1.predict([patches, depthes, zxyzws])
        f = open(postures_path, 'wb')
        pickle.dump(a,f,0)
        f.close()
        # print('predict: ', a)

def test3():
    model1 = keras.models.load_model('/home/well/simulation_data3.0/models/m54/m54.h5')

    for i in [3]:
        patches = []
        # zxyzws = []
        depthes = []
        # postures = []

        patches_path = '/home/well/simulation_data3.0/test3/patches/' + str(i)+'/'
        patch_files = os.listdir(patches_path)
        patch_files.sort(key=lambda x: int(x[:-4]))
        depthes_path = '/home/well/simulation_data3.0/test3/overall/'+str(i)+'.jpg'
        for j in patch_files:
            print(j)
            patch_path = patches_path + j
            patch = image.img_to_array(image.load_img(patch_path))
            patch = normalizeImag(patch)
            patches.append(patch)

            depth = image.img_to_array(image.load_img(depthes_path))
            depth = normalizeImag(depth)
            depthes.append(depth)

        zxyzws_path = '/home/well/simulation_data3.0/test3/100zxyzws/'+str(i)+'.txt'
        f = open(zxyzws_path,'rb')
        zxyzws = json.load(fp=f)
        f.close()

        postures_path = '/home/well/simulation_data3.0/test3/postures/m54/'+str(i)+'.txt'
        a = model1.predict([patches, depthes, zxyzws])
        f = open(postures_path, 'wb')
        pickle.dump(a,f,0)
        f.close()
        # print('predict: ', a)


def test4():
    model1 = keras.models.load_model('/home/well/simulation_data3.0/models/m54/m54.h5')

    for i in [3]:
        patches = []
        # zxyzws = []
        depthes = []
        # postures = []

        patches_path = '/home/well/simulation_data3.0/test4/patches/' + str(i)+'/'
        patch_files = os.listdir(patches_path)
        patch_files.sort(key=lambda x: int(x[:-4]))
        depthes_path = '/home/well/simulation_data3.0/test4/overall/'+str(i)+'.jpg'
        for j in patch_files:
            print(j)
            patch_path = patches_path + j
            patch = image.img_to_array(image.load_img(patch_path))
            patch = normalizeImag(patch)
            patches.append(patch)

            depth = image.img_to_array(image.load_img(depthes_path))
            depth = normalizeImag(depth)
            depthes.append(depth)

        zxyzws_path = '/home/well/simulation_data3.0/test4/100zxyzws.txt'
        f = open(zxyzws_path,'rb')
        zxyzws = json.load(fp=f)
        f.close()

        postures_path = '/home/well/simulation_data3.0/test4/postures/m54/'+str(i)+'.txt'
        a = model1.predict([patches, depthes, zxyzws])
        f = open(postures_path, 'wb')
        pickle.dump(a,f,0)
        f.close()

        # sess = keras.backend.get_session()
        # gradient = keras.backend.gradients(model1.output, model1.input)
        # print(gradient)
        # iterate = keras.backend.function(model1.input, [gradient])
        #
        # grad = iterate([patches, depthes, zxyzws])
        # print(grad)

def test5():
    model1 = keras.models.load_model('/home/well/simulation_data3.0/test5/models/pi16/pi16.h5',
                                     custom_objects={'keras':keras,'tf':tf})


    for i in range(0,4):
        rgb_patches = []
        depth_patches = []
        cur_patches = []
        normal_patches = []
        grasp_confs_init = []

        rgbes_path = '/home/well/simulation_data3.0/test5/test_dataset2.0/rgb_patches/' + str(i) + '/'
        depthes_path = '/home/well/simulation_data3.0/test5/test_dataset2.0/depth_patches/' + str(i) + '/'
        cures_path = '/home/well/simulation_data3.0/test5/test_dataset2.0/cur_patches/' + str(i) + '/'
        normales_path = '/home/well/simulation_data3.0/test5/test_dataset2.0/normal_patches/' + str(i) + '/'

        # rgbes_path = '/home/well/simulation_data3.0/test5/train_dataset2.0/rgb_patches/' + str(i) + '/'
        # depthes_path = '/home/well/simulation_data3.0/test5/train_dataset2.0/depth_patches/' + str(i) + '/'
        # cures_path = '/home/well/simulation_data3.0/test5/train_dataset2.0/cur_patches/' + str(i) + '/'
        # normales_path = '/home/well/simulation_data3.0/test5/train_dataset2.0/normal_patches/' + str(i) + '/'
        patch_files = os.listdir(rgbes_path)

        for j in patch_files:
            rgb_path = rgbes_path + j
            rgb = image.img_to_array(image.load_img(rgb_path))
            rgb = normalize_imag(rgb)  # (200,200,1)
            rgb_patches.append(rgb)

            depth_path = depthes_path + j
            depth = image.img_to_array(image.load_img(depth_path))
            depth = normalizeImag(depth)
            depth_patches.append(depth)

            normal_path = normales_path + j
            normal = image.img_to_array(image.load_img(normal_path))
            normal = normalize_imag(normal)
            normal_patches.append(normal)

            cur_path = cures_path + j
            cur = image.img_to_array(image.load_img(cur_path))
            cur = normalizeImag(cur)
            cur_patches.append(cur)

        grasp_conf_path = '/home/well/simulation_data3.0/test5/test_dataset2.0/grasp_confs_init/' + str(i) + '.txt'
        # grasp_conf_path = '/home/well/simulation_data3.0/test5/train_dataset2.0/grasp_confs/' + str(i) + '.txt'
        f = open(grasp_conf_path, 'r')
        grasp_conf = json.load(f)
        f.close()
        grasp_confs_init += grasp_conf
        grasp_confs_init = np.array(grasp_confs_init)
        grasp_confs_init[:, 7:] = [-0.0070509969090822525, 0.15708630287746228, 0.8684231048744118, 0.20985667739456532,
                                   -0.01393017002025742, 0.6508932204508318, 0.15331127605006806, 0.7196330754330225,
                                   0.03453206265774913, 0.48393492546294153, 0.9225066663000855, 0.33081737654552484,
                                   -0.9824073192368692, 1.0460589371627895, 0.24172038490244951, 0.9455156199992611]

        img_in = np.concatenate((rgb_patches, depth_patches, normal_patches, cur_patches), axis=-1)

        print(model1.summary())

        gradient = keras.backend.gradients(model1.output, model1.input)[1]
        iterate = keras.backend.function(model1.input, [gradient])
        # print(model1.layers[1].name)
        grasp_confs_final = []
        img_in_one = img_in[0:1]
        # print(model1.get_layer('conv2d_3').get_weights()[0][0])
        # print(model1.get_layer('conv2d_3').get_weights()[1])
        # layer_model = Model(inputs=model1.input,outputs=model1.get_layer('max_pooling2d_2').output)
        # img_in_one = img_in_one[np.newaxis,:]
        for it in grasp_confs_init[0:1]:
            conf_old = np.array(it)
            conf_old = conf_old[np.newaxis, :]

            for times in range(50):
                a_old = model1.predict([img_in_one, conf_old]) * 0.3
                grad = iterate([img_in_one, conf_old])
                # layer_output = layer_model.predict([img_in_one, conf_old])
                # print(layer_output)
                # print(a_old)
                # print(grad)
                # exit()
                # exit()
                # print(a_old)
                # print()

                # exit()
                alpha = 0.1
                t = 10
                beta = 0.8

                conf_new = conf_old + t * grad[0]  # shape(1,23)
                # print('conf_old1',conf_old)
                # print('conf_new1',conf_new)
                # conf_new[0][0:7] = conf_old[0][0:7]
                a_new = model1.predict([img_in_one, conf_new]) * 0.3
                while a_new < a_old + alpha * t * np.dot(grad[0][0].T, grad[0][0]):
                    print('a_new',a_new)
                    t = beta * t
                    conf_new = conf_old + t * grad[0]
                    # conf_new[0][0:7] = conf_old[0][0:7]
                    a_new = model1.predict([img_in_one, conf_new]) * 0.3
                    print('t',t)
                    # print(grad[0])
                # print('conf_old',conf_old)
                # print('conf_new',conf_new)
                # print(grad)
                conf_old = conf_new
                print(times)
                # print(grad)
                # exit()
            grasp_confs_final.append(conf_new[0].tolist())
        print(len(grasp_confs_final))
        confs_save_path = '/home/well/simulation_data3.0/test5/test_dataset2.0/grasp_confs_final/pi16_1/' + str(i) + '.txt'
        f = open(confs_save_path, 'w')
        json.dump(grasp_confs_final, f)
        f.close()


def test5_1():
    model1 = keras.models.load_model('/home/well/simulation_data3.0/test5/models/pi14/pi14.h5',
                                     custom_objects={'keras': keras, 'tf': tf})

    for i in range(4):
        # for i in [3]:
        rgb_patches = []
        depth_patches = []
        cur_patches = []
        normal_patches = []
        grasp_confs_init = []

        rgb_path = '/home/well/simulation_data3.0/test5/test_dataset1.0/rgb_patches/' + str(i) + '.jpg'
        depth_path = '/home/well/simulation_data3.0/test5/test_dataset1.0/depth_patches/' + str(i) + '.jpg'
        cur_path = '/home/well/simulation_data3.0/test5/test_dataset1.0/cur_patches/' + str(i) + '.jpg'
        normal_path = '/home/well/simulation_data3.0/test5/test_dataset1.0/normal_patches/' + str(i) + '.jpg'

        grasp_conf_path = '/home/well/simulation_data3.0/test5/test_dataset1.0/grasp_confs_init/' + str(i) + '.txt'
        f = open(grasp_conf_path, 'r')
        grasp_conf = json.load(f)
        f.close()
        grasp_confs_init += grasp_conf
        grasp_confs_init = np.array(grasp_confs_init)
        grasp_confs_init[:,7:] = [-0.0070509969090822525, 0.15708630287746228, 0.8684231048744118, 0.20985667739456532, -0.01393017002025742, 0.6508932204508318, 0.15331127605006806, 0.7196330754330225, 0.03453206265774913, 0.48393492546294153, 0.9225066663000855, 0.33081737654552484, -0.9824073192368692, 1.0460589371627895, 0.24172038490244951, 0.9455156199992611]

        rgb = image.img_to_array(image.load_img(rgb_path))
        rgb = normalize_imag(rgb)  # (400,400,1)
        depth = image.img_to_array(image.load_img(depth_path))
        depth = normalizeImag(depth)
        normal = image.img_to_array(image.load_img(normal_path))
        normal = normalize_imag(normal)
        cur = image.img_to_array(image.load_img(cur_path))
        cur = normalizeImag(cur)

        rgb_patches.append(rgb)
        depth_patches.append(depth)
        normal_patches.append(normal)
        cur_patches.append(cur)

        img_in = np.concatenate((rgb_patches, depth_patches, normal_patches, cur_patches), axis=-1)

        gradient = keras.backend.gradients(model1.output, model1.input)[1]
        iterate = keras.backend.function(model1.input, [gradient])

        grasp_confs_final = []
        for it in grasp_confs_init[0:1]:
            conf_old = np.array(it)
            conf_old = conf_old[np.newaxis, :]
            for times in range(10):
                a_old = model1.predict([img_in, conf_old]) * 0.3
                grad = iterate([img_in, conf_old])

                alpha = 0.3
                t = 1000
                beta = 0.8

                conf_new = conf_old + t * grad[0] #shape(1,23)
                conf_new[0][0:7] = conf_old[0][0:7]
                a_new = model1.predict([img_in, conf_new]) * 0.3
                while a_new < a_old + alpha*t*np.dot(grad[0][0].T, grad[0][0]):
                    # print(a_new)
                    t = beta*t
                    conf_new = conf_old + t * grad[0]
                    conf_new[0][0:7] = conf_old[0][0:7]
                    a_new = model1.predict([img_in, conf_new]) * 0.3
                    # print(grad[0])
                conf_old = conf_new
                print(times)
            grasp_confs_final.append(conf_new[0].tolist())
        print(len(grasp_confs_final))
        confs_save_path = '/home/well/simulation_data3.0/test5/test_dataset1.0/grasp_confs_final/pi11_1/' + str(i) + '.txt'
        f = open(confs_save_path, 'w')
        json.dump(grasp_confs_final, f)
        f.close()

def test5_2():
    model1 = keras.models.load_model('/home/well/simulation_data3.0/test5/models/pi12/pi12.h5',
                                     custom_objects={'keras': keras, 'tf': tf})

    for i in range(4):
        # for i in [3]:
        rgb_patches = []
        depth_patches = []
        cur_patches = []
        normal_patches = []
        grasp_confs_init = []

        rgb_path = '/home/well/simulation_data3.0/test5/test_dataset1.0/rgb_patches/' + str(i) + '.jpg'
        depth_path = '/home/well/simulation_data3.0/test5/test_dataset1.0/depth_patches/' + str(i) + '.jpg'
        cur_path = '/home/well/simulation_data3.0/test5/test_dataset1.0/cur_patches/' + str(i) + '.jpg'
        normal_path = '/home/well/simulation_data3.0/test5/test_dataset1.0/normal_patches/' + str(i) + '.jpg'

        grasp_conf_path = '/home/well/simulation_data3.0/test5/test_dataset1.0/grasp_confs_init/' + str(i) + '.txt'
        f = open(grasp_conf_path, 'r')
        grasp_conf = json.load(f)
        f.close()
        grasp_confs_init += grasp_conf
        grasp_confs_init = np.array(grasp_confs_init)
        grasp_confs_init[:,7:] = [-0.0070509969090822525, 0.15708630287746228, 0.8684231048744118, 0.20985667739456532, -0.01393017002025742, 0.6508932204508318, 0.15331127605006806, 0.7196330754330225, 0.03453206265774913, 0.48393492546294153, 0.9225066663000855, 0.33081737654552484, -0.9824073192368692, 1.0460589371627895, 0.24172038490244951, 0.9455156199992611]

        rgb = image.img_to_array(image.load_img(rgb_path))
        rgb = normalize_imag(rgb)  # (400,400,1)
        depth = image.img_to_array(image.load_img(depth_path))
        depth = normalizeImag(depth)
        normal = image.img_to_array(image.load_img(normal_path))
        normal = normalize_imag(normal)
        cur = image.img_to_array(image.load_img(cur_path))
        cur = normalizeImag(cur)

        rgb_patches.append(rgb)
        depth_patches.append(depth)
        normal_patches.append(normal)
        cur_patches.append(cur)

        img_in = np.concatenate((rgb_patches, depth_patches, normal_patches, cur_patches), axis=-1)

        gradient = keras.backend.gradients(model1.output, model1.input)[1]
        iterate = keras.backend.function(model1.input, [gradient])

        grasp_confs_final = []
        grasp_confs_init = np.array([[-0.0070509969090822525, 0.15708630287746228, 0.8684231048744118, 0.20985667739456532, -0.01393017002025742, 0.6508932204508318, 0.15331127605006806, 0.7196330754330225, 0.03453206265774913, 0.48393492546294153, 0.9225066663000855, 0.33081737654552484, -0.9824073192368692, 1.0460589371627895, 0.24172038490244951, 0.9455156199992611]])
        # grasp_confs_init = np.array([[1]*16])
        for it in grasp_confs_init[0:1]:
            conf_old = np.array(it)
            conf_old = conf_old[np.newaxis, :]
            for times in range(10):
                a_old = model1.predict([img_in, conf_old]) * 0.3
                grad = iterate([img_in, conf_old])
                # print(a_old)
                # print(conf_old)
                alpha = 0.3
                t = 1000
                beta = 0.8

                conf_new = conf_old + t * grad[0] #shape(1,23)
                # conf_new[0][0:7] = conf_old[0][0:7]
                a_new = model1.predict([img_in, conf_new]) * 0.3
                while a_new < a_old + alpha*t*np.dot(grad[0][0].T, grad[0][0]):
                    # print(a_new)
                    t = beta*t
                    conf_new = conf_old + t * grad[0]
                    # conf_new[0][0:7] = conf_old[0][0:7]
                    a_new = model1.predict([img_in, conf_new]) * 0.3
                # print(grad[0])
                # exit()
                conf_old = conf_new
                print(times)
            grasp_confs_final.append(conf_new[0].tolist())
        print(len(grasp_confs_final))
        confs_save_path = '/home/well/simulation_data3.0/test5/test_dataset1.0/grasp_confs_final/pi12_1/' + str(i) + '.txt'
        f = open(confs_save_path, 'w')
        json.dump(grasp_confs_final, f)
        f.close()


def sim5_pre():
    model1 = keras.models.load_model('/home/well/simulation_data5.0/model/pi42.h5',
                                     custom_objects={'keras': keras, 'tf': tf})
    #  Firstly test only one time
    for i in range(4):
        # for i in [3]:
        depth_patches = []
        grasp_confs_init = []

        depthes_path = '/home/well/simulation_data5.0/test_depth_patches/' + str(i) +'/'
        patch_files = os.listdir(depthes_path)
        patch_files.sort(key= lambda x: int(x[:-4]))

        grasp_conf_path = '/home/well/simulation_data5.0/test_grasp_confs/test_m_grasp_confs/' + str(i) + '.txt'
        f = open(grasp_conf_path, 'r')
        grasp_conf = json.load(f)
        f.close()
        grasp_confs_init += grasp_conf
        grasp_confs_init = np.array(grasp_confs_init)
        poses = grasp_confs_init[:, :7]

        # postures_path = '/home/well/simulation_data5.0/test_init_posture/m60/' + str(i) + '.txt'
        #graspit
        postures_path = '/home/well/simulation_data5.0/test_init_posture/' + str(i) + '.txt'
        f = open(postures_path,'rb')
        postures = pickle.load(f)
        f.close()
        postures = np.array(postures)

        for j in patch_files:
            print(j)
            depth_path = depthes_path + j
            depth = image.img_to_array(image.load_img(depth_path))
            depth = normalizeImag(depth)
            depth_patches.append(depth)

        img_in = np.array(depth_patches)
        print(img_in.shape)
        a = model1.predict([img_in, poses, postures])*0.12
        print(a)
        result = []
        for it in a:
            # it.tolist()
            result.append(it[0].item())
        confs_save_path = '/home/well/simulation_data5.0/test_quality/pi42/graspit/' + str(i) + '.txt'
        f = open(confs_save_path, 'w')
        json.dump(result, f)
        f.close()

def sim5_pre1():
    model1 = keras.models.load_model('/home/well/simulation_data5.0/model/pi48.h5',
                                     custom_objects={'keras': keras, 'tf': tf})
   #  Firstly test only one grasp
    for i in range(4):
        # for i in [3]:
        depth_patches = []
        grasp_confs_init = []
        global_depthes = []

        depthes_path = '/home/well/simulation_data5.0/test_patches/' + str(i) +'/'
        patch_files = os.listdir(depthes_path)
        patch_files.sort(key= lambda x: int(x[:-4]))

        grasp_conf_path = '/home/well/simulation_data5.0/test_100zxyzws/' + str(i) + '.txt'
        f = open(grasp_conf_path, 'r')
        grasp_conf = json.load(f)
        f.close()
        grasp_confs_init += grasp_conf
        grasp_confs_init = np.array(grasp_confs_init)
        poses = grasp_confs_init

        # postures_path = '/home/well/simulation_data5.0/test_init_posture/m60/' + str(i) + '.txt'
        #graspit
        postures_path = '/home/well/simulation_data5.0/test_init_posture/' + str(i) + '.txt'
        f = open(postures_path,'rb')
        postures = pickle.load(f)
        f.close()
        postures = np.array(postures)

        global_path = '/home/well/simulation_data3.0/test2/overall/' + str(i) + '.jpg'
        for j in patch_files:
            print(j)
            depth_path = depthes_path + j
            depth = image.img_to_array(image.load_img(depth_path))
            depth = normalizeImag(depth)
            depth_patches.append(depth)

            global_depth = image.img_to_array(image.load_img(global_path))
            global_depth = normalizeImag(global_depth)  # (128,128,1)
            global_depthes.append(global_depth)

        img_in = np.array(depth_patches)
        img_in1 = np.array(global_depthes)
        print(img_in.shape,img_in1.shape,poses.shape,postures.shape)
        a = model1.predict([img_in, img_in1,poses, postures])*0.12
        print(a)
        result = []
        for it in a:
            # it.tolist()
            result.append(it[0].item())
        confs_save_path = '/home/well/simulation_data5.0/test_quality/pi48/graspit/' + str(i) + '.txt'
        f = open(confs_save_path, 'w')
        json.dump(result, f)
        f.close()


def sim5_test():
    model1 = keras.models.load_model('/home/well/simulation_data5.0/model/pi29.h5',
                                     custom_objects={'keras': keras, 'tf': tf})
    #  Firstly test only one grasp
    for i in range(1):
        # for i in [3]:
        depth_patches = []
        grasp_confs_init = []

        depth_path = '/home/well/simulation_data5.0/test_depth_patches/3/0.jpg'

        grasp_conf_path = '/home/well/simulation_data5.0/test_grasp_confs/test_m_grasp_confs/3.txt'
        f = open(grasp_conf_path, 'r')
        grasp_conf = json.load(f)
        f.close()
        grasp_confs_init += grasp_conf


        depth = image.img_to_array(image.load_img(depth_path))
        depth = normalizeImag(depth)

        depth_patches.append(depth)


        img_in = depth_patches

        gradient = keras.backend.gradients(model1.output, model1.input)[1]
        iterate = keras.backend.function(model1.input, [gradient])

        grasp_confs_final = []

        for it in grasp_confs_init[0:1]:
            print(it)
            conf_old = np.array(it)
            conf_old = conf_old[np.newaxis, :]
            for times in range(10):
                a_old = model1.predict([img_in, conf_old]) * 0.3
                print(a_old)
                grad = iterate([img_in, conf_old])
                print(grad)
                # print(a_old)
                # print(conf_old)
                alpha = 0.3
                t = 10
                beta = 0.8

                conf_new = conf_old + t * grad[0]  # shape(1,23)
                a_new = model1.predict([img_in, conf_new]) * 0.3
                # while a_new < a_old + alpha * t * np.dot(grad[0][0].T, grad[0][0]):
                while a_new < a_old :
                    t = beta * t
                    conf_new = conf_old + t * grad[0]
                    a_new = model1.predict([img_in, conf_new]) * 0.3
                    print(a_new,t)
                # print(grad[0])
                # exit()
                conf_old = conf_new
                print(times)
            grasp_confs_final.append(conf_new[0].tolist())
        print(grasp_confs_final)
        confs_save_path = '/home/well/simulation_data5.0/test_final_grasp_confs/3.txt'
        f = open(confs_save_path, 'w')
        json.dump(grasp_confs_final, f)
        f.close()


def limit(limit_min,limit_max,a):
    for index, i in enumerate(a):
        if i < limit_min[index]:
            a[index]=limit_min[index]
        elif i > limit_max[index]:
            a[index] = limit_max[index]
    return a


def sim5_test1():
    model1 = keras.models.load_model('/home/well/simulation_data5.0/model/pi48.h5',
                                     custom_objects={'keras': keras, 'tf': tf})
    limit_min = [-0.3490, 0, 0, 0,
                 -0.3490, 0, 0, 0,
                 -0.3490, 0, 0, 0,
                 -1.047, 0, -0.5236, 0]
    limit_max = [0.3490, 1.57, 1.157, 1.57,
                 0.3490, 1.57, 1.157, 1.57,
                 0.3490, 1.57, 1.157, 1.57,
                 1.047, 1.222, 0.5236, 1.57]
    failure = [[1,6,15,17,23,25],[10,14],[2,5,11,13]]
    #Test only one grasp first
    for i in range(3):
        # for i in [3]:
        depth_patches = []
        grasp_confs_init = []

        global_depthes = []

        depthes_path = '/home/well/simulation_data5.0/test_patches/' + str(i) + '/'
        patch_files = os.listdir(depthes_path)
        patch_files.sort(key=lambda x: int(x[:-4]))

        grasp_conf_path = '/home/well/simulation_data5.0/test_100zxyzws/' + str(i) + '.txt'
        f = open(grasp_conf_path, 'r')
        grasp_conf = json.load(f)
        f.close()
        grasp_confs_init += grasp_conf
        grasp_confs_init = np.array(grasp_confs_init)
        poses = grasp_confs_init

        # postures_path = '/home/well/simulation_data5.0/test_init_posture/m60/' + str(i) + '.txt'
        # graspit
        postures_path = '/home/well/simulation_data5.0/test_init_posture/m60/' + str(i) + '.txt'
        f = open(postures_path, 'rb')
        postures = pickle.load(f)
        f.close()
        postures = np.array(postures)

        global_path = '/home/well/simulation_data3.0/test2/overall/' + str(i) + '.jpg'
        for j in patch_files:
            print(j)
            depth_path = depthes_path + j
            depth = image.img_to_array(image.load_img(depth_path))
            depth = normalizeImag(depth)
            depth_patches.append(depth)

            global_depth = image.img_to_array(image.load_img(global_path))
            global_depth = normalizeImag(global_depth)  # (128,128,1)
            global_depthes.append(global_depth)

        img_ins = np.array(depth_patches)
        img_in1s = np.array(global_depthes)


        gradient = keras.backend.gradients(model1.output, model1.input)[3]
        iterate = keras.backend.function(model1.input, [gradient])

        grasp_confs_final = []
        final_qualities = []
        for index,it in enumerate(poses):
            posture_old = postures[index]
            pose = it[np.newaxis,:]
            posture_old = posture_old[np.newaxis,:]
            img_in = img_ins[index]
            img_in = img_in[np.newaxis,:]
            img_in1 = img_in1s[index]
            img_in1 = img_in1[np.newaxis,:]
            print(posture_old)
            for times in range(10):
                a_old = model1.predict([img_in,img_in1, pose, posture_old])
                print(a_old)
                grad = iterate([img_in,img_in1, pose,posture_old])
                print(grad)
                # print(a_old)
                # print(conf_old)
                alpha = 0.3
                t = 10
                beta = 0.8

                posture_new = posture_old + t * grad[0]  # shape(1,23)
                posture_new = limit(limit_min,limit_max,posture_new[0])
                posture_new = posture_new[np.newaxis, :]
                a_new = model1.predict([img_in,img_in1, pose,posture_new])
                while a_new < a_old + alpha * t * np.dot(grad[0][0].T, grad[0][0]):
                # while a_new < a_old:
                    t = beta * t
                    posture_new = posture_old + t * grad[0]
                    posture_new = limit(limit_min, limit_max, posture_new[0])
                    posture_new = posture_new[np.newaxis, :]
                    a_new = model1.predict([img_in,img_in1, pose,posture_new])
                    if t < (1e-10):
                        break
                    print(a_new,t)

                posture_old = posture_new
                print(times)
            final_qualities.append(a_new[0][0].item())
            final = pose[0].tolist() + posture_old[0].tolist()
            grasp_confs_final.append(final)
        # print(grasp_confs_final)
        confs_save_path = '/home/well/simulation_data5.0/test_final_grasp_confs/pi48/' + str(i) +'.txt'
        f = open(confs_save_path, 'w')
        json.dump(grasp_confs_final, f)
        f.close()

        final_qualities_path = '/home/well/simulation_data5.0/test_quality/pi48/optimize/' + str(i) + '.txt'
        f = open(final_qualities_path, 'w')
        json.dump(final_qualities, f)
        f.close()

def sim5_test2():
    model1 = keras.models.load_model('/home/well/simulation_data5.0/model/pi42.h5',
                                     custom_objects={'keras': keras, 'tf': tf})

    limit_min = [-0.3490, 0, 0, 0,
                 -0.3490, 0, 0, 0,
                 -0.3490, 0, 0, 0,
                 -1.047, 0, -0.5236, 0]
    limit_max = [0.3490, 1.57, 1.157, 1.57,
                 0.3490, 1.57, 1.157, 1.57,
                 0.3490, 1.57, 1.157, 1.57,
                 1.047, 1.222, 0.5236, 1.57]
    #Test only one grasp first
    for i in range(3,4):
        # for i in [3]:
        depth_patches = []
        grasp_confs_init = []

        depthes_path = '/home/well/simulation_data5.0/test_depth_patches/' + str(i) + '/'
        patch_files = os.listdir(depthes_path)
        patch_files.sort(key=lambda x: int(x[:-4]))

        grasp_conf_path = '/home/well/simulation_data5.0/test_grasp_confs/test_m_grasp_confs/' + str(i) + '.txt'
        f = open(grasp_conf_path, 'r')
        grasp_conf = json.load(f)
        f.close()
        grasp_confs_init += grasp_conf
        grasp_confs_init = np.array(grasp_confs_init)
        poses = grasp_confs_init[:, :7]

        postures_path = '/home/well/simulation_data5.0/test_init_posture/m60/' + str(i) + '.txt'
        f = open(postures_path,'rb')
        postures = pickle.load(f)
        f.close()
        postures = np.array(postures)

        for j in patch_files:
            print(j)
            depth_path = depthes_path + j
            depth = image.img_to_array(image.load_img(depth_path))
            depth = normalizeImag(depth)
            depth_patches.append(depth)
        print(poses.shape,postures.shape)
        # grasp_confs_init += grasp_conf

        imgs = np.array(depth_patches)
        print(imgs.shape)
        print(poses[0],postures[0])



        gradient = keras.backend.gradients(model1.output, model1.input)[2]
        iterate = keras.backend.function(model1.input, [gradient])

        grasp_confs_final = []
        final_qualities = []
        for index,it in enumerate(poses):
            posture_old = postures[index]
            pose = it[np.newaxis,:]
            posture_old = posture_old[np.newaxis,:]
            img_in = imgs[index]
            img_in = img_in[np.newaxis,:]
            print(posture_old)
            for times in range(10):
                a_old = model1.predict([img_in, pose,posture_old])
                print(a_old)
                grad = iterate([img_in, pose,posture_old])
                print(grad)
                # print(a_old)
                # print(conf_old)
                alpha = 0.3
                t = 10
                beta = 0.8

                posture_new = posture_old + t * grad[0]  # shape(1,23)
                posture_new = limit(limit_min,limit_max,posture_new[0])
                posture_new = posture_new[np.newaxis, :]
                a_new = model1.predict([img_in, pose,posture_new])
                while a_new < a_old + alpha * t * np.dot(grad[0][0].T, grad[0][0]):
                    t = beta * t
                    posture_new = posture_old + t * grad[0]
                    posture_new = limit(limit_min, limit_max, posture_new[0])
                    posture_new = posture_new[np.newaxis, :]
                    a_new = model1.predict([img_in, pose,posture_new])
                    if t < (1e-10):
                        break
                    print(a_new,t)

                posture_old = posture_new
                print(times)
            final_qualities.append(a_new[0][0].item())
            final = pose[0].tolist() + posture_old[0].tolist()
            grasp_confs_final.append(final)
        # print(grasp_confs_final)
        confs_save_path = '/home/well/simulation_data5.0/test_final_grasp_confs/pi42/' + str(i) +'.txt'
        f = open(confs_save_path, 'w')
        json.dump(grasp_confs_final, f)
        f.close()

        final_qualities_path = '/home/well/simulation_data5.0/test_quality/pi42/optimize/' + str(i) + '.txt'
        f = open(final_qualities_path, 'w')
        json.dump(final_qualities, f)
        f.close()

def sim_test3_failure():
        model1 = keras.models.load_model('/home/well/simulation_data5.0/model/pi48.h5',
                                         custom_objects={'keras': keras, 'tf': tf})
        limit_min = [-0.3490, 0, 0, 0,
                     -0.3490, 0, 0, 0,
                     -0.3490, 0, 0, 0,
                     -1.047, 0, -0.5236, 0]
        limit_max = [0.3490, 1.57, 1.157, 1.57,
                     0.3490, 1.57, 1.157, 1.57,
                     0.3490, 1.57, 1.157, 1.57,
                     1.047, 1.222, 0.5236, 1.57]
        failure = [[],[0,3,4,8,10,13], [2,5, 12, 11], [0,9,22,21,39]]
       #Test only one grasp first
        for i in range(1,4):
            # for i in [3]:
            depth_patches = []
            grasp_confs_init = []

            global_depthes = []

            depthes_path = '/home/well/simulation_data5.0/test_patches/' + str(i) + '/'
            patch_files = os.listdir(depthes_path)
            patch_files.sort(key=lambda x: int(x[:-4]))

            grasp_conf_path = '/home/well/simulation_data5.0/test_100zxyzws/' + str(i) + '.txt'
            f = open(grasp_conf_path, 'r')
            grasp_conf = json.load(f)
            f.close()
            grasp_confs_init += grasp_conf
            grasp_confs_init = np.array(grasp_confs_init)
            poses = grasp_confs_init

            # postures_path = '/home/well/simulation_data5.0/test_init_posture/m60/' + str(i) + '.txt'
            # graspit
            postures_path = '/home/well/simulation_data5.0/test_init_posture/m60/' + str(i) + '.txt'
            f = open(postures_path, 'rb')
            postures = pickle.load(f)
            f.close()
            postures = np.array(postures)

            global_path = '/home/well/simulation_data3.0/test2/overall/' + str(i) + '.jpg'
            for j in patch_files:
                print(j)
                depth_path = depthes_path + j
                depth = image.img_to_array(image.load_img(depth_path))
                depth = normalizeImag(depth)
                depth_patches.append(depth)

                global_depth = image.img_to_array(image.load_img(global_path))
                global_depth = normalizeImag(global_depth)  # (128,128,1)
                global_depthes.append(global_depth)

            img_ins = np.array(depth_patches)
            img_in1s = np.array(global_depthes)

            gradient = keras.backend.gradients(model1.output, model1.input)[3]
            iterate = keras.backend.function(model1.input, [gradient])

            grasp_confs_final = []
            final_qualities = []
            for index in failure[i]:
                print('index',index)
                posture_old = postures[index]
                pose = poses[index]
                pose = pose[np.newaxis, :]
                posture_old = posture_old[np.newaxis, :]
                img_in = img_ins[index]
                img_in = img_in[np.newaxis, :]
                img_in1 = img_in1s[index]
                img_in1 = img_in1[np.newaxis, :]
                print(posture_old)
                for times in range(100):
                    a_old = model1.predict([img_in, img_in1, pose, posture_old])
                    print(a_old)
                    grad = iterate([img_in, img_in1, pose, posture_old])
                    print(grad)
                    # print(a_old)
                    # print(conf_old)
                    alpha = 0.3
                    t = 1
                    beta = 0.8

                    posture_new = posture_old + t * grad[0]  # shape(1,23)
                    posture_new = limit(limit_min, limit_max, posture_new[0])
                    posture_new = posture_new[np.newaxis, :]
                    a_new = model1.predict([img_in, img_in1, pose, posture_new])

                    maxtimes = 0
                    while a_new < a_old + alpha * t * np.dot(grad[0][0].T, grad[0][0]):
                        # while a_new < a_old:
                        t = beta * t
                        posture_new = posture_old + t * grad[0]
                        posture_new = limit(limit_min, limit_max, posture_new[0])
                        posture_new = posture_new[np.newaxis, :]
                        a_new = model1.predict([img_in, img_in1, pose, posture_new])
                        if maxtimes > 10:
                            break
                        print(a_new, t)
                        maxtimes += 1
                    posture_old = posture_new
                    print(times)
                final_qualities.append(a_new[0][0].item())
                final = pose[0].tolist() + posture_old[0].tolist()
                grasp_confs_final.append(final)
            # print(grasp_confs_final)
            confs_save_path = '/home/well/simulation_data5.0/test_final_grasp_confs/pi48/1/' + str(i) + '.txt'
            f = open(confs_save_path, 'w')
            json.dump(grasp_confs_final, f)
            f.close()

            final_qualities_path = '/home/well/simulation_data5.0/test_quality/pi48/optimize/' + str(i) + '.txt'
            f = open(final_qualities_path, 'w')
            json.dump(final_qualities, f)
            f.close()

def old_test():

    model1 = keras.models.load_model('/home/well/PycharmProjects/test/p6.h5')

    for i in range(1):
        patches = []
        # zxyzws = []
        #depthes = []
        # postures = []

        patches_path = '/home/well/simulation_data2.0/test2/old_patches/' + str(i)+'/'
        patch_files = os.listdir(patches_path)
        for j in patch_files:
            patch_path = patches_path + j
            patch = image.img_to_array(image.load_img(patch_path))
            patch = normalizeImag(patch)
            patches.append(patch)

        hand_names = ['rh_FFJ1', 'rh_FFJ2', 'rh_FFJ3', 'rh_FFJ4',
                      'rh_MFJ1', 'rh_MFJ2', 'rh_MFJ3', 'rh_MFJ4',
                      'rh_RFJ1', 'rh_RFJ2', 'rh_RFJ3', 'rh_RFJ4',
                      'rh_THJ1', 'rh_THJ2', 'rh_THJ4', 'rh_THJ5']
        graspit_names = ['rh_RFJ4', 'rh_RFJ3', 'rh_RFJ2', 'rh_RFJ1',
                         'rh_MFJ4', 'rh_MFJ3', 'rh_MFJ2', 'rh_MFJ1',
                         'rh_FFJ4', 'rh_FFJ3', 'rh_FFJ2', 'rh_FFJ1',
                         'rh_THJ5', 'rh_THJ4', 'rh_THJ2', 'rh_THJ1']
        postures_path = '/home/well/simulation_data2.0/test2/old_postures/'+str(i)+'.txt'
        a = model1.predict([patches])
        dofs = []
        print(a[16])
        for it in a:
            hand = dict(zip(hand_names,it))
            temp = []
            for key in graspit_names:
                if key == 'rh_RFJ4':
                    temp.append(-hand[key])
                temp.append(hand[key])
            dofs.append(temp)
        print(dofs[16])
        f = open(postures_path, 'wb')
        pickle.dump(dofs,f,0)
        f.close()
        # print('predict: ', a)

if __name__ =='__main__':
     #main()
    #test1()
    # test2()
    # test3()
    # test4()
    # test5_1()
    #test5()
    # old_test()
    # sim5_test1()
    # sim5_pre()
    #  sim5_pre1()
    sim_test3_failure()
