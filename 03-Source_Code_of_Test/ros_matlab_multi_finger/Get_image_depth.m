function [ output_image , output_depth ] = Get_image_depth( )
%UNTITLED2 此处显示有关此函数的摘要
%   此处显示详细说明
sub_image =rossubscriber('/realsense_f200/rgb/image_rect_color','sensor_msgs/Image');
msg_image = receive(sub_image);
output_image = readImage(msg_image);

% sub_depth =rossubscriber('/realsense_f200/depth/image_raw','sensor_msgs/Image');
% msg_depth= receive(sub_depth);
%  output_depth= readImage(msg_depth);

sub_points =rossubscriber('/realsense_f200/depth_registered/points','sensor_msgs/PointCloud2');
msg_points= receive(sub_points);
output_depth=readXYZ(msg_points);

end

