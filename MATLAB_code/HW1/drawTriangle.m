function drawTriangle(position,orientation)
N = size(position,2);
for ii = 1:N
    % define the vertices of the triangle around the position input
    T=[0 .5;
        -0.25 -0.5;
        0.25 -0.5];
    % close the polygon
    T(4,:)=T(1,:);
    %now we need to apply the rotation matrix.
    R = [cos(orientation(ii)-(pi/2)) -sin(orientation(ii)-(pi/2));
         sin(orientation(ii)-(pi/2))  cos(orientation(ii)-(pi/2))];
    S =  (R*T')'+repmat(position(:,ii)',4,1);
    
    fill(S(:,1),S(:,2),'b');
    hold on;
end
