num_tests = 1000
min_graph_size = 2
max_graph_size = 100
while num_tests > 0
    sample_gph = gen_sample(...
        uint16(rand*(max_graph_size - min_graph_size))+min_graph_size);
    if( ~isequal(adj_laplacian(sample_gph), laplacian(sample_gph)) )
        disp('failed')
        break
    end
    num_tests = num_tests -1;
end