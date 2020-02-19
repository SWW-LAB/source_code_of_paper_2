
points_data = Get_Deep_Img_xyz(points);
points_data_image = Deal_points_Img1(points_data);

deepdata = Get_Deep_Img(msg_points);
deep_data_image = Deal_Deep_Img1(deepdata);
deep_0_1 = Normalize1(deep_data_image);%归一�?

r_long = 32;
r_wide = 16;
save_Frame = [[],[]];
save_data = [[],[],[],[]];
result = 0;
n_1 = 1;
n_2 = 0;
 
deep_size = size(deep_0_1);
img_size = size(img);

 tic
for multiple_i = 1.3:0.2:1.5
    multiple = multiple_i;
    img1 = change_size(img, img_size(2)/multiple, img_size(1)/multiple);
    deepdata1 = change_size_deep(deep_0_1,deep_size(2)/multiple, deep_size(1)/multiple);
    img_size1 = size(img1);
    img_judge = [[],[]];
    n=12;
    img_judge_i =1;
    for i_1 = round(245/multiple):n:(img_size1(1)-round(180/multiple)-n)
        for i_2 = round(380/multiple):n:(img_size1(2)-round(390/multiple)-n)
            img_f = img1(i_1:i_1+n-1,i_2:i_2+n-1,:);
            data = double(img_f)/255;
            cnn0 = cnn_feedforward(cnn0, data);
            cnn1_result = cnn0.full_layer{1}.o; 
            if cnn1_result >0.5
                 img_judge(img_judge_i,:)=[i_1+2 i_2+2];
                img_judge_i = img_judge_i + 1;
                img_judge(img_judge_i,:)=[i_1+2  i_2+6];
                img_judge_i = img_judge_i + 1;
                img_judge(img_judge_i,:)=[i_1+2 i_2+10];
                img_judge_i = img_judge_i + 1;
                img_judge(img_judge_i,:)=[i_1+6 i_2+2];
                img_judge_i = img_judge_i + 1;
                 img_judge(img_judge_i,:)=[i_1+6 i_2+6];
                img_judge_i = img_judge_i + 1;
                img_judge(img_judge_i,:)=[i_1+6 i_2+10];
                img_judge_i = img_judge_i + 1;
                img_judge(img_judge_i,:)=[i_1+10 i_2+2];
                img_judge_i = img_judge_i + 1;
                 img_judge(img_judge_i,:)=[i_1+10 i_2+6];
                img_judge_i = img_judge_i + 1;
                img_judge(img_judge_i,:)=[i_1+10 i_2+10];
                img_judge_i = img_judge_i + 1;
            end
        end  
    end
    for i = 1:img_judge_i-1
       
            for r = pi*2/8:pi/8:pi*6/8
                img_f = Dig_Img (img1,img_judge(i,1), img_judge(i,2), r_long, r_wide,  r);
                if  isempty(img_f)
                    continue;
                end
                img_f = img_f/255;
                cnn1 = cnn_feedforward(cnn1, img_f);
                cnn1_result = cnn1.full_layer{1}.o; 

                deep_f = Dig_deep (deepdata1,img_judge(i,1), img_judge(i,2), r_long, r_wide,  r);
                cnn_deep = cnn_feedforward_deep(cnn_deep,deep_f);
                cnn_deep_result = cnn_deep.full_layer{1}.o; 
               %cnn_deep_result = 1;
                if (cnn1_result>0.6&&cnn_deep_result>0.2)
                    save_Frame(n_1,:) = [round(img_judge(i,1)*multiple) round(img_judge(i,2)*multiple) round(r_long*multiple) round(r_wide*multiple) r cnn1_result];
                    save_data(:,:,:,n_1)  = img_f;
                    n_1 = n_1 + 1;
                end
                n_2 = n_2+1;
            end
            
    end
end
if  isempty(save_data)
    disp('NaN');
    return;
end

result1 = 0;
result2 = 0;
result3 = 0;
result_Frame1 = [0 0 0 0 0 0];
result_Frame2 = [0 0 0 0 0 0];
result_Frame3 = [0 0 0 0 0 0];
cnn2_n = size(save_data,4);

for i = 1:1:cnn2_n
    cnn2 = cnn_feedforward(cnn2, save_data(:,:,:,i));
    cnn2_result = cnn2.full_layer{2}.o;
    if result1 < cnn2_result
        if (result_Frame1(1)~=save_Frame(i,1))||(result_Frame1(2)~=save_Frame(i,2))
            result3 = result2;
            result_Frame3 = result_Frame2;
            result2 = result1;
            result_Frame2 = result_Frame1;
        end
        result1 = cnn2_result;
        result_Frame1 = save_Frame(i,:);
    elseif (result2 < cnn2_result)
        if(result_Frame1(1)~=save_Frame(i,1))||(result_Frame1(2)~=save_Frame(i,2))
            if result_Frame2(1)~=save_Frame(i,1)||(result_Frame2(2)~=save_Frame(i,2))
                result3 = result2;
                result_Frame3 = result_Frame2;
            end
            result2 = cnn2_result;
            result_Frame2 = save_Frame(i,:);
        end
    elseif (result3 < cnn2_result)
        if (result_Frame1(1)~=save_Frame(i,1))||(result_Frame1(2)~=save_Frame(i,2))
            if (result_Frame2(1)~=save_Frame(i,1))||(result_Frame2(2)~=save_Frame(i,2))
                result3 = cnn2_result;
                result_Frame3 = save_Frame(i,:);
            end
        end
    end
end
mean_coordinates=mean(save_Frame(:,1:2));
a1 = sum(abs(mean_coordinates-result_Frame1(1:2)));
a2 = sum(abs(mean_coordinates-result_Frame2(1:2)));
a3 = sum(abs(mean_coordinates-result_Frame3(1:2)));
if (a1<a2)&&(a1<a3)
    result_Frame =  result_Frame1;
elseif a2<a3
    result_Frame =  result_Frame2; 
else
    result_Frame =  result_Frame3;
end
toc;


x1 = points_data_image(result_Frame(1),result_Frame(2),1);  %或�?直接调整物体的位置误�?reult_frame是结�?1是x,2是y,3\4是边框大�?5是角�?6是打�?
y1 = points_data_image(result_Frame(1),result_Frame(2),2);
z1 = points_data_image(result_Frame(1),result_Frame(2),3);

x2 = points_data_image(result_Frame(1)+15,result_Frame(2),1);%手掌再根据物体�?斜旋�?
y2 = points_data_image(result_Frame(1)+15,result_Frame(2),2);
z2 = points_data_image(result_Frame(1)+15,result_Frame(2),3);

% deta_z =z1-z2;
% deta_y = y2-y1;
% deta_x = sqrt(deta_z^2+deta_y^2);
% sin_xi = deta_z/deta_x;
% cos_xi = deta_y/deta_x;
sin_xi = 0;
cos_xi =1;
%再将坐标转换到世界坐标系中，成为UR5的末端执行器坐标（之后�?虑直接作为shadow手的坐标�?
camera2word = [ 0.9984    0.0508    0.0235    0.8675;
                              -0.0170   -0.1239    0.9922   -1.0755;
                               0.0533   -0.9910   -0.1228    0.5315;
                               0               0              0             1.0000];
% target_word = camera2word*[x1;y1;z1;1]+[-0.154;0;0.015;0];%ur5的末端执行器位置而不是shadow手的位置
target_word = camera2word*[x1;y1;z1;1]; %这个直接是shadow的手掌位�?
angle = result_Frame(5)-pi/2+pi*1/16;%
R1 = [cos(angle)*cos_xi        sin_xi         sin(angle)*cos_xi;      %手掌跟着框旋�?
         -cos(angle)*sin_xi        cos_xi         -sin(angle)*sin_xi;
          -sin(angle)                        0                   cos(angle)];
R2=quat2rotm([0 0.72885 -0.016046 0.68448]);%手横�?��world位姿固定

wTh = [R2*R1 target_word(1:3)-[0.09;0.0;0.0];%修改shadow手的手掌误差，�?不是直接修改UR5的末端位置误�?
    0 0 0 1];
% wTh = [R2*R1 target_word(1:3)-[0.09;0.03;0.05];%修改shadow手的手掌误差，�?不是直接修改UR5的末端位置误�?
%     0 0 0 1];
eTh=[0             -0.6428    0.7660  0.154;   %ur末端到shadow手的旋转矩阵
          1.0000         0          0              0;
           0             0.7660    0.6428  -0.015;
           0                   0         0              1];
wTe = wTh*(eTh)^(-1);
my_orientation = rotm2quat(wTe(1:3,1:3));

% msg.Position.X = wTe(1,4);
% msg.Position.Y = wTe(2,4);
% msg.Position.Z = wTe(3,4);
% 
% msg.Orientation.X = my_orientation(2);
% msg.Orientation.Y = my_orientation(3);
% msg.Orientation.Z = my_orientation(4);
% msg.Orientation.W = my_orientation(1);
% send(pub_msg,msg);
% pause(2);


%save data_005.mat msg_points points points_data_image deep_data_image deep_0_1 img save_Frame result_Frame result_Frame1 result_Frame2 result_Frame3
