function [ output_img ] = Dig_deep(img, x, y, f_long, f_wide, r)
%img:ͼ�� x,y����������ꣻf_long����ĳ���f_wide����r�������б�Ƕ�
%�������ܣ���ͼ�������⻭��
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