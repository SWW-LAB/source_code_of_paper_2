function OutImg = Normalize(InImg)  
    ymax=1;ymin=0;  
    xmax = max(max(InImg(310:450,210:450))); %���InImg�е����ֵ  
    xmin = min(min(InImg(310:450,210:450))); %���InImg�е���Сֵ  
%     xmax = max(max(InImg(130:280,210:400))); %���InImg�е����ֵ  
%     xmin = min(min(InImg(130:280,210:400))); %���InImg�е���Сֵ  
    OutImg = (ymax-ymin)*(InImg-xmin)/(xmax-xmin) + ymin; %��һ�� 
end
