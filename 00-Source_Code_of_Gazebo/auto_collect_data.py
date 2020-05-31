#!/usr/bin/env python
#coding:utf-8
import os
import rospy
from sensor_msgs.msg import Image
import cv2
import numpy as np
import copy
from cv_bridge import CvBridge
import sys



def rgb_callback(data,args):
    bridge = CvBridge()
    cv_image = bridge.imgmsg_to_cv2(data)
    file_path = '/home/well/simulation_data/rgb/'+args+'.jpg'
    cv2.imwrite(file_path, cv_image)   

def depth_callback(data,args):
    bridge = CvBridge()
    cv_image = bridge.imgmsg_to_cv2(data)
    cv2.normalize(cv_image, cv_image, 0, 1, cv2.NORM_MINMAX)
    file_path = '/home/well/simulation_data/depth/'+args+'.jpg'
    cv2.imwrite(file_path, cv_image*255)  
     

def callback(data):
    bridge = CvBridge()
    cv_image = bridge.imgmsg_to_cv2(data)
    cv2.imwrite('/home/well/1.jpg', cv_image)    

def load_model(num,name):
    #load model files
    file_path = '/home/well/simulation_data/gazebo_data/sdf_file/o'+num+'.sdf'
    #name = '"model"'
    command = 'rosrun gazebo_ros spawn_model -sdf -file ' + file_path + ' -model ' + '\"' + name +'\"'
    os.system(command)

def del_model(name):
    #delete model files
    command = 'rosservice call /gazebo/delete_model "model_name: ' +'\'' + name + '\'' +'\"'
    os.system(command)

if __name__ == '__main__':
    for num in range(65):
        print num
        command = 'rosrun gazebo_ros collect_data.py ' + str(num)
        os.system(command)
        rospy.sleep(5)
#    rospy.init_node('collect_image', anonymous = True)
    #num = sys.argv[-1]
#    for num in range(65):
#        num = str(num)
##        del_model('object')
    #load_model('cube','standard')
#        load_model(num,'object')
    #Subscribe to image topic and save
    #print 'input s to start:' #Detect object coordinate system
    #if raw_input() == 's':
    #    pass
    #else:
    #    exit()

 #       rospy.sleep(1)
#        rospy.Subscriber('/kinect/rgb/image_raw', Image, rgb_callback,num)
#        rospy.sleep(1)
#
 #       rospy.Subscriber('/kinect/depth/image_raw', Image,depth_callback,num)
 #       rospy.sleep(1)
 #       print 'input f to finish:',num  #Save world files, and save image files
 #       if raw_input() == 'f':
 #           pass



