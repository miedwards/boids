% A variation of "boid" swarm logic so that each boid moves a small step
% towards the center, a big step towards its friend boid, and a medium
% step away from its enemy boid. Each round, friend and enemy of each
% boid are randomly chosen.

% n = number of boids
% size = size of the boid field
% steps = number of rounds to simulate

function boid_dance( n, size, steps )
    % Step sizes for movement
    w = [.2, 5, -3]; % [center, friend, enemy]    
    
    function d = unit_dir_vector(p1, p2)
        nv = norm(p2 - p1);
        if nv > 0.05
            d = (p2 - p1) / nv;
        else
            d = [0, 0];
        end
    end
    
    % Initial coordinates of boids
    x = rand(1, n) * size;
    y = rand(1, n) * size;
    s = scatter(x, y, 20, 'MarkerFaceColor', 'g');    
    axis([0, size, 0, size]);
    title('Dancing Boids');
    
    for t = 1:steps
        friend = randi(n, 1, n);
        enemy = randi(n, 1, n);
        for iter = 1:30
            c = [mean(x), mean(y)];
            xn = zeros(1, n);
            yn = zeros(1, n);
            for k = 1:n                    
                % towards center
                d = unit_dir_vector([x(k), y(k)], c);
                xn(k) = x(k) + w(1) * d(1);
                yn(k) = y(k) + w(1) * d(2);
                % towards friend
                d = unit_dir_vector([x(k), y(k)], [x(friend(k)), y(friend(k))]);
                xn(k) = xn(k) + w(2) * d(1);
                yn(k) = yn(k) + w(2) * d(2);
                % away from enemy
                d = unit_dir_vector([x(k), y(k)], [x(enemy(k)), y(enemy(k))]);
                xn(k) = xn(k) + w(3) * d(1);
                yn(k) = yn(k) + w(3) * d(2);                                
            end
            x = xn;
            y = yn;
            pause(0.02);
            set(s, 'XData', x);
            set(s, 'YData', y);
            refreshdata;
            drawnow
        end        
    end
end