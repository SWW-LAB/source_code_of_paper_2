function net = cnn_feedforward(net, x)  
    n = numel(net.conv_layer); % ����

    net.conv_layer{1}.a{1} = reshape(x(:,:,1,:), size(x,1),size(x,2),size(x,4)); % ����ĵ�һ��������룬���������������˶��ѵ��ͼ��  
    net.conv_layer{1}.a{2} = reshape(x(:,:,2,:), size(x,1),size(x,2),size(x,4));
    net.conv_layer{1}.a{3} = reshape(x(:,:,3,:), size(x,1),size(x,2),size(x,4));
    inputmaps = 3; % �����ֻ��һ������map��Ҳ����ԭʼ������ͼ��  
  
    for l_n = 2 : n   %  for each layer  
        if strcmp(net.conv_layer{l_n}.type, 'c') % �����  
            %  !!below can probably be handled by insane matrix operations  
            % ��ÿһ������map������˵������Ҫ��outputmaps����ͬ�ľ����ȥ���ͼ��  
            for j = 1 : net.conv_layer{l_n}.outputmaps   %  for each output map  
                %  create temp output map  
                % ����һ���ÿһ������map������������map�Ĵ�С����   
                % ������map�� - ����˵Ŀ� + 1��* ������map�� - ����˸� + 1��  
                % ��������Ĳ㣬��Ϊÿ�㶼������������map����Ӧ������������ÿ��map�ĵ���ά  
                % ���ԣ������z����ľ��Ǹò������е�����map�� 
                z = zeros([size(net.conv_layer{l_n - 1}.a{1},1) - net.conv_layer{l_n}.kernelsize + 1 size(net.conv_layer{l_n - 1}.a{1},2) - net.conv_layer{l_n}.kernelsize + 1 size(net.conv_layer{l_n - 1}.a{1},3)]);  
                for i = 1 : inputmaps   %  for each input map  
                    %  convolve with corresponding kernel and add to temp output map  
                    % ����һ���ÿһ������map��Ҳ������������map����ò�ľ���˽��о��  
                    % Ȼ�󽫶���һ������map�����н����������Ҳ����˵����ǰ���һ������map����  
                    % ��һ�־����ȥ�����һ�������е�����map��Ȼ����������map��Ӧλ�õľ��ֵ�ĺ�  
                    % ���⣬��Щ���Ļ���ʵ��Ӧ���У���������ȫ��������map���ӵģ��п���ֻ�����е�ĳ��������  
                    z = z + convn(net.conv_layer{l_n - 1}.a{i}, net.conv_layer{l_n}.k{i}{j}, 'valid');  %'same'�����ͼƬ��С���䣬'valid'������size(A)-size(B) + 1
                end  
                %  add bias, pass through nonlinearity  
                % ���϶�Ӧλ�õĻ�b��Ȼ�����ü�����������map��ÿ��λ�õļ���ֵ����Ϊ�ò��������map  
                net.conv_layer{l_n}.a{j} = activation_function(z + net.conv_layer{l_n}.b{j});  
            end  
            %  set number of input maps to this layers number of outputmaps  
            inputmaps = net.conv_layer{l_n}.outputmaps;  
        elseif strcmp(net.conv_layer{l_n}.type, 's') % �²�����  
            %  downsample  
            for j = 1 : inputmaps  
                %  !! replace with variable  
                if l_n == n
                    %���ڿռ�������ػ���
                    img_sz = size(net.conv_layer{l_n - 1}.a{j});
                    p_z = fix([img_sz(1)/net.conv_layer{l_n}.scale_1 img_sz(2)/net.conv_layer{l_n}.scale_2]); %ȡ����,�óػ��˴�С
                    z = convn(net.conv_layer{l_n - 1}.a{j}, ones(p_z) / (p_z(1)*p_z(2)), 'valid');   
                    net.conv_layer{l_n}.a{j} = z(1 : p_z(1) : p_z(1)*net.conv_layer{l_n}.scale_1, 1 : p_z(2) : p_z(2)*net.conv_layer{l_n}.scale_2, :); 
                else
                    % ��������Ҫ��scale=2��������ִ��mean pooling����ô���Ծ����СΪ2*2��ÿ��Ԫ�ض���1/4�ľ����  
                    z = convn(net.conv_layer{l_n - 1}.a{j}, ones(net.conv_layer{l_n}.scale) / (net.conv_layer{l_n}.scale^2), 'valid');   
                    % ��Ϊconvn������Ĭ�Ͼ������Ϊ1����pooling����������û���ص��ģ����Զ�������ľ�����  
                    % ����pooling�Ľ����Ҫ������õ��ľ���������scale=2Ϊ���������Ű�mean pooling��ֵ������  
                    net.conv_layer{l_n}.a{j} = z(1 : net.conv_layer{l_n}.scale : end, 1 : net.conv_layer{l_n}.scale : end, :);  
                end
            end  
        end  
    end  
  
    % �����һ��õ�������map����һ����������Ϊ������ȡ������������  
    net.fv = [];  
    for j = 1 : numel(net.conv_layer{n}.a) % ���һ�������map�ĸ���  
        sa = [size(net.conv_layer{n}.a{j},1),size(net.conv_layer{n}.a{j},2),size(net.conv_layer{n}.a{j},3)]; % ��j������map�Ĵ�С  
        % �����е�����map����һ��������������һά���Ƕ�Ӧ������������ÿ������һ�У�ÿ��Ϊ��Ӧ����������  
        net.fv = [net.fv; reshape(net.conv_layer{n}.a{j}, sa(1) * sa(2), sa(3))];  
    end  
    net.full_layer_in = net.fv;
    %  feedforward into output perceptrons  
    % ����������������ֵ��sigmoid(W*X + b)��ע����ͬʱ������batchsize�����������ֵ  
    for l_n = 1 : numel(net.full_layer)
        net.full_layer{l_n}.o = activation_function(net.full_layer{l_n}.w * net.full_layer_in + repmat(net.full_layer{l_n}.b, 1, size(net.full_layer_in, 2)));
        net.full_layer_in = net.full_layer{l_n}.o;
    end
  
end  
