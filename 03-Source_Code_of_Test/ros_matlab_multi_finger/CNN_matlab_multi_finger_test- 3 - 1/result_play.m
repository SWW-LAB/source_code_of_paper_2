%clear;
%clc;
result_Frame3 = Label_finger(11,:);
img2= draw_frame(img, result_Frame3(1), result_Frame3(2), result_Frame3(3),result_Frame3(4), result_Frame3(5));
figure;
imshow(img2);

img2= draw_frame(img, save_Frame1(1), save_Frame1(2), save_Frame1(3),save_Frame1(4), save_Frame1(5));
img2= draw_frame(img2, save_Frame2(1), save_Frame2(2), save_Frame2(3),save_Frame2(4), save_Frame2(5));
img2= draw_frame(img2, save_Frame3(1), save_Frame3(2), save_Frame3(3),save_Frame3(4), save_Frame3(5));
img2= draw_frame(img2, save_Frame4(1), save_Frame4(2), save_Frame4(3),save_Frame4(4), save_Frame4(5));
figure;
imshow(img2);
% value = size(save_Frame2,1);
% for i = 1:value
%     img2= draw_frame(img2, save_Frame2(i,1), save_Frame2(i,2), save_Frame2(i,3),save_Frame2(i,4), save_Frame2(i,5));
% end
% figure;
% imshow(img2);
%load result-122;
%img = imread('image1.png');%��ȡԭͼ��
% value = size(save_Frame,1);
% img_1=img;
% for i = 1:value
%     img_1= draw_frame(img_1, save_Frame(i,1), save_Frame(i,2), save_Frame(i,3),save_Frame(i,4), save_Frame(i,5));
% end
% figure;
% imshow(img_1);
% img2= draw_frame(img, result_Frame(1), result_Frame(2), result_Frame(3),result_Frame(4), result_Frame(5));
% figure;
% imshow(img2);
% img2= draw_frame(img, result_Frame1(1), result_Frame1(2), result_Frame1(3),result_Frame1(4), result_Frame1(5));
% figure;
% imshow(img2);
% img2= draw_frame(img, result_Frame2(1), result_Frame2(2), result_Frame2(3),result_Frame2(4), result_Frame2(5));
% figure;
% imshow(img2);
% img2= draw_frame(img, result_Frame3(1), result_Frame3(2), result_Frame3(3),result_Frame3(4), result_Frame3(5));
% figure;
% imshow(img2);
