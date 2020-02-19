function [ output_args ] = Deal_points_Img( input_args )
%Deal_Deep_Img �����ͼ���е�0ֵ��û�����ֵ���ø������ֵ����
%   �˴���ʾ��ϸ˵��
    data_size = size(input_args);
    n = 0;
    flag = 0;
    deep_img = [ [], [], [] ];
    for i = 1:data_size(1)
        for j = 1:data_size(2)
%             if (input_args(i,j,1)==0)&&(i>300)&&(i<480)&&(j>200)&&(j<450)
             if (input_args(i,j,1)==0)
                while flag==0
                    n = n + 1;
                    i_n_1 = i-n;
                    i_n_2 = i+n;
                    j_n_1 = j-n;
                    j_n_2 = j+n;
                    if i_n_1<1
                        i_n_1 = 1;
                    end
                    if j_n_1<1
                        j_n_1 = 1;
                    end
                    if i_n_2>data_size(1)
                        i_n_2 = data_size(1);
                    end
                    if j_n_2>data_size(2)
                        j_n_2 = data_size(2);
                    end
                    for i_n = i_n_1:i_n_2
                        for j_n = j_n_1:j_n_2
                            if input_args(i_n,j_n,1)~=0
                                flag = 1;
                                break;
                            end
                        end
                        if flag == 1
                            break;
                        end
                    end
                    if n>10
                        flag = 1;
                    end
                end
                if n<10
                    deep_img(i,j,:) = input_args(i_n,j_n,:);
                else
                    deep_img(i,j,:) = input_args(i,j,:);
                end
                flag = 0;
                n = 0;
            else
                deep_img(i,j,:) = input_args(i,j,:);
            end
         
        end
    end
	output_args = deep_img;
end
