function [ output_img ] = Dig_Img(img, x, y, f_long, f_wide, r)
%img:ͼ�� x,y���������ꣻf_long����ĳ���f_wide���?r�������б�Ƕ�
%�����ܣ���ͼ�������⻭��
in = size(img)-[2 2 0];
coordinate = [[],[]];%�涥�����
half_L=round(f_long/2);
half_W=round(f_wide/2);
Trans_L = round([-half_W*sin(r) half_W*cos(r)]);%ƽ������
L=zeros(half_L*2+1,2);%�������洢
for L_i = -half_L:half_L
    L(L_i+half_L+1,1)=round(L_i*cos(r));
    L(L_i+half_L+1,2)=round(L_i*sin(r));
end
coordinate(1,:) = [L(1,2)+y+Trans_L(2) L(1,1)+x+Trans_L(1)];
coordinate(2,:) = [L(half_L*2+1,2)+y+Trans_L(2) L(half_L*2+1,1)+x+Trans_L(1)];
coordinate(3,:) = [L(half_L*2+1,2)+y-Trans_L(2) L(half_L*2+1,1)+x-Trans_L(1)];
coordinate(4,:) = [L(1,2)+y-Trans_L(2) L(1,1)+x-Trans_L(1)];
data = coordinate;
if ((0.5<data(1,2)&&data(1,2)<in(1))&&(0.5<data(2,2)&&data(2,2)<in(1))&&(0.5<data(3,2)&&data(3,2)<in(1))&&(0.5<data(4,2)&&data(4,2)<in(1))&&(0.5<data(1,1)&&data(1,1)<in(2))&&(0.5<data(2,1)&&data(2,1)<in(2))&&(0.5<data(3,1)&&data(3,1)<in(2))&&(0.5<data(4,1)&&data(4,1)<in(2)))
    unit_1 = (data(2,1)-data(1,1))/f_long;
    unit_2 = (data(2,2)-data(1,2))/f_long;
    unit_11 = (data(4,1)-data(1,1))/f_wide;
    unit_22 = (data(4,2)-data(1,2))/f_wide;
    n1 = data(1,1);
    n2 = data(1,2);
    n11 = data(1,1);
    n22 = data(1,2);
    data_x1 = [[],[],[]];
    for xh = 1:f_long
        for yh = 1:f_wide
             data_x1(yh,xh,:) = img(round(n22),round(n11),:);
             n11 = n11 + unit_11;
             n22 = n22 + unit_22;
        end
        n1 = n1 + unit_1;
        n2 = n2 + unit_2;
        n11 = n1;
        n22 = n2;
    end   
    output_img = uint8(data_x1);
else
    output_img = [[],[]];
end

end
