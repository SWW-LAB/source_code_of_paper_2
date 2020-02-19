%clear;
%clc;

%load result-122;
%img = imread('image1.png');%��ȡԭͼ��
value = size(save_Frame,1);

img1=img;
for i = 1:value
    img1= draw_frame(img1, save_Frame(i,1), save_Frame(i,2), save_Frame(i,3),save_Frame(i,4), save_Frame(i,5));
end
figure;
imshow(img1);
img3= draw_frame(img, result_Frame(1), result_Frame(2), result_Frame(3),result_Frame(4), result_Frame(5));
 figure;
 imshow(img3);
 
% img2= draw_frame(img, result_Frame1(1), result_Frame1(2), result_Frame1(3),result_Frame1(4), result_Frame1(5));
% figure;
% imshow(img2);
% img2= draw_frame(img, result_Frame2(1), result_Frame2(2), result_Frame2(3),result_Frame2(4), result_Frame2(5));
% figure;
% imshow(img2);
% img2= draw_frame(img, result_Frame3(1), result_Frame3(2), result_Frame3(3),result_Frame3(4), result_Frame3(5));
% figure;
% imshow(img2);

