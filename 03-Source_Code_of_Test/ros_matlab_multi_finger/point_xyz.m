function [ point ] = point_xyz( points, Frame)
%UNTITLED2 Summary of this function goes here
%   Detailed explanation goes here
    point0 = squeeze(points(Frame(1),Frame(2),:));
    point1 = squeeze(points(Frame(1)+1,Frame(2)+1,:));
    point2 = squeeze(points(Frame(1)+1,Frame(2)-1,:));
    point3 = squeeze(points(Frame(1)-1,Frame(2)+1,:));
    point4 = squeeze(points(Frame(1)-1,Frame(2)-1,:));
    point = ((point0+point1+point2+point3+point4)/5)';
end

