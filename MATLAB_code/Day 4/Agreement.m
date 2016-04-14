function [ total_time, output_positions ] = Agreement( positions, adjacency )
%AGREEMENT Summary of this function goes here
%   Detailed explanation goes here

time_step = 0.01;
total_time = 0.0;
tolorance = 0.02;
s = size(positions);
difference = sqrt(sum((positions-ones(s(1),1)*mean(positions)).^2,2));
output_positions = [];
output_positions(:,:,1) = positions;
index = 2;
while max(difference) > mean(positions) * tolorance   
    change = - adj_laplacian(adjacency)*positions;
    positions = time_step * change + positions;
    output_positions(:,:,index) = positions;
    index = index + 1;
    total_time = total_time + time_step;
    difference = sqrt(sum((positions-ones(s(1),1)*mean(positions)).^2,2));
end
for i = 1:s(1)
    plot(squeeze(output_positions(i,1,:)),squeeze(output_positions(i,2,:)),'.')
    hold on
end
hold off
end

