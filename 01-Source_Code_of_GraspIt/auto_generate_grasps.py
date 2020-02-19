#!/usr/bin/env python
# coding:utf-8
import rospy
import pickle
import sys
import numpy as np
from geometry_msgs.msg import Pose
from graspit_commander import GraspitCommander

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

from move2contact import move2contact

def write_file(grasp, file_name):
    dof_values = grasp.dofs
    dof_values = ' '.join([str(i) for i in dof_values ])
    position = grasp.pose.position
    p_x = position.x*1000.0
    p_y = position.y*1000.0
    p_z = position.z*1000.0
    
    orientation = grasp.pose.orientation
    o_x = orientation.x
    o_y = orientation.y
    o_z = orientation.z
    o_w = orientation.w
    file_name = '/home/well/graspit/worlds/' + file_name + '.xml'
    f = open(file_name,'w')
    world_file = '<?xml version="1.0" ?>\n'
    world_file += '<world>\n'
    world_file +='	<graspableBody>\n'
    world_file +='		<filename>models/objects/sim_model/model.xml</filename>\n'
    world_file +='		<transform>\n'
    world_file +='			<fullTransform>(+1 +0 +0 +0)[+0 +0 +0]</fullTransform>\n'
    world_file +='		</transform>\n'
    world_file +='	</graspableBody>\n'
    world_file +='	<robot>\n'
    world_file +='		<filename>models/robots/ShadowHandLast/shadowhandnew.xml</filename>\n'
    world_file +='		<dofValues>'
    world_file += dof_values+'</dofValues>\n'
    world_file +='		<transform>\n'
    world_file +='			<fullTransform>'
    world_file +='(' + str(o_w) +' '+ str(o_x)+ ' '  + str(o_y)+' ' + str(o_z)+ ')'
    world_file +='['+ str(p_x) +' '+ str(p_y) +' '+ str(p_z) + ']</fullTransform>\n'
    world_file +='		</transform>\n'
    world_file +='	</robot>\n'
    world_file +='</world>\n'
    
    f.write(world_file)
    f.close()

def writeFile(pose, dofs, file_name):
    dof_values = dofs
    dof_values = ' '.join([str(i) for i in dof_values ])
    position = pose.position
    p_x = position.x*1000.0
    p_y = position.y*1000.0
    p_z = (position.z)*1000.0 
    
    orientation = pose.orientation
    o_x = orientation.x
    o_y = orientation.y
    o_z = orientation.z
    o_w = orientation.w
    file_name = '/home/well/graspit/worlds/' + file_name + '.xml'
    f = open(file_name,'w')
    world_file = '<?xml version="1.0" ?>\n'
    world_file += '<world>\n'
    world_file +='	<graspableBody>\n'
    world_file +='		<filename>models/objects/sim_model/model.xml</filename>\n'
    world_file +='		<transform>\n'
    world_file +='			<fullTransform>(+1 +0 +0 +0)[+0 +0 +0]</fullTransform>\n'
    world_file +='		</transform>\n'
    world_file +='	</graspableBody>\n'
    world_file +='	<robot>\n'
    world_file +='		<filename>models/robots/ShadowHandLast/shadowhandnew.xml</filename>\n'
    world_file +='		<dofValues>'
    world_file += dof_values+'</dofValues>\n'
    world_file +='		<transform>\n'
    world_file +='			<fullTransform>'
    world_file +='(' + str(o_w) +' '+ str(o_x)+ ' '  + str(o_y)+' ' + str(o_z)+ ')'
    world_file +='['+ str(p_x) +' '+ str(p_y) +' '+ str(p_z) + ']</fullTransform>\n'
    world_file +='		</transform>\n'
    world_file +='	</robot>\n'
    world_file +='</world>\n'
    
    f.write(world_file)
    f.close()

def getHandPose(palmpose):
    wTp = np.array([[-1, 0, 0, palmpose[0]],
                    [0, -1, 0, palmpose[1]],
                    [0, 0, 1, palmpose[2]],
                    [0, 0, 0, 1]])   #手掌初始位姿
    pTh = np.array([[1, 0, 0, -0.068],
                    [0, 1, 0, 0.020],
                    [0, 0, 1, -0.012],
                    [0, 0, 0, 1]])
    wTh = np.dot(wTp, pTh)
    handpose = [wTh[0][3],wTh[1][3],wTh[2][3]]
    handrotm = [wTh[0][0:3],wTh[1][0:3],wTh[2][0:3]]
    return handpose, handrotm

#要分好几种情况,还是直接使用MATLAB中的rotm2quat函数
def rotm2quat(rotm):
    w = np.sqrt(1+rotm[0][0]+rotm[1][1]+rotm[2][2])
    x = (rotm[2][1]-rotm[1][2])/(4*w)
    y = (rotm[0][2]-rotm[2][0])/(4*w)
    z = (rotm[1][0]-rotm[0][1])/(4*w)
    return [w,x,y,z]

def randomPalmPosition(graspit, palm_pose_center):
    '''
    change the position of the palm randomly
    '''
    #hand_pose 是灵巧手在graspIT中的坐标系,palm_pose是自定义的坐标系,它们都相对于世界坐标系
    palm_pose_center = palm_pose_center  #人为设定的最优点
    palm_pose_x = np.random.normal(palm_pose_center[0],0.01,10)[0] #正态分布
    palm_pose_y = np.random.normal(palm_pose_center[1],0.01,10)[0]
    palm_pose = [palm_pose_x, palm_pose_y, palm_pose_center[2]]   #手掌初始位置
    print 'palm_pose:', palm_pose
    hand_pose_init, handrotm = getHandPose(palm_pose)
    print 'handrotm:', handrotm  #grapit中手坐标系关于世界坐标系的旋转矩阵
    hand_pose = Pose()
    #in graspit ,the unit is m
    hand_pose.position.x = hand_pose_init[0]
    hand_pose.position.y = hand_pose_init[1]
    hand_pose.position.z = hand_pose_init[2]
    hand_pose.orientation.w = 0
    hand_pose.orientation.x = 0
    hand_pose.orientation.y = 0
    hand_pose.orientation.z = 1
    rospy.sleep(1)
    graspit.setRobotPose(hand_pose)

def writeModelfile(model_index):
    modelfile_path = '/home/well/graspit/models/objects/sim_model/model.xml'
    model_index = str(model_index)
    f = open(modelfile_path,'w')    
    content ='<?xml version="1.0" ?>\n'
    content+='<root>\n'
    content+='	<material>plastic</material>\n'  
    content+='	<geometryFile type="Inventor">'+model_index+'.stl</geometryFile>\n'
    content+='</root>'	
    f.write(content)
    f.close()

def write_modelfile(model_path,model_index):
    f = open(model_path,'w')    
    content ='<?xml version="1.0" ?>\n'
    content+='<root>\n'
    content+='	<material>plastic</material>\n'  
    content+='	<geometryFile type="Inventor">'+str(model_index)+'.stl</geometryFile>\n'
    content+='</root>'	
    f.write(content)
    f.close()

def generateGrasps(model_index,palm_pose_center):
    '''
    configure EigenGrasp Planner, 
    start to search grasps and save the results
    '''

    graspit_udf = GraspitCommander()
    graspit_udf.clearWorld()
    world_file = 'compare_shadow'
    graspit_udf.loadWorld(world_file)
    palm_pose_center = palm_pose_center  #人为设定的最优点  
    good_grasps = []
    bad_grasps = []        
    for times in range(10):
        randomPalmPosition(graspit_udf,palm_pose_center)
        grasps = graspit_udf.planGrasps(search_space=SearchSpace(SearchSpace.SPACE_APPROACH), max_steps=70000)
            
            #select good grasps
        g = grasps.grasps
        length = len(g)
        for i in range(0, length):
            if g[i].epsilon_quality > 0.0:
                good_grasps.append(g[i])
            else:
                bad_grasps.append(g[i])
        print 'len_goodgrasps:',len(good_grasps) 
        print 'len_badgrasps:',len(bad_grasps) 
     
    #从后面几个开始,刚开始就应该自动化的
    model_index = str(model_index)
    #file_path = '/home/well/simulation_data1.0/graspit_data/'+model_index +'.txt'
    file_path = '/home/well/simulation_data5.0/bad_graspit_data/'+model_index +'.txt'

    #write 
    f = open(file_path, 'w')
    pickle.dump(bad_grasps, f, 0)
    f.close()   
    graspit_udf.clearWorld()
        
def generate_grasps(model_index,palm_pose_center,world_file,save_path):
    '''
    configure EigenGrasp Planner, 
    start to search grasps and save the results
    '''

    graspit_udf = GraspitCommander()
    graspit_udf.clearWorld()
    graspit_udf.loadWorld(world_file)
    palm_pose_center = palm_pose_center  #人为设定的最优点  
    good_grasps = []        
    for times in range(10):
        randomPalmPosition(graspit_udf,palm_pose_center)
        grasps = graspit_udf.planGrasps(search_space=SearchSpace(SearchSpace.SPACE_APPROACH), max_steps=70000)
            
            #select good grasps
        g = grasps.grasps
        length = len(g)
        for i in range(0, length):
            if g[i].epsilon_quality > 0.0:
                good_grasps.append(g[i])
        print 'len_goodgrasps:',len(good_grasps) 

     
    #从后面几个开始,刚开始就应该自动化的
    model_index = str(model_index)
    file_path = save_path + model_index +'.txt'
    #write 
    f = open(file_path, 'w')
    pickle.dump(good_grasps, f, 0)
    f.close()   
    graspit_udf.clearWorld()

def main():
    rospy.init_node('random_palm_position')
    num = int(sys.argv[1])
    #index = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,50,51,54,55,56,57,60,62]
    palm_pose_centers = [[0.06,0.04,0.0],[60.0/1000,45.0/1000, -20.0/1000],[70.0/1000,40.0/1000, -0.0/1000], [40.0/1000,100.0/1000, -0.0/1000], [60.0/1000,70.0/1000, -0.0/1000],[0.0,0,-0.04],[40.0 / 1000, 30.0 / 1000, -40.0 / 1000], [30.0/1000,30.0/1000, -40.0/1000], [30.0/1000,30.0/1000, -40.0/1000], [30.0/1000,00.0/1000, -60.0/1000],[20.0 / 1000, 30.0 / 1000, -50.0 / 1000],[0.01,0,-0.05],[30.0/1000,30.0/1000, -50.0/1000], [5.0/1000,30.0/1000, -50.0/1000], [0,0,-0.04],[25.0/1000,30.0/1000, -50.0/1000],[0,0,-0.04],[0,0,-0.08],[0,0,-0.03], [25.0/1000,30.0/1000, -55.0/1000] ,[0,-0.02,-0.03],[35.0 / 1000, 30.0 / 1000, -40.0 / 1000],[0,0,-0.09], [35.0/1000,30.0/1000, -40.0/1000], [35.0/1000,30.0/1000, -40.0/1000],[-0.01,0.02,-0.04], [35.0/1000,30.0/1000, -40.0/1000],[0,0.05,-0.08],
                         [35.0 / 1000, 0.0 / 1000, -50.0 / 1000],[0,0,-0.025], [0,0.025,-0.05],[0,0,-0.09],[35.0/1000,0.0/1000, -80.0/1000], [35.0/1000,20.0/1000, -50.0/1000], [25.0/1000,20.0/1000, -30.0/1000],
                         [35.0 / 1000, 00.0 / 1000, -60.0 / 1000],[15.0/1000,00.0/1000, -40.0/1000],[35.0/1000,20.0/1000, -50.0/1000],[35.0/1000,20.0/1000, -50.0/1000],[35.0/1000,0.0/1000, -70.0/1000],
                         [50.0 / 1000, 50.0 / 1000, -70.0 / 1000],[15.0/1000,50.0/1000, -45.0/1000],[0,0,-0.06],[0,-0.01,-0.05],
                         [0.02, 0.035, -0.06],[0.02, 0.03, -0.04], [0.03, 0.02, -0.04], [0.03, 0.04, -0.04], [0.03, 0.008, -0.04], [0.03, 0.008, -0.04], [0.01, 0.04, -0.04], [0.028, 0.04, -0.04], [0.01, 0.070, -0.04], [0.025, 0.02, -0.065], [0.025, 0.0, -0.055], [0.025, 0.0, -0.055], [0.025, 0.0, -0.038], [0.025, 0.0, -0.08], [0.025, 0.03, -0.05], [0.025, 0.03, -0.05], [0.025, 0.045, -0.05], [0.025, 0.025, -0.05], [0.025, 0.085, -0.05], [0.005, 0.025, -0.05], [0.025, 0.01, -0.04]]
    #44~64
    # palm_pose_centers = [[0.02, 0.035, -0.04],[0.02, 0.03, -0.04], [0.03, 0.02, -0.04], [0.03, 0.04, -0.04], [0.03, 0.008, -0.04], [0.03, 0.008, -0.04], [0.028, 0.04, -0.04], [0.028, 0.04, -0.04], [0.028, 0.070, -0.04], [0.025, 0.02, -0.055], [0.025, 0.0, -0.055], [0.025, 0.0, -0.055], [0.025, 0.0, -0.038], [0.025, 0.0, -0.07], [0.025, 0.03, -0.05], [0.025, 0.03, -0.05], [0.025, 0.045, -0.05], [0.025, 0.025, -0.05], [0.025, 0.045, -0.05], [0.025, 0.025, -0.05], [0.025, 0.01, -0.04]]
    length = len(palm_pose_centers)
    print 'input s to start:'
    if raw_input() == 's':
        pass
    else:
        exit()
    for i,j in enumerate(palm_pose_centers):
        if i < num:
            continue
        model_index = i
        print i
        writeModelfile(model_index)
        generateGrasps(model_index,j)

def select_grasps():
    '''
    修改抓取,并筛选出来
    ''' 
    rospy.init_node('random_palm_position')
    num = sys.argv[1]
    num1 = int(sys.argv[2])
    grasps_path = '/home/well/simulation_data1.0/graspit_data/' + num +'.txt'
    f = open(grasps_path,'r')
    grasps = pickle.load(f)
    f.close()
    writeModelfile(num)
    world_file = 'compare_shadow'
    graspit_udf = GraspitCommander()
    poses_path = '/home/well/simulation_data1.0/modify_grasps/poses/'+ num +'.txt'
    dofs_path = '/home/well/simulation_data1.0/modify_grasps/dofs/' + num + '.txt'
    try:
        f = open(poses_path, 'r')
        poses = pickle.load(f)
        f.close()
        f = open(dofs_path, 'r')
        dofs = pickle.load(f)
        f.close()
    except:
        print 'error'
        dofs = []
        poses = []
    print len(dofs),len(poses),len(grasps) 
    for index,i in enumerate(grasps):
        if index < num1:
            continue
        print 'index:',index
        write_file(i,world_file)
        graspit_udf.clearWorld()
        graspit_udf.loadWorld(world_file)
        graspit_udf.toggleAllCollisions(False)
        print 'if modify:input m; if del:input d; if do nothing: input c'
        temp = raw_input()
        if temp == 'm':
            while True:
                graspit_udf.toggleAllCollisions(True)
                final_dofs = [0.0, 1.57, 1.57, 1.57, 0.0, 1.57, 1.57, 1.57, 0.0, 1.57, 1.57, 1.57, 1.047, 1.222, 0.0, 0.524, 1.57]
                final_dofs[0] = i.dofs[0]
                final_dofs[4] = i.dofs[4]
                final_dofs[8] = i.dofs[8]
                if raw_input()=='m':
                    pass
                move2contact(final_dofs,graspit_udf)
                q = graspit_udf.computeQuality()
                print 'qulity:' , q
                print 'if modify finished: input f'
                graspit_udf.toggleAllCollisions(False)
                if raw_input()=='f':
                    break
                
            new_dofs = graspit_udf.getRobot().robot.dofs
            new_pose = graspit_udf.getRobot().robot.pose                
            poses.append(new_pose)
            dofs.append(new_dofs)
        elif temp =='c' :
            poses.append(i.pose)
            dofs.append(i.dofs)
        else:
            continue
        #f = open(poses_path, 'w')
       # pickle.dump(poses, f, 0)
        #f.close() 
        #f = open(dofs_path, 'w')
        #pickle.dump(dofs, f, 0)
        #f.close() 
    print len(dofs),len(poses),len(grasps)    


def test_grasps():
    '''
    查看抓取,确保无误
    ''' 
    rospy.init_node('random_palm_position')
    num = sys.argv[1]
    poses_path = '/home/well/simulation_data1.0/modify_grasps/poses/' + num +'.txt'
    f = open(poses_path,'r')
    poses = pickle.load(f)
    f.close()
    dofs_path = '/home/well/simulation_data1.0/modify_grasps/dofs/' + num +'.txt'
    f = open(dofs_path,'r')
    dofs = pickle.load(f)
    f.close()

    writeModelfile(num)
    world_file = 'compare_shadow'
    graspit_udf = GraspitCommander()
    poses_path = '/home/well/simulation_data1.0/final_grasps/poses/'+ num +'.txt'
    dofs_path = '/home/well/simulation_data1.0/final_grasps/dofs/' + num + '.txt'
    try:
        f = open(poses_path, 'r')
        final_poses = pickle.load(f)
        f.close()
        f = open(dofs_path, 'r')
        final_dofs = pickle.load(f)
        f.close()
    except:
        print 'error'
        final_dofs = []
        final_poses = []
    print len(dofs),len(poses)
    for index,i in enumerate(poses):
        writeFile(i,dofs[index],world_file)
        graspit_udf.clearWorld()
        graspit_udf.loadWorld(world_file)
        print 'if del:input d; if do nothing: input c'
        temp = raw_input()
        if temp =='c' :
            final_poses.append(i)
            final_dofs.append(dofs[index])
        else:
            continue
        f = open(poses_path, 'w')
        pickle.dump(final_poses, f, 0)
        f.close() 
        f = open(dofs_path, 'w')
        pickle.dump(final_dofs, f, 0)
        f.close() 
    print len(dofs),len(poses)   


def test_z():
    rospy.init_node('random_palm_position')
    num = int(sys.argv[1])
    z_size = [0,0,0,0,0,
             0.0334,0.0371,0.033,0.0326,0.06,
             0.0415,0.038,0.0445,0.043,0.032,
             0.0358,0.033,0.0711,0.021,0.05,
             0.0261,0.0429,0.0837,0.014,0.015,
             0.0397,0.0394,0.0697,0.0556,0.020,
             0.0411,0.069,0.0758,0.0455,0.0219,
             0.0635,0.034,0.0453,0.0453,0.0595,
             0.0657,0.037,0.0552,0.0404,0.056,
             0.0524,0.0397,0.032,0.03,0.03,
             0.0329,0.0382,0.03,0.055,0.0434,
             0.0428,0.015,0.0774,0.040,0.0375,
             0.029,0.041,0.037,0.0358,0.02]
    palm_pose_centers = [[0.06,0.04,0.0],[60.0/1000,45.0/1000, -20.0/1000],[70.0/1000,40.0/1000, -0.0/1000], [40.0/1000,100.0/1000, -0.0/1000], [60.0/1000,70.0/1000, -0.0/1000],[0.0,0,-0.04],[40.0 / 1000, 30.0 / 1000, -40.0 / 1000], [30.0/1000,30.0/1000, -40.0/1000], [30.0/1000,30.0/1000, -40.0/1000], [30.0/1000,00.0/1000, -60.0/1000],[20.0 / 1000, 30.0 / 1000, -50.0 / 1000],[0.01,0,-0.05],[30.0/1000,30.0/1000, -50.0/1000], [5.0/1000,30.0/1000, -50.0/1000], [0,0,-0.04],[25.0/1000,30.0/1000, -50.0/1000],[0,0,-0.04],[0,0,-0.08],[0,0,-0.03], [25.0/1000,30.0/1000, -55.0/1000] ,[0,-0.02,-0.03],[35.0 / 1000, 30.0 / 1000, -40.0 / 1000],[0,0,-0.09], [35.0/1000,30.0/1000, -40.0/1000], [35.0/1000,30.0/1000, -40.0/1000],[-0.01,0.02,-0.04], [35.0/1000,30.0/1000, -40.0/1000],[0,0.05,-0.08],
                         [35.0 / 1000, 0.0 / 1000, -50.0 / 1000],[0,0,-0.025], [0,0.025,-0.05],[0,0,-0.09],[35.0/1000,0.0/1000, -80.0/1000], [35.0/1000,20.0/1000, -50.0/1000], [25.0/1000,20.0/1000, -30.0/1000],
                         [35.0 / 1000, 00.0 / 1000, -60.0 / 1000],[15.0/1000,00.0/1000, -40.0/1000],[35.0/1000,20.0/1000, -50.0/1000],[35.0/1000,20.0/1000, -50.0/1000],[35.0/1000,0.0/1000, -70.0/1000],
                         [50.0 / 1000, 50.0 / 1000, -70.0 / 1000],[15.0/1000,50.0/1000, -45.0/1000],[0,0,-0.06],[0,-0.01,-0.05],
                         [0.02, 0.035, -0.06],[0.02, 0.03, -0.04], [0.03, 0.02, -0.04], [0.03, 0.04, -0.04], [0.03, 0.008, -0.04], [0.03, 0.008, -0.04], [0.01, 0.04, -0.04], [0.028, 0.04, -0.04], [0.01, 0.070, -0.04], [0.025, 0.02, -0.065], [0.025, 0.0, -0.055], [0.025, 0.0, -0.055], [0.025, 0.0, -0.038], [0.025, 0.0, -0.08], [0.025, 0.03, -0.05], [0.025, 0.03, -0.05], [0.025, 0.045, -0.05], [0.025, 0.025, -0.05], [0.025, 0.085, -0.05], [0.005, 0.025, -0.05], [0.025, 0.01, -0.04]]
    length = len(palm_pose_centers)
    graspit_udf = GraspitCommander()
    world_file = 'compare_shadow'
    for i,j in enumerate(palm_pose_centers):
        if i < num:
            continue
        model_index = i
        print i
        writeModelfile(model_index)
        graspit_udf.clearWorld()
        graspit_udf.loadWorld(world_file)
        j[0] = 0
        j[1] = 0
        j[-1] = -z_size[i]
        palm_pose_center = j  #人为设定的最优点  
        randomPalmPosition(graspit_udf,palm_pose_center)
        graspit_udf.toggleAllCollisions(False)
        if raw_input() == 'c':
            pass

def test2():
    rospy.init_node('random_palm_position')
    index = [0,1,2,3,4,5]
    palm_pose_centers = [[53.0/1000,50.0/1000, -10.0/1000],[30.0/1000,50.0/1000, -10.0/1000], [32.0/1000,100.0/1000, -10.0/1000], [43.0/1000,43.0/1000, -10.0/1000],[60.0/1000,40.0/1000,-10.0/1000],[60.0/1000,40.0/1000,-10.0/1000]]
    modelfile_path = '/home/well/graspit/models/objects/test2_model/model.xml'
    world_file = 'test2_shadow'
    save_path = '/home/well/simulation_data2.0/test2/graspit_data/'
    print (len(index),len(palm_pose_centers))
    print 'input s to start:'
    if raw_input() == 's':
        pass
    else:
        exit()
    for i,j in enumerate(index):
        if i in [0,1,2,3]:
           pass
        else:
            continue
        print i,j
        model_index = j
        write_modelfile(modelfile_path,model_index)
        generate_grasps(model_index,palm_pose_centers[i],world_file,save_path)

def read_file():
    for i in range(65):
        zxyzws_path = '/home/well/simulation_data1.0/zxyzws/'+str(i)+ '.txt'
        save_path = '/home/well/simulation_data1.0/modify_grasps/zxyzws/' + str(i)+ '.txt'
        f = open(zxyzws_path,'rb')
        zxyzws = pickle.load(f)
        f.close()
        f = open(save_path, 'wb')
        pickle.dump(zxyzws, f, 0)
        f.close()       

if __name__ == '__main__':
     #test2()
     select_grasps()
     #main()
