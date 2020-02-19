﻿real_predict.py:实际实验的网络预测结果。
sim_predict.py:仿真实验的网络预测结果。
demo_new_cnn_grasp.py:使用real_predict.py生成的抓取手势操作shadow hand进行抓取。
demo_ur5.py：UR5的规划程序，根据topic中发布的shadow hand的位姿，使UR5到达指定位姿。
ros_matlab_multi_finger:喻群超师兄的抓取框检测网络，用于生成抓取框，以及发布灵巧手的位姿信息。运行顺序：cnn_init.m -> main_image_deep.m ->well_cal.m.
real_predict.py: Network prediction results from actual experiments.
sim_predict.py: network prediction results of simulation experiments.
demo_new_cnn_grasp.py: Use the grasping posture generated by real_predict.py to grasp.
demo_ur5.py: The UR5 planning code, according to the pose of the shadow hand published in the topic, to make UR5 reach the specified pose.
ros_matlab_multi_finger: Grasping rectangle detection networks (GRDNs) is used to generate the grasp rectangle and publish pose information of the shadow hand. Running : cnn_init.m-> main_image_deep.m-> well_cal.m.