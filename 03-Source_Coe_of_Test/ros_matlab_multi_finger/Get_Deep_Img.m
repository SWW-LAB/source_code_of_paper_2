function [ out_deep_img ] = Get_Deep_Img(msg_points)

    deep_img = [ [], [] ];
    points_z=readField(msg_points,'z');
%     for i = 1:540
%         for j = 1:960
%             if ~isnan(points_z((i-1)*960+j))
%                 deep_img(i,j) =points_z((i-1)*960+j);
%             else
%                 deep_img(i,j) = 0;
%             end
%         end
%     end

    for i = 1:480
        for j = 1:640
            if ~isnan(points_z((i-1)*640+j))
                deep_img(i,j) =points_z((i-1)*640+j);
            else
                deep_img(i,j) = 0;
            end
        end
    end
        out_deep_img = deep_img;
end
