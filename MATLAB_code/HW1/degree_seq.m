function [ exists ] = degree_seq( sequence )
%Implements the Erd?s?Gallai theorem
%   Detailed explanation goes here
if( mod(sum(sequence),2) )
    exists = false;
    return
end
sorted_seq = sort(sequence,'descend');
for k = 1:length(sorted_seq)
    if( sum(sorted_seq(1:k)) > k*(k-1) + sum(min(k, sorted_seq(k+1:end))) )
        exists = false;
        return
    end
end
exists = true;
end

