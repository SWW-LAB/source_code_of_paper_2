function OutImg = Normalize1(InImg)  
    ymax=1;ymin=0;  
    xmax = max(max(InImg(235:365,355:565))); %���InImg�е����ֵ  
    xmin = min(min(InImg(235:365,355:565))); %���InImg�е���Сֵ  
    OutImg = (ymax-ymin)*(InImg-xmin)/(xmax-xmin) + ymin; %��һ�� 
end
