clear
clc

load data
load cnn_deep

cnn_deep = cnn_feedforward_deep(cnn_deep,train_data_x(:,:,1));
b = cnn_deep.full_layer{2}.o;