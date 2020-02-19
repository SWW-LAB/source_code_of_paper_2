function net = cnn_setup_deep(net, x, y)  
    inputmaps = 1;  %该层的输入图片数）
    full_n = numel(net.full_layer); %全连接层层数 
    mapsize = size(squeeze(x(:, :, 1)));  %x(:, :, 1,1)表示一张（手写字符）图片:结果是图片大小：mapsize=[28 28]
  
    % 下面通过传入net这个结构体来逐层构建CNN网络  
    % n = numel(A)返回数组A中元素个数   
    for layer_n = 1 : numel(net.conv_layer)   
        if strcmp(net.conv_layer{layer_n}.type, 'c') % 如果这层是 卷积层 
            
            mapsize = mapsize - net.conv_layer{layer_n}.kernelsize + 1; %卷积后的图片大小
            
            fan_out = net.conv_layer{layer_n}.outputmaps * net.conv_layer{layer_n}.kernelsize ^ 2;  %该层权值w数目
            for j = 1 : net.conv_layer{layer_n}.outputmaps  %  output map  
                % fan_out保存的是对于上一层的一张特征map，我在这一层需要对这一张特征map提取outputmaps种特征，  
                % 提取每种特征用到的卷积核不同，所以fan_out保存的是这一层输出新的特征需要学习的参数个数  
                % 而，fan_in保存的是，我在这一层，要连接到上一层中所有的特征map，然后用fan_out保存的提取特征  
                % 的权值来提取他们的特征。也即是对于每一个当前层特征图，有多少个参数链到前层  
                fan_in = inputmaps * net.conv_layer{layer_n}.kernelsize ^ 2;  
                for i = 1 : inputmaps  %  input map  
                    % 随机初始化权值，也就是共有outputmaps个卷积核，对上层的每个特征map，都需要用这么多个卷积核  
                    % 去卷积提取特征。  
                    % rand(n)是产生n×n的 0-1之间均匀取值的数值的矩阵，再减去0.5就相当于产生-0.5到0.5之间的随机数  
                    % 再 *2 就放大到 [-1, 1]。然后再乘以后面那一数，why？  
                    % 反正就是将卷积核每个元素初始化为[-sqrt(6 / (fan_in + fan_out)), sqrt(6 / (fan_in + fan_out))]  
                    % 之间的随机数。因为这里是权值共享的，也就是对于一张特征map，所有感受野位置的卷积核都是一样的  
                    % 所以只需要保存的是 inputmaps * outputmaps 个卷积核。  
                    net.conv_layer{layer_n}.k{i}{j} = (rand(net.conv_layer{layer_n}.kernelsize) - 0.5) * 2 * sqrt(6 / (fan_in + fan_out));  
                end  
                net.conv_layer{layer_n}.b{j} = 0; % 将偏置初始化为0  
            end  
            % 只有在卷积层的时候才会改变特征map的个数，pooling的时候不会改变个数。这层输出的特征map个数就是  
            % 输入到下一层的特征map个数  
            inputmaps = net.conv_layer{layer_n}.outputmaps;   
        end
        if strcmp(net.conv_layer{layer_n}.type, 's') % 如果这层是 子采样层  （池化层）
            if layer_n == numel(net.conv_layer)
                mapsize = floor([net.conv_layer{layer_n}.scale_1 net.conv_layer{layer_n}.scale_2]);%基于空间金字塔池化层图片大小
            else
                mapsize = floor(mapsize / net.conv_layer{layer_n}.scale); %pooling后图像大小 
            end
            for j = 1 : inputmaps % inputmap就是上一层有多少张特征图 （池化层与上一层的卷积层的神经元一样多）
                net.conv_layer{layer_n}.b{j} = 0; % 将偏置初始化为0  
            end  
        end  
    end  
      
    %卷积层后的第一个全连接层的输入大小
    fvnum = prod(mapsize) * inputmaps;  %每个神经元的连接数目，prod(mapsize)的输出是=map的行*map的列
    %全连接的参数设置
    output_num = size(y, 1);  %输出神经元个数.
    
    net.full_layer{full_n}.neurons = output_num;
    
    for layer_n = 1 :full_n
        
        net.full_layer{layer_n}.w = (rand(net.full_layer{layer_n}.neurons, fvnum) - 0.5) * 2 * sqrt(6 / (net.full_layer{layer_n}.neurons + fvnum)); %全连接中的权值初始化
        
        net.full_layer{layer_n}.b = zeros(net.full_layer{layer_n}.neurons, 1);  %用于神经元的偏差保存
        
        fvnum = net.full_layer{layer_n}.neurons;%上一层的神经元个数。
        
        
    end
end  