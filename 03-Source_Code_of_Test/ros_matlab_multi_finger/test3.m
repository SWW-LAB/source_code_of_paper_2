figure
hold on
plot3(point_finger(1,1),point_finger(1,2),point_finger(1,3),'.')
plot3( point_finger(2,1),point_finger(2,2),point_finger(2,3),'*r')
plot3(point_finger(3,1),point_finger(3,2),point_finger(3,3),'*b')
plot3(point_finger(4,1),point_finger(4,2),point_finger(4,3),'*g')
plot3(point_finger(5,1),point_finger(5,2),point_finger(5,3),'*y')

axis([-0.5 0.5 -0.1 0.5 0 2])
view(0,-90);
xlabel('X');
ylabel('Y');
zlabel('Z');

point_ob = [[],[]];
ob_n = 1;
for i = 300:460
    for j = 340:600
        point_ob(ob_n,:) = points_data_image(i,j,:);
        ob_n=ob_n+1;
    end
end
figure
hold on
pcshow(point_ob)
pcshow(point_finger,'r')
axis([-0.4 0.4 0 0.4 0.8 1.6])
xlabel('X');
ylabel('Y');
zlabel('Z');
