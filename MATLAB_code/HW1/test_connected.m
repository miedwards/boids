num_tests = 1e5
while num_tests > 0
    mat_size = uint32(rand*45)+5;
    sample_mat = gen_sample(mat_size);
    is_connected = Connected(sample_mat);
    num_comp = num_connected_components(sample_mat);
    if( is_connected ~= (num_comp == 1) )
        disp('Test fails for:')
        disp(sample_mat)
        break
    end
    num_tests = num_tests - 1;
end