function [ output_img ] = change_size( input_img, long, wide )
%long,wide:ͼ����Ҫ���õĳ��Ϳ�
    img_size = size(input_img);
    data = [[],[],[]];
    for i = 1:long
        for j = 1:wide
            x = round(j/wide*img_size(1));
            y = round(i/long*img_size(2));
            if x < 1
                x = 1;
            end
            if y < 1
                y = 1;
            end
            data(j,i,:) = input_img(x,y,:);
        end
    end
    output_img = uint8(data);
end

