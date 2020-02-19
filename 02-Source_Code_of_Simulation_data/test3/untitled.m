%得到手掌的一系列倾斜和旋转的位姿,保证手掌的世界坐标xy以及x轴在世界坐标系xy平面上的投影方向不变
pose = [-0.0542343936537, 0.454316432973,0.105399191172,0.882919146794];%手掌的四元素相对于世界坐标系
w_R_h = quat2rotm(pose);%手掌的旋转矩阵相对于世界坐标系
%手掌绕手掌坐标系x轴旋转,得到倾斜的位姿
%alpha = -pi/4; %旋转的角度
result = [];
i = 1;
for alpha = -pi/2:pi/10:pi/2
c = cos(alpha);
s = sin(alpha);
h_R_h1 = [1 0 0;
                   0  c  -s;
                   0  s  c;];%旋转后的坐标系关于原手掌坐标系的旋转矩阵
w_R_h1 = w_R_h * h_R_h1;

%手掌绕垂直于手掌坐标系x轴以及x轴在世界坐标系上的投影的单位向量旋转,得到旋转位姿
w_X_h  = w_R_h1(:,1); 
temp = [w_X_h(1:2);0];  %x轴在xy平面的投影
rotate_v= cross(temp,w_X_h);              %旋转轴,垂直垂直于上面的两个向量,这个向量要在h1坐标系下
rotate_v = (w_R_h1^(-1))*rotate_v;
rotate_v = rotate_v/norm(rotate_v); 
rv_x = rotate_v(1);
rv_y = rotate_v(2);
rv_z = rotate_v(3);
%theta = pi/4; 
for theta = -pi/2:pi/10:0
c1 = cos(theta);
s1 = sin(theta);
h1_R_h2 = [rv_x^2*(1-c1)+c1  rv_x*rv_y*(1-c1)-rv_z*s1  rv_x*rv_z*(1-c1)+rv_y*s1;
                    rv_x*rv_y*(1-c1)+rv_z*s1    rv_y^2*(1-c1)+c1    rv_y*rv_z*(1-c1)-rv_x*s1;
                    rv_x*rv_z*(1-c1)-rv_y*s1    rv_y*rv_z*(1-c1)+rv_x*s1  rv_z^2*(1-c1)+c1];
 
 w_R_h2 = w_R_h1*h1_R_h2;
 final_pose = rotm2quat(w_R_h2);
 result(i,:)=final_pose;
 i = i+1;
end
end