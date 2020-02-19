clear;
clc
% rosshutdown;
% rosinit('192.168.1.30');
% pub_msg = rospublisher('/ros_msg','geometry_msgs/Pose');
% msg = rosmessage(pub_msg);
load cnn0;
load cnn1;
load cnn2;
load cnn_deep;
load cnn_multi_finger;
load data_003;
imshow(img);