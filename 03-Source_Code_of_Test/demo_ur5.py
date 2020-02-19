#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg


ur5_pose=[]
def read_pose(data):
    global ur5_pose
    ur5_pose=[data.position.x,data.position.y,data.position.z,
              data.orientation.x,data.orientation.y,data.orientation.z,data.orientation.w]

if __name__ == '__main__':
    moveit_commander.roscpp_initialize(sys.argv)
    rospy.init_node('demo',anonymous=True)
    #rospy.Subscriber('/ros_msg',geometry_msgs.msg.Pose,read_pose)
    rospy.sleep(1)
    robot=moveit_commander.RobotCommander()
    scene=moveit_commander.PlanningSceneInterface()
    group=moveit_commander.MoveGroupCommander('right_arm')
    group.set_pose_reference_frame('/ur5_arm_base_link')
    display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path',
                                               moveit_msgs.msg.DisplayTrajectory,
                                               queue_size=20)
    print '========reference frame:%s' %group.get_pose_reference_frame()
    print '========reference end:%s' %group.get_end_effector_link()
    print '========robot groups:'
    print robot.get_group_names()
    print '=======printing robot state'
    print robot.get_current_state()
    print '==============================='



    joints_names=['ur5_arm_shoulder_pan_joint','ur5_arm_shoulder_lift_joint',
                  'ur5_arm_elbow_joint','ur5_arm_wrist_1_joint',
                  'ur5_arm_wrist_2_joint','ur5_arm_wrist_3_joint']
    
    start_states = [-1.5656865278827112, -0.510897461568014, -2.4022160212146204, -1.885188404713766, -1.623455826436178, -1.5901487509356897]
    start_states = [1.574569582939148, -2.7520349661456507, 2.2072672843933105, 2.4807510375976562, -1.7042854467975062, 0.03943634033203125]
    joints_values = [-1.5653265158282679, -1.6535943190204065, -1.3298404852496546, -3.1251190344439905, -1.8060310522662562, -1.590052906666891]

    final_states = [-1.3774836699115198, -1.7190240065204065, -1.6392996946917933, -2.810662094746725, -1.9035609404193323, -1.6153386274920862]
    print 'plan0'
    print 'input s to start ur5'
    if raw_input() == 's':
	    pass
#plan0,初始状态
    group.set_joint_value_target(start_states)
    plan0=group.plan()
    group.execute(plan0)
    
    print 'input s to start ur5'
    if raw_input() == 's':
	    exit()
#plan1.中间状态 
    group.set_joint_value_target(joints_values)   
    plan1=group.plan()
    group.execute(plan1)
    rospy.sleep(1)    #最好停一下,太快,会导致Goal start doesn't match current pose,给robot反应时间
#plan2, 中间灵巧手姿态调整
    pose_target=geometry_msgs.msg.Pose()
    print 'ur5_pose',ur5_pose
    pose_target.orientation.w=ur5_pose[6]
    pose_target.orientation.x=ur5_pose[3]
    pose_target.orientation.y=ur5_pose[4]
    pose_target.orientation.z=ur5_pose[5]

    pose_target.position.x=ur5_pose[0]+0.07
    pose_target.position.y=ur5_pose[1]
    pose_target.position.z=ur5_pose[2]
    group.set_pose_target(pose_target)
    print 'pose_target',pose_target
    plan2=group.plan()

    while True:
        rospy.sleep(0.5)
        display_trajectory = moveit_msgs.msg.DisplayTrajectory()
        display_trajectory.trajectory_start = robot.get_current_state()
        display_trajectory.trajectory.append(plan2)
        display_trajectory_publisher.publish(display_trajectory);
        print 'show plan2 if continue:input c'
        if raw_input()=='c':
            break
        plan2=group.plan()

    #print 'continue:c'
    #if raw_input() == 'c':
     #   pass
    group.execute(plan2)
    rospy.sleep(1)
#plan2,抓取状态
    pose_target=geometry_msgs.msg.Pose()
    print 'ur5_pose',ur5_pose
    pose_target.orientation.w=ur5_pose[6]
    pose_target.orientation.x=ur5_pose[3]
    pose_target.orientation.y=ur5_pose[4]
    pose_target.orientation.z=ur5_pose[5]

    pose_target.position.x=ur5_pose[0]
    pose_target.position.y=ur5_pose[1]
    pose_target.position.z=ur5_pose[2]
    group.set_pose_target(pose_target)
    plan2=group.plan()
    print 'pose_target',pose_target

    display_trajectory = moveit_msgs.msg.DisplayTrajectory()
    display_trajectory.trajectory_start = robot.get_current_state()
    display_trajectory.trajectory.append(plan2)
    # Publish
    display_trajectory_publisher.publish(display_trajectory);

    print 'continue:c'
    if raw_input() == 'c':
        pass
    group.execute(plan2)
    rospy.sleep(1)
#plan3,终止状态
   # print 'c to continue' 
    pose_target.position.z=ur5_pose[2]+0.1
    group.set_pose_target(pose_target)
    #group.set_joint_value_target(final_states)
    plan3=group.plan()

    while True:
        rospy.sleep(0.5)
        display_trajectory = moveit_msgs.msg.DisplayTrajectory()
        display_trajectory.trajectory_start = robot.get_current_state()
        display_trajectory.trajectory.append(plan3)
        display_trajectory_publisher.publish(display_trajectory);
        print 'show plan3 if ok to continue:input c'
        if raw_input()=='c':
            break
        plan3=group.plan()
    #if raw_input() == 'c':
    group.execute(plan3)
    rospy.sleep(1)
    print 'finish:input f'
#plan4,回到初始状态
    group.set_joint_value_target(start_states)
    plan0=group.plan()
    if raw_input() == 'f':
        group.execute(plan0)
    exit()
