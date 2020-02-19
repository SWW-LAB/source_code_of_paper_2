#!/usr/bin/env python
#coding:utf-8
import os
import rospy
from sensor_msgs.msg import Image, PointCloud2
from sensor_msgs import point_cloud2
import cv2
import numpy as np
import copy
from cv_bridge import CvBridge
import sys


def points_callback(data,args):
    gen = point_cloud2.read_points(data,skip_nans = False)
    rospy.sleep(1)
    normal_points = np.array(list(gen))
    normal_points = np.reshape(normal_points, (480, 640, 4))
    normal_points[np.logical_or(np.logical_or(np.isinf(normal_points), np.isneginf(normal_points)),
                                    np.isnan(normal_points))] = 0
    normal = normal_points
    for i in xrange(3):
        normal[:, :, i] = 255. * (normal[:, :, i] - np.min(normal[:, :, i])) / \
                (np.max(normal[:, :, i]) - np.min(normal[:, :, i]))
    normal = normal.astype('uint8')
    cv2.imwrite(args[0], normal)

    curv = normal_points[:,:,3]
    curv = 255. * (curv - np.min(curv)) / (np.max(curv) - np.min(curv))
    cv2.imwrite(args[1], curv)

def rgb_callback(data,args):
    bridge = CvBridge()
    cv_image = bridge.imgmsg_to_cv2(data)
    file_path = args 
    cv2.imwrite(file_path, cv_image)   

def depth_callback(data,args):
    bridge = CvBridge()
    cv_image = bridge.imgmsg_to_cv2(data)
    cv2.normalize(cv_image, cv_image, 0, 1, cv2.NORM_MINMAX)
    file_path = args 
    cv2.imwrite(file_path, cv_image*255)  
     

def callback(data):
    bridge = CvBridge()
    cv_image = bridge.imgmsg_to_cv2(data)
    cv2.imwrite('/home/well/1.jpg', cv_image)    

def load_model(sdf_path,name):
    #加载模型文件
    file_path = sdf_path
    #name = '"model"'
    command = 'rosrun gazebo_ros spawn_model -sdf -file ' + file_path + ' -model ' + '\"' + name +'\"'
    os.system(command)

def del_model(name):
    #删除模型文件
    command = 'rosservice call /gazebo/delete_model "model_name: ' +'\'' + name + '\'' +'\"'
    os.system(command)

def test():
    rospy.init_node('collect_image', anonymous = True)
    num = sys.argv[-1]
    del_model('object')
    #load_model('cube','standard')
    sdf_path = '/home/well/simulation_data3.0/test2/gazebo_data/o' + num +'.sdf'
    load_model(sdf_path,'object')
    #订阅image topic 并保存
    #print 'input s to start:' #检测物体坐标系
    #if raw_input() == 's':
     #   pass
    #else:
    #    exit()

    rospy.sleep(1)
    rgb_path = '/home/well/simulation_data3.0/test5/test_dataset/rgb/'+num+'.jpg'
    rospy.Subscriber('/kinect/rgb/image_raw', Image, rgb_callback,rgb_path)
    rospy.sleep(1)
    
    #depth_path = '/home/well/simulation_data2.0/test2/depth/'+num+'.jpg'
    #rospy.Subscriber('/kinect/depth/image_raw', Image,depth_callback,depth_path)
    rospy.sleep(1)
   
    normal_path = '/home/well/simulation_data3.0/test5/test_dataset/normal/' + num + '.jpg'
    curv_path = '/home/well/simulation_data3.0/test5/test_dataset/cur/' + num + '.jpg'
    rospy.Subscriber('/kinect/depth/points', PointCloud2,points_callback,[normal_path,curv_path])
    rospy.sleep(5)
    print 'input f to finish:'  #保存世界文件,以及保存图像文件
    if raw_input() == 'f':
        pass


def test1():
    rospy.init_node('collect_image', anonymous = True)
    num = sys.argv[-1]
    del_model('object')
    #load_model('cube','standard')
    sdf_path = '/home/well/simulation_data3.0/test2/gazebo_data/o' + num +'.sdf'
    load_model('','object')
    #订阅image topic 并保存
    #print 'input s to start:' #检测物体坐标系
    #if raw_input() == 's':
     #   pass
    #else:
    #    exit()

    rospy.sleep(1)
    rgb_path = '/home/well/simulation_data3.0/test5/test_dataset/rgb/'+num+'.jpg'
    rospy.Subscriber('/kinect/rgb/image_raw', Image, rgb_callback,rgb_path)
    rospy.sleep(1)
    
    #depth_path = '/home/well/simulation_data2.0/test2/depth/'+num+'.jpg'
    #rospy.Subscriber('/kinect/depth/image_raw', Image,depth_callback,depth_path)
    rospy.sleep(1)
   
    normal_path = '/home/well/simulation_data3.0/test5/test_dataset/normal/' + num + '.jpg'
    curv_path = '/home/well/simulation_data3.0/test5/test_dataset/cur/' + num + '.jpg'
    rospy.Subscriber('/kinect/depth/points', PointCloud2,points_callback,[normal_path,curv_path])
    rospy.sleep(5)
    print 'input f to finish:'  #保存世界文件,以及保存图像文件
    if raw_input() == 'f':
        pass


if __name__ == '__main__':
    
    #test1()
    #exit()


    rospy.init_node('collect_image', anonymous = True)
    num = sys.argv[-1]
    del_model('object')
    #load_model('cube','standard')
    #sdf_path = '/home/well/simulation_data/gazebo_data/sdf_file/o' + num +'.sdf'
    sdf_path = '/home/well/simulation_data/gazebo_data/sdf_file/ocube.sdf'
    load_model(sdf_path,'object')
    #订阅image topic 并保存
    #print 'input s to start:' #检测物体坐标系
    #if raw_input() == 's':
     #   pass
    #else:
    #    exit()

    #rospy.sleep(1)
    #rgb_path = '/home/well/simulation_data/test2/'+num+'.jpg'
    #rospy.Subscriber('/kinect/rgb/image_raw', Image, rgb_callback,rgb_path)
    #rospy.sleep(1)
    
    #depth_path = '/home/well/simulation_data2.0/test2/depth/'+num+'.jpg'
    depth_path = '/home/well/fig4.jpg'
    rospy.Subscriber('/kinect/depth/image_raw', Image,depth_callback,depth_path)
    rospy.sleep(1)
   
    #normal_path = '/home/well/simulation_data3.0/test5/normal/' + num + '.jpg'
    #curv_path = '/home/well/simulation_data3.0/test5/curvature/' + num + '.jpg'
    #rospy.Subscriber('/kinect/depth/points', PointCloud2,points_callback,[normal_path,curv_path])
    #rospy.sleep(5)
    #print 'input f to finish:'  #保存世界文件,以及保存图像文件
    #if raw_input() == 'f':
    #    pass



