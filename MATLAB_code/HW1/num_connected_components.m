function [ num_components ] = num_connected_components( adj_mat )
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here
num_components = sum(abs(eig(double(adj_laplacian(adj_mat))))<1e-13);
end

