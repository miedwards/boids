%min_mat_size = 5;
%max_mat_size = 50;

mat_size = 5%uint16(rand*(max_mat_size - min_mat_size))+min_mat_size

% Generate a minimally connected matrix
test_mat = zeros(mat_size);
for jj = 2:mat_size
    test_mat(jj,jj-1) = 1;
    test_mat(jj-1,jj) = 1;
end

num_edges = mat_size - 1;
num_iterations = mat_size*(mat_size-1.0)/2.0 - num_edges+1;
agreement_steps = zeros(mat_size*(mat_size-1.0)/2.0-num_edges, 1);

tic; 
tolorance = 1e-2
InitialTheta = [-pi:2.0*pi/(mat_size-1):pi]'/2
Omega = zeros(size(InitialTheta)) %-0.9*InitialTheta
h = 1e-2

for jj = 1:num_iterations
    Theta = p3( test_mat, h, InitialTheta, Omega, tolorance );
    graph_steps = min(size(Theta, 2), 1400);
    figure
    for kk = 1:mat_size
        plot(1:graph_steps, Theta(kk,1:graph_steps))
        hold on
    end
    hold off
    agreement_steps(jj) = size(Theta,2);
    adj_mat_updated = false;
    for ii = 1:mat_size
        for iii = 1:mat_size
            if( ii ~= iii && ~test_mat(ii,iii) )
                test_mat(ii,iii) = 1;
                test_mat(iii,ii) = 1;
                adj_mat_updated = true;
                break
            end
        end
        if( adj_mat_updated )
            break
        end
    end
end
figure
plot( num_edges:num_edges+num_iterations-1, agreement_steps )
toc