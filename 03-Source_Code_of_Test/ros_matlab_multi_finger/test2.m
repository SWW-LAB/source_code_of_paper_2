load cnn_multi_finger
Get_F =result_Frame;%ץȡ��ı��
    
    save_Frame1 = [[],[]];
    
    flag1 = 0;
    n_i=1;
   
    axis_1 = Get_F(1);
    axis_2 = Get_F(2);

    n=8/8;
    for i = Get_F(3)/2:-2:1  %���ѷ�Χ������߿�
        for j = 0:4:round(i*sin(pi/6)) 
            axis_1_1 = axis_1 - round(j*cos(Get_F(5)+pi/2) + i*sin(Get_F(5)+pi/2));  %������
            axis_2_1 = axis_2 - round(j*sin(Get_F(5)+pi/2) - i*cos(Get_F(5)+pi/2));
            img_f = Dig_Img (img,axis_1_1, axis_2_1, 24*n, 24*n,  0);
            if  ~isempty(img_f)
                cnn_multi_finger = cnn_feedforward(cnn_multi_finger, img_f);
                cnn1_result = cnn_multi_finger.full_layer{2}.o;
                if (cnn1_result>0)
                    save_Frame1(n_i,:)= [axis_1_1 axis_2_1 24*n 24*n 0 cnn1_result];
                    n_i=n_i+1;
                end
            end
            if j==0
                continue;
            end
            axis_1_1 = axis_1 - round(-j*cos(Get_F(5)+pi/2) + i*sin(Get_F(5)+pi/2));  %������
            axis_2_1 = axis_2 - round(-j*sin(Get_F(5)+pi/2) - i*cos(Get_F(5)+pi/2));
            img_f = Dig_Img (img,axis_1_1, axis_2_1, 24*n, 24*n,  0);
            if  ~isempty(img_f)
                cnn_multi_finger = cnn_feedforward(cnn_multi_finger, img_f);
                cnn1_result = cnn_multi_finger.full_layer{2}.o;
                if (cnn1_result>0)
                    save_Frame1(n_i,:) = [axis_1_1 axis_2_1 24*n 24*n 0 cnn1_result];
                    n_i=n_i+1;
                end
            end
        end
    end 
   value = size(save_Frame1,1);
   img1=img;
for i = 1:value
    img1= draw_frame(img1, save_Frame1(i,1), save_Frame1(i,2), save_Frame1(i,3),save_Frame1(i,4), save_Frame1(i,5));
end
figure;
imshow(img1);
    
    