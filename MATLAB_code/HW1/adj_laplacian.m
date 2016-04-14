function [ output ] = adj_laplacian( Adj )
%ADJ_LAPLACIAN Summary of this function goes here
%   Detailed explanation goes here
output = diag(sum(Adj)) - Adj;
end

