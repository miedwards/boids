%min_mat_size = 5;
%max_mat_size = 50;

mat_size = 20%uint16(rand*(max_mat_size - min_mat_size))+min_mat_size

% Generate a minimally connected matrix
test_mat = zeros(mat_size);
for jj = 2:mat_size
    test_mat(jj,jj-1) = 1;
    test_mat(jj-1,jj) = 1;
end
initial_positions = rand(mat_size,2);
num_edges = mat_size - 1;
num_iterations = mat_size*(mat_size-1.0)/2.0 - num_edges+1;
agreement_times = zeros(mat_size*(mat_size-1.0)/2.0-num_edges,1);
all_eigenvalues = [];



for jj = 1:num_iterations
    [eigenvecs, eigenvals] = eig(adj_laplacian(test_mat));
    eigvalmat = diag(eigenvals);
    eigenvals = sort(eigenvals*ones(mat_size,1), 'ascend');
    all_eigenvalues(jj,:) = eigenvals;
    agreement_times(jj) = Agreement(initial_positions, test_mat);
    
    
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