# -*- coding: utf-8 -*-
'''
Obtain the slant area from the picture:
first rotate the picture reversely by the corresponding angle, and then intercept the corresponding area
'''

from PIL import Image
import math
import random

def get_patch(depth_path, num, *args):
    '''

    :param depth_path: File location
    :param num: Rotation angle, greater than or equal to 0, less than 90, not applicable to 90
    :param args:The center position and size of the patch
    :return: patch
    '''
    img = Image.open(depth_path)
    img_size = img.size
    radians = math.radians(num)

    # The coordinates of the center point of the patch after the image is rotated, clockwise is positive
    x = int(round((args[0][0]-img_size[0]/2)*math.cos(radians)-(args[0][1]-img_size[1]/2)*math.sin(radians)+img_size[0]/2))
    y = int(round((args[0][0]-img_size[0]/2)*math.sin(radians)+(args[0][1]-img_size[1]/2)*math.cos(radians)+img_size[1]/2))
    img2 = img.rotate(-num)  # clockwise is positive
    patch = img2.crop((x-args[1][0]/2, y-args[1][1]/2, x+args[1][0]/2, y+args[1][1]/2))
    return patch


if __name__ == '__main__':


    # for i in range(4,6):
    # #    i = 1
    #     depth_path = '/home/well/simulation_data2.0/test2/new_depth/' + str(i) + '.jpg'
    #     center = [295, 370]
    #     patch_size = [128, 128]
    #     angle = 0
    #     img = get_patch(depth_path, angle, center, patch_size)  #Enter the picture path \central position of patch \rotation angle \patch size
    #     save_path = '/home/well/simulation_data2.0/test2/overall/' + str(i) + '.jpg'
    #     img.save(save_path)



    for i in range(65):
        rgb_path = '/home/well/simulation_data3.0/test5/train_dataset1.0/rgb/' + str(i) + '.jpg'
        depth_path = '/home/well/simulation_data3.0/test5/train_dataset1.0/depth/' + str(i) + '.jpg'
        cur_path = '/home/well/simulation_data3.0/test5/train_dataset1.0/curvature/' + str(i) + '.jpg'
        norm_path = '/home/well/simulation_data3.0/test5/train_dataset1.0/normal/' + str(i) + '.jpg'

        center = [280,350]
        patch_size = [200, 200]
        angle = 0

        img = get_patch(rgb_path, angle, center, patch_size)  #Enter the picture path \central position of patch \rotation angle \patch size
        save_path = '/home/well/simulation_data3.0/test5/train_dataset1.0/rgb_patches/' + str(i) + '.jpg'
        img.save(save_path)

        img = get_patch(depth_path, angle, center, patch_size)  
        save_path = '/home/well/simulation_data3.0/test5/train_dataset1.0/depth_patches/' + str(i) + '.jpg'
        img.save(save_path)

        img = get_patch(cur_path, angle, center, patch_size)  
        save_path = '/home/well/simulation_data3.0/test5/train_dataset1.0/cur_patches/' + str(i) + '.jpg'
        img.save(save_path)

        img = get_patch(norm_path, angle, center, patch_size)  
        save_path = '/home/well/simulation_data3.0/test5/train_dataset1.0/normal_patches/' + str(i) + '.jpg'
        img.save(save_path)



    for i in range(4):
        rgb_path = '/home/well/simulation_data3.0/test5/test_dataset1.0/rgb/' + str(i) + '.jpg'
        depth_path = '/home/well/simulation_data3.0/test5/test_dataset1.0/depth/' + str(i) + '.jpg'
        cur_path = '/home/well/simulation_data3.0/test5/test_dataset1.0/cur/' + str(i) + '.jpg'
        norm_path = '/home/well/simulation_data3.0/test5/test_dataset1.0/normal/' + str(i) + '.jpg'

        center = [280, 350]
        patch_size = [200, 200]
        angle = 0

        img = get_patch(rgb_path, angle, center, patch_size)  #Enter the picture path \central position of patch \rotation angle \patch size
        save_path = '/home/well/simulation_data3.0/test5/test_dataset1.0/rgb_patches/' + str(i) + '.jpg'
        img.save(save_path)

        img = get_patch(depth_path, angle, center, patch_size)  
        save_path = '/home/well/simulation_data3.0/test5/test_dataset1.0/depth_patches/' + str(i) + '.jpg'
        img.save(save_path)

        img = get_patch(cur_path, angle, center, patch_size) 
        save_path = '/home/well/simulation_data3.0/test5/test_dataset1.0/cur_patches/' + str(i) + '.jpg'
        img.save(save_path)

        img = get_patch(norm_path, angle, center, patch_size)  
        save_path = '/home/well/simulation_data3.0/test5/test_dataset1.0/normal_patches/' + str(i) + '.jpg'
        img.save(save_path)
