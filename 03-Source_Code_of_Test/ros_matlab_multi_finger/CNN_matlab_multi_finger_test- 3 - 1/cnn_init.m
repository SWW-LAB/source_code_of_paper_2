clear;
clc
load cnn0;
load cnn1;
load cnn2;
pub_msg = rospublisher('/ros_msg','geometry_msgs/Pose');
msg = rosmessage(pub_msg);
sub_points = rossubscriber('/realsense_f200/depth_registered/points','sensor_msgs/PointCloud2');
msg_points= receive(sub_points);
points=readXYZ(msg_points);
disp('get points');
sub_image = rossubscriber('/realsense_f200/rgb/image_rect_color','sensor_msgs/Image');