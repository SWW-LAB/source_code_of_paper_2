load cnn_multi_finger
point_finger = [[],[]];
%这个应该是搜索接触点
[Frame1, Frame2 , Frame3, Frame4] = Fixed_Point_Finger( img, result_Frame,cnn_multi_finger );
%point_xyz求抓取点的平均位置
point_finger(1,:) = point_xyz(points_data_image,result_Frame); %抓取框中心

point_0 = point_finger(1,:);
point_finger(2,:) = points_data(Frame1(1),Frame1(2),:);
point_finger(3,:) = points_data(Frame2(1),Frame2(2),:);
point_finger(4,:) = points_data(Frame3(1),Frame3(2),:);
point_finger(5,:) = points_data(Frame4(1),Frame4(2),:);
flag = 0;
while 1

    if point_finger(2,3) > point_finger(1,3) + 0.1
       point_finger(2,:) = points_data(Frame1(1),Frame1(2)+5,:);
    else
       flag = flag +1;
    end
    if point_finger(3,3) > point_finger(1,3) + 0.1
       point_finger(3,:) = points_data(Frame2(1),Frame2(2)-5,:);
    else
       flag = flag +1;
   end
    if point_finger(4,3) > point_finger(1,3) + 0.1
       point_finger(4,:) = points_data(Frame3(1),Frame3(2)-5,:);
    else
       flag = flag +1;
    end
    if point_finger(5,3) > point_finger(1,3) + 0.1
       point_finger(5,:) = points_data(Frame4(1),Frame4(2)-5,:);
    else
       flag = flag +1;
    end
    
    if flag == 4
        break;
    else
        flag =0 ;
    end
end
% point_1 = point_xyz(points_data_image,result_Frame+[10 0 0 0 0 0]);
% point_2 = point_xyz(points_data_image,result_Frame+[0 10 0 0 0 0]);
% dif_1 = (point_1-point_0)/10;
% dif_2 = (point_2-point_0)/10;
% point_finger(2,:) = point_0 + dif_1*(Frame1(1)-result_Frame(1)) + dif_2*(Frame1(2)-result_Frame(2));
% point_finger(3,:) = point_0 + dif_1*(Frame2(1)-result_Frame(1)) + dif_2*(Frame2(2)-result_Frame(2));
% point_finger(4,:) = point_0 + dif_1*(Frame3(1)-result_Frame(1)) + dif_2*(Frame3(2)-result_Frame(2));
% point_finger(5,:) = point_0 + dif_1*(Frame4(1)-result_Frame(1)) + dif_2*(Frame4(2)-result_Frame(2));
% point_finger(2,:) = point_finger(2,:)+[0 0 0.080];
% point_finger(3,:) = point_finger(3,:)+[0 0 0.080];
% point_finger(4,:) = point_finger(4,:)+[0 0 0.080];
% point_finger(5,:) = point_finger(5,:)+[0 0 0.080];

 E1 =  c_to_s( wTh, point_finger(2,:),result_Frame(5),cos_xi,sin_xi);
 E2 =  c_to_s( wTh, point_finger(3,:),result_Frame(5),cos_xi,sin_xi);
 E3 =  c_to_s( wTh, point_finger(4,:),result_Frame(5),cos_xi,sin_xi);
 E4 =  c_to_s( wTh, point_finger(5,:),result_Frame(5),cos_xi,sin_xi);

img2= draw_frame(img, result_Frame(1), result_Frame(2), result_Frame(3),result_Frame(4), result_Frame(5));
if  ~isempty(Frame1)
    img2= draw_frame1(img2, Frame1(1), Frame1(2), Frame1(3),Frame1(4), Frame1(5));
end
if  ~isempty(Frame2)
    img2= draw_frame1(img2, Frame2(1), Frame2(2), Frame2(3),Frame2(4), Frame2(5));
end
if  ~isempty(Frame3)
    img2= draw_frame1(img2, Frame3(1), Frame3(2), Frame3(3),Frame3(4), Frame3(5));
end
if  ~isempty(Frame4)
    img2= draw_frame1(img2, Frame4(1), Frame4(2), Frame4(3),Frame4(4), Frame4(5));
end
%计算指尖接触点在rh_palm中的坐标

shadow_th = pTc * [point_finger(2,:)' ; 1];
shadow_ff = pTc*[point_finger(3,:)' ; 1];
shadow_mf = pTc*[point_finger(4,:)' ; 1];
shadow_rf = pTc*[point_finger(5,:)' ; 1];
shadow_fingers = [[],[]];
shadow_fingers(1,:) = shadow_th;
shadow_fingers(2,:) = shadow_ff;
shadow_fingers(3,:) = shadow_mf;
shadow_fingers(4,:) = shadow_rf;
save('/home/well/simulation_data3.0/test6/2/finger_points.mat', 'shadow_fingers')

figure;
imshow(img2);