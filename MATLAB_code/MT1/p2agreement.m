function [ s, x ] = p2agreement( N, initial_x, alpha, d )
%UNTITLED4 Summary of this function goes here
%   Detailed explanation goes here
L = diag(sum(N)) - N;
x = initial_x;
TOLORANCE = 1e-3;
s = 0;
plot(ones(size(x))*s, x, '*')
hold on
while norm(x - (alpha*ones(size(x))+d)) > TOLORANCE && s < 2e2 %norm(x-mean(x)) > TOLORANCE && s < 2e3 % - (alpha*ones(size(x))+d)) > TOLORANCE
    %x = -L*x*1e-3 + x;
    x = (-alpha.*L)*x+d.*x;
    s = s+1;
    plot(ones(size(x))*s, x, '*')
    hold on
end
hold off


