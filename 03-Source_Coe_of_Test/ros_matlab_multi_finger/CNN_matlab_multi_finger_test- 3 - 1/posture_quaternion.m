function [ quaternion ] = posture_quaternion( points,point,result_Frame,img_size_2 )
%UNTITLED3 Summary of this function goes here
%   Detailed explanation goes here
    a=(round(result_Frame(1)-result_Frame(3)*cos(result_Frame(5))/6))*img_size_2 + round(result_Frame(2)-result_Frame(4)*sin(result_Frame(5)/2));
    point_x = piont_xyz(points,a,img_size_2);
    x = point_x- point;
    b=(round(result_Frame(1)-result_Frame(3)*cos(result_Frame(5)+pi/2)/6))*img_size_2 + round(result_Frame(2)-result_Frame(4)*sin(result_Frame(5)+pi/2)/2);
    point_y = piont_xyz(points,b,img_size_2);
    y = point_y- point;
    if x*y' ~= 0
        x(2) = -(x(1)*y(1)+x(3)*y(3))/y(2);
    end
    z = [0 0 0];
    z(3) = -point(3);
    z(1) = (x(2)*y(3)*z(3)-y(2)*x(3)*z(3))/(y(2)*x(1)-x(2)*y(1));
    z(2) = (x(1)*y(3)*z(3)-y(1)*x(3)*z(3))/(y(1)*x(2)-y(2)*x(1));
    proportion_x = sqrt(1/(x*x'));
    x = proportion_x*x;
    proportion_y = sqrt(1/(y*y'));
    y = proportion_y*y;
    proportion_z = sqrt(1/(z*z'));
    z = proportion_z*z;
    %旋转矩阵转换为四元数
    tr = x(1)+y(2)+z(3);
    if tr>0
        s = sqrt(tr+1)*2;
        q_w = s/4;
        q_x = (y(3)-z(2))/s;
        q_y = (z(1)-x(3))/s;
        q_z = (x(2)-y(1))/s;
    elseif (x(1)>y(2))&&(x(1)>z(3))
        s = sqrt(1+x(1)-y(2)-z(3))*2;
        q_w = (y(3)-z(2))/s;
        q_x = s/4;
        q_y = (x(2)+y(1))/s;
        q_z = (z(1)+x(3))/s;
    elseif y(2)>z(3)
        s = sqrt(1+y(2)-x(1)-z(3))*2;
        q_w = (x(2)+y(1))/s;
        q_x = (x(2)+y(1))/s;
        q_y = s/4;
        q_z = (y(3)+z(2))/s;
    else
        s = sqrt(1+z(3)-y(2)-x(1))*2;
        q_w = (x(2)-y(1))/s;
        q_x = (z(1)+x(3))/s;
        q_y = (y(3)+z(2))/s;
        q_z = s/4;
    end
    quaternion = [q_x q_y q_z q_w];
end

