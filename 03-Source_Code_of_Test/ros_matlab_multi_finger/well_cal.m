%计算各个坐标系的转换关系
x1 = points_data_image(result_Frame(1),result_Frame(2),1);  %或�?直接调整物体的位置误�?reult_frame是结�?1是x,2是y,3\4是边框大�?5是角�?6是打�?
y1 = points_data_image(result_Frame(1),result_Frame(2),2);
z1 = points_data_image(result_Frame(1),result_Frame(2),3);

x2 = points_data_image(result_Frame(1)+15,result_Frame(2),1);%手掌再根据物体�?斜旋�?
y2 = points_data_image(result_Frame(1)+15,result_Frame(2),2);
z2 = points_data_image(result_Frame(1)+15,result_Frame(2),3);

deta_z =z1-z2;
deta_y = y2-y1;
deta_x = sqrt(deta_z^2+deta_y^2);
sin_xi = deta_z/deta_x;
cos_xi = deta_y/deta_x;
% sin_xi = 0;
% cos_xi =1;
% %再将坐标转换到世界坐标系中，成为UR5的末端执行器坐标（之后�?虑直接作为shadow手的坐标�?
%这个是gazebo中相机坐标系相对于graspit中world坐标系的转换
camera2word = [    -1   0  0    0;
                                  0    -1    0    0.2859;
                                0   0     1    -0.8632;
                                        0         0         0    1.0000];
                                    
  z1_p = 0.03; %抓取点到手掌的距离
% % target_word = camera2word*[x1;y1;z1;1]+[-0.154;0;0.015;0];%ur5的末端执行器位置而不是shadow手的位置
target_word = camera2word*[x1;y1;z1-z1_p;1]; %这个直接是shadow的手掌位�?
angle = result_Frame(5)-pi/2;%
R1 = [cos(angle)*cos_xi        sin_xi         sin(angle)*cos_xi;      %手掌跟着框旋�?,最终姿态相对于初始姿态(横着)
         -cos(angle)*sin_xi        cos_xi         -sin(angle)*sin_xi;
          -sin(angle)                        0                   cos(angle)];
%手掌横着相对于世界坐标系的旋转矩阵
R2 = [0 0 -1 ;
          1 0 0;
          0 -1 0];
 wTh = [R2*R1 target_word(1:3)-[0.00;0.0;0.00];%修改shadow手的手掌误差，�?不是直接修改UR5的末端位置误�?
    0 0 0 1];
wTgh = wTh*[0,  -1,   0,  0;
                                   0 ,  0,  -1,  0;
                                   1,   0,   0,  -0.03;
                                   0, 0, 0,1];  %graspit中手掌坐标系相对于其世界坐标系的转换矩阵
pose_wTgh = rotm2quat(wTgh(1:3,1:3));
save('/home/well/simulation_data3.0/test6/2/wTh.mat', 'wTgh')
save('/home/well/simulation_data3.0/test6/2/quat.mat','pose_wTgh')
% % wTh = [R2*R1 target_word(1:3)-[0.09;0.03;0.05];%修改shadow手的手掌误差，�?不是直接修改UR5的末端位置误�?
% %     0 0 0 1];
pTh = [1 0 0 0.02;
             0 1 0 0;
             0 0 1 0.12;
             0 0 0 1];%自定义的手掌中心到rh_palm的旋转矩阵,h也是设定的抓取框的中心
   %相机坐标系相对于rh_palm的转换矩阵
pTc = pTh*(wTh)^(-1)*camera2word;