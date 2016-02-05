function thetaBar = averageAngles(thetas)

x=[cos(thetas);
   sin(thetas)];

avgX = mean(x,2);

thetaBar = atan2(avgX(2),avgX(1));