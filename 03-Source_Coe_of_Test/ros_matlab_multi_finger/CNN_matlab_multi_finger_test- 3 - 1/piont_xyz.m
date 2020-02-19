function [ point ] = piont_xyz( points, p_p, img_size_2 )
%UNTITLED2 Summary of this function goes here
%   Detailed explanation goes here
    p_p_0 = 0;
    p_p_n = 0;
    n = 1;
    point = [0 0 0];
    if ~isnan(points(p_p,1))   
        point = point + points(p_p,:);
        p_p_0 = 1;
    end
    while p_p_n==0
        if ~isnan(points(p_p+n,1))   
            point = point + points(p_p+n,:);
            p_p_n = p_p_n+1;
        end
        if ~isnan(points(p_p-n,1))    
            point = point + points(p_p-n,:);
            p_p_n = p_p_n+1;
        end
        if ~isnan(points(p_p+img_size_2*n,1))    
            point = point + points(p_p+img_size_2*n,:);
            p_p_n = p_p_n+1;
        end
        if ~isnan(points(p_p-img_size_2*n,1))   
            point = point + points(p_p-img_size_2*n,:);
            p_p_n = p_p_n+1;
        end
        n = n + 1;
    end
    point = point/(p_p_n+p_p_0);
end

