function X = activation_function(X)
    X = 1./(1+exp(-X));
    %X(find(X<0))=0;
end