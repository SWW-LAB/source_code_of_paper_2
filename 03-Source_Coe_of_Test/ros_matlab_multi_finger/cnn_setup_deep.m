function net = cnn_setup_deep(net, x, y)  
    inputmaps = 1;  %�ò������ͼƬ����
    full_n = numel(net.full_layer); %ȫ���Ӳ���� 
    mapsize = size(squeeze(x(:, :, 1)));  %x(:, :, 1,1)��ʾһ�ţ���д�ַ���ͼƬ:�����ͼƬ��С��mapsize=[28 28]
  
    % ����ͨ������net����ṹ������㹹��CNN����  
    % n = numel(A)��������A��Ԫ�ظ���   
    for layer_n = 1 : numel(net.conv_layer)   
        if strcmp(net.conv_layer{layer_n}.type, 'c') % �������� ����� 
            
            mapsize = mapsize - net.conv_layer{layer_n}.kernelsize + 1; %������ͼƬ��С
            
            fan_out = net.conv_layer{layer_n}.outputmaps * net.conv_layer{layer_n}.kernelsize ^ 2;  %�ò�Ȩֵw��Ŀ
            for j = 1 : net.conv_layer{layer_n}.outputmaps  %  output map  
                % fan_out������Ƕ�����һ���һ������map��������һ����Ҫ����һ������map��ȡoutputmaps��������  
                % ��ȡÿ�������õ��ľ���˲�ͬ������fan_out���������һ������µ�������Ҫѧϰ�Ĳ�������  
                % ����fan_in������ǣ�������һ�㣬Ҫ���ӵ���һ�������е�����map��Ȼ����fan_out�������ȡ����  
                % ��Ȩֵ����ȡ���ǵ�������Ҳ���Ƕ���ÿһ����ǰ������ͼ���ж��ٸ���������ǰ��  
                fan_in = inputmaps * net.conv_layer{layer_n}.kernelsize ^ 2;  
                for i = 1 : inputmaps  %  input map  
                    % �����ʼ��Ȩֵ��Ҳ���ǹ���outputmaps������ˣ����ϲ��ÿ������map������Ҫ����ô��������  
                    % ȥ�����ȡ������  
                    % rand(n)�ǲ���n��n�� 0-1֮�����ȡֵ����ֵ�ľ����ټ�ȥ0.5���൱�ڲ���-0.5��0.5֮��������  
                    % �� *2 �ͷŴ� [-1, 1]��Ȼ���ٳ��Ժ�����һ����why��  
                    % �������ǽ������ÿ��Ԫ�س�ʼ��Ϊ[-sqrt(6 / (fan_in + fan_out)), sqrt(6 / (fan_in + fan_out))]  
                    % ֮������������Ϊ������Ȩֵ����ģ�Ҳ���Ƕ���һ������map�����и���Ұλ�õľ���˶���һ����  
                    % ����ֻ��Ҫ������� inputmaps * outputmaps ������ˡ�  
                    net.conv_layer{layer_n}.k{i}{j} = (rand(net.conv_layer{layer_n}.kernelsize) - 0.5) * 2 * sqrt(6 / (fan_in + fan_out));  
                end  
                net.conv_layer{layer_n}.b{j} = 0; % ��ƫ�ó�ʼ��Ϊ0  
            end  
            % ֻ���ھ�����ʱ��Ż�ı�����map�ĸ�����pooling��ʱ�򲻻�ı������������������map��������  
            % ���뵽��һ�������map����  
            inputmaps = net.conv_layer{layer_n}.outputmaps;   
        end
        if strcmp(net.conv_layer{layer_n}.type, 's') % �������� �Ӳ�����  ���ػ��㣩
            if layer_n == numel(net.conv_layer)
                mapsize = floor([net.conv_layer{layer_n}.scale_1 net.conv_layer{layer_n}.scale_2]);%���ڿռ�������ػ���ͼƬ��С
            else
                mapsize = floor(mapsize / net.conv_layer{layer_n}.scale); %pooling��ͼ���С 
            end
            for j = 1 : inputmaps % inputmap������һ���ж���������ͼ ���ػ�������һ��ľ�������Ԫһ���ࣩ
                net.conv_layer{layer_n}.b{j} = 0; % ��ƫ�ó�ʼ��Ϊ0  
            end  
        end  
    end  
      
    %������ĵ�һ��ȫ���Ӳ�������С
    fvnum = prod(mapsize) * inputmaps;  %ÿ����Ԫ��������Ŀ��prod(mapsize)�������=map����*map����
    %ȫ���ӵĲ�������
    output_num = size(y, 1);  %�����Ԫ����.
    
    net.full_layer{full_n}.neurons = output_num;
    
    for layer_n = 1 :full_n
        
        net.full_layer{layer_n}.w = (rand(net.full_layer{layer_n}.neurons, fvnum) - 0.5) * 2 * sqrt(6 / (net.full_layer{layer_n}.neurons + fvnum)); %ȫ�����е�Ȩֵ��ʼ��
        
        net.full_layer{layer_n}.b = zeros(net.full_layer{layer_n}.neurons, 1);  %������Ԫ��ƫ���
        
        fvnum = net.full_layer{layer_n}.neurons;%��һ�����Ԫ������
        
        
    end
end  