function [ output_args ] = Connected( adjacency_matrix )
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here
visited = zeros(length(adjacency_matrix),1);
to_visit = 1;
while ~isempty(to_visit);
    pos = to_visit(1);
    to_visit = to_visit(2:end);
    if(visited(pos))
        continue;
    end
    visited(pos) = 1;
    
    connects_to = find(adjacency_matrix(pos,:));
    for jj = connects_to
        if(~visited(jj))
            to_visit =  [jj to_visit];
        end
    end
end
output_args = isequal(length(adjacency_matrix),sum(visited));

