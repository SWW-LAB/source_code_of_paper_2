img = imread('/home/well/0.jpg');
img = double(img);
ymax=255;ymin=173;  
xmax = max(max(img)); %���InImg�е����ֵ  
xmin = 120; %���InImg�е���Сֵ  
OutImg = (ymax-ymin)*(img-xmin)/(xmax-xmin) + ymin; %��һ�� 
OutImg = uint8(OutImg);
 imwrite(OutImg,'/home/well/16.jpg');