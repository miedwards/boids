function [ Theta ] = p3( G, h, InitialTheta, Omega, tolorance )
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here
Theta = InitialTheta;
function o = rms_diff(a)
    o = sqrt(sum((a - mean(a)).^2));
end
time_step = 1;
max_steps = 1e5;
while rms_diff(Theta(:,time_step)) > tolorance * rms_diff(InitialTheta)...
        && time_step < max_steps;
    change = Omega;
    for ii = 1:length(change)
        for jj = 1:length(change) 
            if( G(ii, jj) )
                change(ii) = change(ii) + ...
                    sin(Theta(jj,time_step) - Theta(ii,time_step));
            end
        end
    end
    Theta(:,time_step+1) = h*change + Theta(:,time_step);
    time_step = time_step + 1;
end
end

