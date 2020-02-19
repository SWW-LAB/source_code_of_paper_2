img2= draw_frame(img, result_Frame(1), result_Frame(2), result_Frame(3),result_Frame(4), result_Frame(5));
if  ~isempty(Frame1)
    img2= draw_frame1(img2, Frame1(1), Frame1(2), Frame1(3),Frame1(4), Frame1(5));
end
if  ~isempty(Frame2)
    img2= draw_frame1(img2, Frame2(1), Frame2(2), Frame2(3),Frame2(4), Frame2(5));
end
% if  ~isempty(Frame3)
%     img2= draw_frame1(img2, Frame3(1), Frame3(2), Frame3(3),Frame3(4), Frame3(5));
% end
% if  ~isempty(Frame4)
%     img2= draw_frame1(img2, Frame4(1), Frame4(2), Frame4(3),Frame4(4), Frame4(5));
% end
figure;
imshow(img2);
imwrite(img,'71.png')
imwrite(img3,'72.png')
imwrite(img2,'73.png')
imwrite(img1,'74.png')
