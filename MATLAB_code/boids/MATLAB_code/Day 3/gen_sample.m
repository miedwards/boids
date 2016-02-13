function [ output_args ] = gen_sample( n )
%UNTITLED Summary of this function goes here
%   Detailed explanation goes hereo
output_args = rand(n) > 0.5;
output_args = output_args & output_args' & ~eye(n);
end

