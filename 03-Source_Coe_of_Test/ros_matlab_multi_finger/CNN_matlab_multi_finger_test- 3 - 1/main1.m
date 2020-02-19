clear
clc

load cnn_multi_finger;

result_dir = 'C:\Users\Qunchao\Desktop\CNN¡ª¶àÖ¸ÁéÇÉÊÖ\CNN_matlab_multi_finger_test- 3 - 1\result';
source_dir = 'I:\Êý¾Ý´¦Àí\Get_Data\raw_data';

for iii=1:150
    img = sprintf('%s/image_data_%03d.png',source_dir,iii);
    Label = sprintf('%s/multi_fingered_label_%03d.mat',source_dir,iii);
    if ~exist(img,'file');
        continue;
    end
    img = imread(img);
    load(Label);
    save_Frame1 = [];
    save_Frame2 = [];
    save_Frame3 = [];
    save_Frame4 = [];
    flag1 = 0;
    flag2 = 0;
    flag3 = 0;
    flag4 = 0;

    result = 0;
    n_1 = 1;
    

    Get_F = Label_finger(11,:);%×¥È¡¿òµÄ±ê¼Ç
    axis_1 = Get_F(1);
    axis_2 = Get_F(2);
    n = round(Get_F(3)/100);
    img_size = size(img);
    for i = Get_F(3)/2:-5:1  %ÊÕËÑ·¶Î§²»³¬¹ý±ß¿ò
        for j = 0:4:round(i*sin(pi/6)) 
            axis_1_1 = axis_1 - round(j*cos(Get_F(5)+pi/2) + i*sin(Get_F(5)+pi/2));  %×ó±ß×ø±ê
            axis_2_1 = axis_2 - round(j*sin(Get_F(5)+pi/2) - i*cos(Get_F(5)+pi/2));
            img_f = Dig_Img (img,axis_1_1, axis_2_1, 24*n, 24*n,  0);
            if  ~isempty(img_f)
                cnn_multi_finger = cnn_feedforward(cnn_multi_finger, img_f);
                cnn1_result = cnn_multi_finger.full_layer{2}.o;
                if (cnn1_result>0.95)
                    save_Frame1= [axis_1_1 axis_2_1 24*n 24*n 0 cnn1_result];
                    flag1=flag1+1;
                    break; 
                end
            end
            if j==0
                continue;
            end
            
            axis_1_1 = axis_1 - round(-j*cos(Get_F(5)+pi/2) + i*sin(Get_F(5)+pi/2));  %×ó±ß×ø±ê
            axis_2_1 = axis_2 - round(-j*sin(Get_F(5)+pi/2) - i*cos(Get_F(5)+pi/2));
            img_f = Dig_Img (img,axis_1_1, axis_2_1, 24*n, 24*n,  0);
            if  ~isempty(img_f)
                cnn_multi_finger = cnn_feedforward(cnn_multi_finger, img_f);
                cnn1_result = cnn_multi_finger.full_layer{2}.o;
                if (cnn1_result>0.95)
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
    
    for i =  Get_F(3)/2:-5:1  %ÊÕËÑ·¶Î§²»³¬¹ý±ß¿ò
        for j = 0:4:round(i*sin(pi/6)) 
            axis_1_1 = axis_1 - round(j*cos(Get_F(5)-pi/6) + i*sin(Get_F(5)-pi/6));  %×ó±ß×ø±ê
            axis_2_1 = axis_2 - round(j*sin(Get_F(5)-pi/6) - i*cos(Get_F(5)-pi/6));
            img_f = Dig_Img (img,axis_1_1, axis_2_1, 24*n, 24*n,  0);
            if  ~isempty(img_f)
                cnn_multi_finger = cnn_feedforward(cnn_multi_finger, img_f);
                cnn1_result = cnn_multi_finger.full_layer{2}.o;
                if (cnn1_result>0.95)
                    save_Frame2= [axis_1_1 axis_2_1 24*n 24*n 0 cnn1_result];
                    flag2=flag2+1;
                    break; 
                end
            end
            if j==0
                continue;
            end
            
            axis_1_1 = axis_1 - round(-j*cos(Get_F(5)-pi/6) + i*sin(Get_F(5)-pi/6));  %×ó±ß×ø±ê
            axis_2_1 = axis_2 - round(-j*sin(Get_F(5)-pi/6) - i*cos(Get_F(5)-pi/6));
            img_f = Dig_Img (img,axis_1_1, axis_2_1, 24*n, 24*n,  0);
            if  ~isempty(img_f)
                cnn_multi_finger = cnn_feedforward(cnn_multi_finger, img_f);
                cnn1_result = cnn_multi_finger.full_layer{2}.o;
                if (cnn1_result>0.95)
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
    
    for i =  Get_F(3)/2:-5:1  %ÊÕËÑ·¶Î§²»³¬¹ý±ß¿ò
        for j = 0:4:round(i*sin(pi/6)) 
            axis_1_1 = axis_1 - round(j*cos(Get_F(5)-pi/2) + i*sin(Get_F(5)-pi/2));  %×ó±ß×ø±ê
            axis_2_1 = axis_2 - round(j*sin(Get_F(5)-pi/2) - i*cos(Get_F(5)-pi/2));
            img_f = Dig_Img (img,axis_1_1, axis_2_1, 24*n, 24*n,  0);
            if  ~isempty(img_f)
                cnn_multi_finger = cnn_feedforward(cnn_multi_finger, img_f);
                cnn1_result = cnn_multi_finger.full_layer{2}.o;
                if (cnn1_result>0.95)
                    save_Frame3= [axis_1_1 axis_2_1 24*n 24*n 0 cnn1_result];
                    flag3=flag3+1;
                    break; 
                end
            end
            if j==0
                continue;
            end
            
            axis_1_1 = axis_1 - round(-j*cos(Get_F(5)-pi/2) + i*sin(Get_F(5)-pi/2));  %×ó±ß×ø±ê
            axis_2_1 = axis_2 - round(-j*sin(Get_F(5)-pi/2) - i*cos(Get_F(5)-pi/2));
            img_f = Dig_Img (img,axis_1_1, axis_2_1, 24*n, 24*n,  0);
            if  ~isempty(img_f)
                cnn_multi_finger = cnn_feedforward(cnn_multi_finger, img_f);
                cnn1_result = cnn_multi_finger.full_layer{2}.o;
                if (cnn1_result>0.95)
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
    
    for i =  Get_F(3)/2:-5:1  %ÊÕËÑ·¶Î§²»³¬¹ý±ß¿ò
        for j = 0:4:round(i*sin(pi/6)) 
            axis_1_1 = axis_1 - round(j*cos(Get_F(5)-pi*5/6) + i*sin(Get_F(5)-pi*5/6));  %×ó±ß×ø±ê
            axis_2_1 = axis_2 - round(j*sin(Get_F(5)-pi*5/6) - i*cos(Get_F(5)-pi*5/6));
            img_f = Dig_Img (img,axis_1_1, axis_2_1, 24*n, 24*n,  0);
            if  ~isempty(img_f)
                cnn_multi_finger = cnn_feedforward(cnn_multi_finger, img_f);
                cnn1_result = cnn_multi_finger.full_layer{2}.o;
                if (cnn1_result>0.95)
                    save_Frame4= [axis_1_1 axis_2_1 24*n 24*n 0 cnn1_result];
                    flag4=flag4+1;
                    break; 
                end
            end
            if j==0
                continue;
            end
            
            axis_1_1 = axis_1 - round(-j*cos(Get_F(5)-pi*5/6) + i*sin(Get_F(5)-pi*5/6));  %×ó±ß×ø±ê
            axis_2_1 = axis_2 - round(-j*sin(Get_F(5)-pi*5/6) - i*cos(Get_F(5)-pi*5/6));
            img_f = Dig_Img (img,axis_1_1, axis_2_1, 24*n, 24*n,  0);
            if  ~isempty(img_f)
                cnn_multi_finger = cnn_feedforward(cnn_multi_finger, img_f);
                cnn1_result = cnn_multi_finger.full_layer{2}.o;
                if (cnn1_result>0.95)
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

    img2= draw_frame(img,  Label_finger(11,1),  Label_finger(11,2),  Label_finger(11,3), Label_finger(11,4),  Label_finger(11,5));
    if  ~isempty(save_Frame1)
        img2= draw_frame(img2, save_Frame1(1), save_Frame1(2), save_Frame1(3),save_Frame1(4), save_Frame1(5));
    end
    if  ~isempty(save_Frame2)
        img2= draw_frame(img2, save_Frame2(1), save_Frame2(2), save_Frame2(3),save_Frame2(4), save_Frame2(5));
    end
    if  ~isempty(save_Frame3)
        img2= draw_frame(img2, save_Frame3(1), save_Frame3(2), save_Frame3(3),save_Frame3(4), save_Frame3(5));
    end
    if  ~isempty(save_Frame4)
        img2= draw_frame(img2, save_Frame4(1), save_Frame4(2), save_Frame4(3),save_Frame4(4), save_Frame4(5));
    end
    
    mingzhi = sprintf('%s/%04d.png',result_dir,iii);
    imwrite(img2,mingzhi);
end

