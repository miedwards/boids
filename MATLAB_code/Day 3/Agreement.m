function [ total_time ] = Agreement( positions, adjacency )
%AGREEMENT Summary of this function goes here
%   Detailed explanation goes here

time_step = 0.01;
total_time = 0.0;
tolorance = 0.02;
change = zeros(length(positions),1);

while (max(positions) - min(positions)) > mean(positions) * tolorance     
    for node = 1:length(positions)
        change(node) = sum(positions(logical(adjacency(node,:))) - positions(node));
    end
    positions = time_step * change(node) + positions;
    total_time = total_time + time_step;
end
end

