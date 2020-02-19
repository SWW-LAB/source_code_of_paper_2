function [ out_deep_img ] = Get_Deep_Img_xyz(points)

    deep_img = [ [], [], [] ];

%     for i = 1:540
%         for j = 1:960
%             if ~isnan(points((i-1)*960+j, 3))
%                 deep_img(i,j,:) =points((i-1)*960+j, :);
%             else
%                 deep_img(i,j,:) = [0 0 0];
%             end
%         end
%     end
%         out_deep_img = deep_img;
    for i = 1:480
        for j = 1:640
            if ~isnan(points((i-1)*640+j, 3))
                deep_img(i,j,:) =points((i-1)*640+j, :);
            else
                deep_img(i,j,:) = [0 0 0];
            end
        end
    end
        out_deep_img = deep_img;
end