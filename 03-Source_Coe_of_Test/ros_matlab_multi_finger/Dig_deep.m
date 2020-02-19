function [ output_img ] = Dig_deep(img, x, y, f_long, f_wide, r)
%img:图像 x,y框的中心坐标；f_long：框的长，f_wide：宽；r：框的倾斜角度
%函数功能：在图像上任意画框
data_x1 = [[],[]];
sin_r = sin(r);
cos_r = cos(r);
f_wide_j1 = x-sin_r*f_wide/2-cos_r*f_long/2;
f_wide_j2 = y+cos_r*f_wide/2-sin_r*f_long/2;
for j=1:f_wide
    f_wide_j1 = f_wide_j1 + sin_r;
    f_1 = f_wide_j1;
    f_wide_j2 = f_wide_j2 - cos_r;
    f_2 = f_wide_j2;
    for i=1:f_long
        f_1 = f_1 + cos_r;
        f_2 = f_2 + sin_r;
        data_x1(j,i) = img(round(f_1),round(f_2));
    end 
end
output_img = data_x1;
end