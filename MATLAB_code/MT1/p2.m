sample_fully_connected_graph = ones(5) - diag(ones(5,1))
initial_x = [2, 9, 1, 5, 3]
alpha = 1%5.5
d = ones(1,5)%[ -2, 3, -1, 4, 0]
alpha * ones(1,5) + d
[s, x] = p2agreement(sample_fully_connected_graph, initial_x', alpha, d')


