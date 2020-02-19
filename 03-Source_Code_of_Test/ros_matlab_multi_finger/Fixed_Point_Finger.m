function [ save_Frame1, save_Frame2 , save_Frame3, save_Frame4] = Fixed_Point_Finger( input_img, input_label,cnn_multi_finger)
%UNTITLED2 此处显示有关此函数的摘要
%   此处显示详细说明
    img = input_img;
    Get_F = input_label;%ץȡ��ı��
    
    save_Frame1 = [];
    save_Frame2 = [];
    save_Frame3 = [];
    save_Frame4 = [];
    flag1 = 0;
    flag2 = 0;
    flag3 = 0;
    flag4 = 0;
    r0=pi*8/8;
    r=pi*0/8;
    axis_1 = Get_F(1);
    axis_2 = Get_F(2);
    %n = round(Get_F(3)/100);
    n=5/8;
    for i = Get_F(3)/2:-2:1  %���ѷ�Χ������߿�
        for j = 0:4:round(i*sin(pi/6)) 
            axis_1_1 = axis_1-10 - round(j*cos(Get_F(5)+pi/2) + i*sin(Get_F(5)+pi/2));  %������
            axis_2_1 = axis_2 - round(j*sin(Get_F(5)+pi/2) - i*cos(Get_F(5)+pi/2));
            img_f = Dig_Img (img,axis_1_1, axis_2_1, 24*n, 24*n,  r0);
            if  ~isempty(img_f)
                cnn_multi_finger = cnn_feedforward(cnn_multi_finger, img_f);
                cnn1_result = cnn_multi_finger.full_layer{2}.o;
                if (cnn1_result>0.8)
                    save_Frame1= [axis_1_1 axis_2_1 24*n 24*n 0 cnn1_result];
                    flag1=flag1+1;
                    break; 
                end
            end
            if j==0
                continue;
            end
            
            axis_1_1 = axis_1 - round(-j*cos(Get_F(5)+pi/2) + i*sin(Get_F(5)+pi/2));  %������
            axis_2_1 = axis_2 - round(-j*sin(Get_F(5)+pi/2) - i*cos(Get_F(5)+pi/2));
            img_f = Dig_Img (img,axis_1_1, axis_2_1, 24*n, 24*n,  r0);
            if  ~isempty(img_f)
                cnn_multi_finger = cnn_feedforward(cnn_multi_finger, img_f);
                cnn1_result = cnn_multi_finger.full_layer{2}.o;
                if (cnn1_result>0.8)
                    save_Frame1 = [axis_1_1 axis_2_1 24*n 24*n 0 cnn1_result];
                    flag1=flag1+1;
                    break;
                end
            end
        end
        if flag1 > 0
            break;
        end
    end 
    
    for i =  Get_F(3)/2:-2:1  %���ѷ�Χ������߿�
        for j = 0:4:round(i*sin(pi/12)) 
            axis_1_1 = axis_1 - round(j*cos(Get_F(5)-pi/3) + i*sin(Get_F(5)-pi/3));  %������
            axis_2_1 = axis_2 - round(j*sin(Get_F(5)-pi/3) - i*cos(Get_F(5)-pi/3));
            img_f = Dig_Img (img,axis_1_1, axis_2_1, 24*n, 24*n,  r);
            if  ~isempty(img_f)
                cnn_multi_finger = cnn_feedforward(cnn_multi_finger, img_f);
                cnn1_result = cnn_multi_finger.full_layer{2}.o;
                if (cnn1_result>0.9)
                    save_Frame2= [axis_1_1 axis_2_1 24*n 24*n 0 cnn1_result];
                    flag2=flag2+1;
                    break; 
                end
            end
            if j==0
                continue;
            end
            
            axis_1_1 = axis_1 - round(-j*cos(Get_F(5)-pi/3) + i*sin(Get_F(5)-pi/3));  %������
            axis_2_1 = axis_2 - round(-j*sin(Get_F(5)-pi/3) - i*cos(Get_F(5)-pi/3));
            img_f = Dig_Img (img,axis_1_1, axis_2_1, 24*n, 24*n,  r);
            if  ~isempty(img_f)
                cnn_multi_finger = cnn_feedforward(cnn_multi_finger, img_f);
                cnn1_result = cnn_multi_finger.full_layer{2}.o;
                if (cnn1_result>0.9)
                    save_Frame2 = [axis_1_1 axis_2_1 24*n 24*n 0 cnn1_result];
                    flag2=flag2+1;
                    break;
                end
            end
        end
        if flag2 > 0
            break;
        end
    end 
    
    for i =  Get_F(3)/2:-2:1  %���ѷ�Χ������߿�
        for j = 0:4:round(i*sin(pi/12)) 
            axis_1_1 = axis_1 - round(j*cos(Get_F(5)-pi/2) + i*sin(Get_F(5)-pi/2));  %������
            axis_2_1 = axis_2 - round(j*sin(Get_F(5)-pi/2) - i*cos(Get_F(5)-pi/2));
            img_f = Dig_Img (img,axis_1_1, axis_2_1, 24*n, 24*n,  r);
            if  ~isempty(img_f)
                cnn_multi_finger = cnn_feedforward(cnn_multi_finger, img_f);
                cnn1_result = cnn_multi_finger.full_layer{2}.o;
                if (cnn1_result>0.9)
                    save_Frame3= [axis_1_1 axis_2_1 24*n 24*n 0 cnn1_result];
                    flag3=flag3+1;
                    break; 
                end
            end
            if j==0
                continue;
            end
            
            axis_1_1 = axis_1 - round(-j*cos(Get_F(5)-pi/2) + i*sin(Get_F(5)-pi/2));  %������
            axis_2_1 = axis_2 - round(-j*sin(Get_F(5)-pi/2) - i*cos(Get_F(5)-pi/2));
            img_f = Dig_Img (img,axis_1_1, axis_2_1, 24*n, 24*n,  r);
            if  ~isempty(img_f)
                cnn_multi_finger = cnn_feedforward(cnn_multi_finger, img_f);
                cnn1_result = cnn_multi_finger.full_layer{2}.o;
                if (cnn1_result>0.9)
                    save_Frame3 = [axis_1_1 axis_2_1 24*n 24*n 0 cnn1_result];
                    flag3=flag3+1;
                    break;
                end
            end
        end
        if flag3 > 0
            break;
        end
    end  
    
    for i =  Get_F(3)/2:-2:1  %���ѷ�Χ������߿�
        for j = 0:4:round(i*sin(pi/12)) 
            axis_1_1 = axis_1 - round(j*cos(Get_F(5)-pi*2/3) + i*sin(Get_F(5)-pi*4/6));  %������
            axis_2_1 = axis_2 - round(j*sin(Get_F(5)-pi*4/6) - i*cos(Get_F(5)-pi*4/6));
            img_f = Dig_Img (img,axis_1_1, axis_2_1, 24*n, 24*n,  r);
            if  ~isempty(img_f)
                cnn_multi_finger = cnn_feedforward(cnn_multi_finger, img_f);
                cnn1_result = cnn_multi_finger.full_layer{2}.o;
                if (cnn1_result>0.9)
                    save_Frame4= [axis_1_1 axis_2_1 24*n 24*n 0 cnn1_result];
                    flag4=flag4+1;
                    break; 
                end
            end
            if j==0
                continue;
            end
            
            axis_1_1 = axis_1 - round(-j*cos(Get_F(5)-pi*4/6) + i*sin(Get_F(5)-pi*4/6));  %������
            axis_2_1 = axis_2 - round(-j*sin(Get_F(5)-pi*4/6) - i*cos(Get_F(5)-pi*4/6));
            img_f = Dig_Img (img,axis_1_1, axis_2_1, 24*n, 24*n, r);
            if  ~isempty(img_f)
                cnn_multi_finger = cnn_feedforward(cnn_multi_finger, img_f);
                cnn1_result = cnn_multi_finger.full_layer{2}.o;
                if (cnn1_result>0.9)
                    save_Frame4 = [axis_1_1 axis_2_1 24*n 24*n 0 cnn1_result];
                    flag4=flag4+1;
                    break;
                end
            end
        end
        if flag4 > 0
            break;
        end
    end   

end

