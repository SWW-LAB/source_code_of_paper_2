function [ E ] = c_to_s( wTh, point_finger,result_Frame_r,cos_xi,sin_xi)
%UNTITLED3 此处显示有关此函数的摘要,相机坐标系下的点转换到手掌坐标系下
%   此处显示详细说明
AB=wTh;
camera2word = [ 0.9984    0.0508    0.0235    0.8675;
                              -0.0170   -0.1239    0.9922   -1.0755;
                               0.0533   -0.9910   -0.1228    0.5315;
                               0               0              0             1.0000];
                           
target_word2 = camera2word*[ point_finger(1); point_finger(2); point_finger(3);1]; %这个直接是shadow的手掌位置
angle = result_Frame_r-pi/2;%
R1 = [cos(angle)*cos_xi        sin_xi         sin(angle)*cos_xi;      %手掌跟着框旋转
         -cos(angle)*sin_xi        cos_xi         -sin(angle)*sin_xi;
          -sin(angle)                        0                   cos(angle)];
R2=quat2rotm([0 0.72885 -0.016046 0.68448]);%手横着与world位姿固定

FB = [R2*R1 target_word2(1:3)-[0.09;0.0;0.0];%修改shadow手的手掌误差，而不是直接修改UR5的末端位置误差
    0 0 0 1];

E = (AB)^(-1)*FB;

end

