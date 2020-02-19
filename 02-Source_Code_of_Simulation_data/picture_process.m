for index = 4:5
  img_path = ['/home/well/simulation_data2.0/test2/depth/' ,num2str(index),'.jpg'];
  save_path = ['/home/well/simulation_data2.0/test2/new_depth/' ,num2str(index),'.jpg'];
  img = imread(img_path);
  img_size = size(img);
%   temp = img(434,141);
temp = img(424,213);
  for i = 1:img_size(1)
      if i >424
          for j = 1:img_size(2)
              img(i,j) = temp;
          end        
      end
  end
  imwrite(img,save_path);
end