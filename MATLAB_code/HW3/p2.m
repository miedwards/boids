function [ values ] = p2( D, h, init )
%UNTITLED4 Summary of this function goes here
%   Detailed explanation goes here
values(:,1) = init;
deg = diag(sum(D,2));
L = deg -D;
A = -L*h;
for ii = 2:1e4
    values(:,ii) = A*values(:,ii-1);
end

end

