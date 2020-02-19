function net = cnn_feedforward(net, x)  
    n = numel(net.conv_layer); % 层数

    net.conv_layer{1}.a{1} = reshape(x(:,:,1,:), size(x,1),size(x,2),size(x,4)); % 网络的第一层就是输入，但这里的输入包含了多个训练图像  
    net.conv_layer{1}.a{2} = reshape(x(:,:,2,:), size(x,1),size(x,2),size(x,4));
    net.conv_layer{1}.a{3} = reshape(x(:,:,3,:), size(x,1),size(x,2),size(x,4));
    inputmaps = 3; % 输入层只有一个特征map，也就是原始的输入图像  
  
    for l_n = 2 : n   %  for each layer  
        if strcmp(net.conv_layer{l_n}.type, 'c') % 卷积层  
            %  !!below can probably be handled by insane matrix operations  
            % 对每一个输入map，或者说我们需要用outputmaps个不同的卷积核去卷积图像  
            for j = 1 : net.conv_layer{l_n}.outputmaps   %  for each output map  
                %  create temp output map  
                % 对上一层的每一张特征map，卷积后的特征map的大小就是   
                % （输入map宽 - 卷积核的宽 + 1）* （输入map高 - 卷积核高 + 1）  
                % 对于这里的层，因为每层都包含多张特征map，对应的索引保存在每层map的第三维  
                % 所以，这里的z保存的就是该层中所有的特征map了 
                z = zeros([size(net.conv_layer{l_n - 1}.a{1},1) - net.conv_layer{l_n}.kernelsize + 1 size(net.conv_layer{l_n - 1}.a{1},2) - net.conv_layer{l_n}.kernelsize + 1 size(net.conv_layer{l_n - 1}.a{1},3)]);  
                for i = 1 : inputmaps   %  for each input map  
                    %  convolve with corresponding kernel and add to temp output map  
                    % 将上一层的每一个特征map（也就是这层的输入map）与该层的卷积核进行卷积  
                    % 然后将对上一层特征map的所有结果加起来。也就是说，当前层的一张特征map，是  
                    % 用一种卷积核去卷积上一层中所有的特征map，然后所有特征map对应位置的卷积值的和  
                    % 另外，有些论文或者实际应用中，并不是与全部的特征map链接的，有可能只与其中的某几个连接  
                    z = z + convn(net.conv_layer{l_n - 1}.a{i}, net.conv_layer{l_n}.k{i}{j}, 'valid');  %'same'卷积后图片大小不变，'valid'卷积结果size(A)-size(B) + 1
                end  
                %  add bias, pass through nonlinearity  
                % 加上对应位置的基b，然后再用激活函数算出特征map中每个位置的激活值，作为该层输出特征map  
                net.conv_layer{l_n}.a{j} = activation_function(z + net.conv_layer{l_n}.b{j});  
            end  
            %  set number of input maps to this layers number of outputmaps  
            inputmaps = net.conv_layer{l_n}.outputmaps;  
        elseif strcmp(net.conv_layer{l_n}.type, 's') % 下采样层  
            %  downsample  
            for j = 1 : inputmaps  
                %  !! replace with variable  
                if l_n == n
                    %基于空间金字塔池化层
                    img_sz = size(net.conv_layer{l_n - 1}.a{j});
                    p_z = fix([img_sz(1)/net.conv_layer{l_n}.scale_1 img_sz(2)/net.conv_layer{l_n}.scale_2]); %取整数,得池化核大小
                    z = convn(net.conv_layer{l_n - 1}.a{j}, ones(p_z) / (p_z(1)*p_z(2)), 'valid');   
                    net.conv_layer{l_n}.a{j} = z(1 : p_z(1) : p_z(1)*net.conv_layer{l_n}.scale_1, 1 : p_z(2) : p_z(2)*net.conv_layer{l_n}.scale_2, :); 
                else
                    % 例如我们要在scale=2的域上面执行mean pooling，那么可以卷积大小为2*2，每个元素都是1/4的卷积核  
                    z = convn(net.conv_layer{l_n - 1}.a{j}, ones(net.conv_layer{l_n}.scale) / (net.conv_layer{l_n}.scale^2), 'valid');   
                    % 因为convn函数的默认卷积步长为1，而pooling操作的域是没有重叠的，所以对于上面的卷积结果  
                    % 最终pooling的结果需要从上面得到的卷积结果中以scale=2为步长，跳着把mean pooling的值读出来  
                    net.conv_layer{l_n}.a{j} = z(1 : net.conv_layer{l_n}.scale : end, 1 : net.conv_layer{l_n}.scale : end, :);  
                end
            end  
        end  
    end  
  
    % 把最后一层得到的特征map拉成一条向量，作为最终提取到的特征向量  
    net.fv = [];  
    for j = 1 : numel(net.conv_layer{n}.a) % 最后一层的特征map的个数  
        sa = [size(net.conv_layer{n}.a{j},1),size(net.conv_layer{n}.a{j},2),size(net.conv_layer{n}.a{j},3)]; % 第j个特征map的大小  
        % 将所有的特征map拉成一条列向量。还有一维就是对应的样本索引。每个样本一列，每列为对应的特征向量  
        net.fv = [net.fv; reshape(net.conv_layer{n}.a{j}, sa(1) * sa(2), sa(3))];  
    end  
    net.full_layer_in = net.fv;
    %  feedforward into output perceptrons  
    % 计算网络的最终输出值。sigmoid(W*X + b)，注意是同时计算了batchsize个样本的输出值  
    for l_n = 1 : numel(net.full_layer)
        net.full_layer{l_n}.o = activation_function(net.full_layer{l_n}.w * net.full_layer_in + repmat(net.full_layer{l_n}.b, 1, size(net.full_layer_in, 2)));
        net.full_layer_in = net.full_layer{l_n}.o;
    end
  
end  
