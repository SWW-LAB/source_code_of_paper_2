function send_msg( f1,f2,f3,f4)
%UNTITLED 此处显示有关此函数的摘要
%   此处显示详细说明
%{
pub_msg = rospublisher('/ros_msg','msg_custom/msg_float64');
pause(2);
msg = rosmessage(pub_msg);
msg.Num1 = f1;
msg.Num2 = f2;
msg.Num3 = f3;
msg.Num4 = f4;
send(pub_msg,msg);
pause(2);
%}
pub_msg = rospublisher('/ros_msg','geometry_msgs/Pose');
pause(2);
msg = rosmessage(pub_msg);
msg.Position.X =f1;
msg.Position.Y =f2;
msg.Position.Z =f3;
msg.Orientation.X =0;
msg.Orientation.Y = 1;
msg.Orientation.Z = 0;
msg.Orientation.W =f4;
send(pub_msg,msg);
pause(2);

end

