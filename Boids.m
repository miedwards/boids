clear all;
N=20;
separation_minrange = 0.0;
separation_maxrange = 1.0;
alignment_minrange = 0.9;
alignment_maxrange = 2.0;
cohesion_minrange = 1.9;
cohesion_maxrange = 3.0;

position =5*rand(2,N);
h=0.001;
angle=-pi + (2*pi)*rand(1,N);
for ii=2:30000
    position = position + h*[cos(angle);sin(angle)];
    
    axis([-10 10 -10 10])
    hold off;
    D=squareform(pdist(position')); % Distance Matrix
    AdjCohesion=D;
    AdjCohesion(D<cohesion_maxrange & D > cohesion_minrange);
    AdjAlignment=D;
    AdjAlignment(D<alignment_maxrange & D > alignment_minrange);
    AdjSeparation=D;
    AdjSeparation(D<separation_maxrange & D > separation_minrange);

    for jj=1:N
        cohesion_boids=position;
        if find(~AdjCohesion(jj,:))
            cohesion_boids(:,find(~AdjCohesion(jj,:)))=[];
        end
        alignment_boids=position;
        if find(~AdjAlignment(jj,:))
            alignment_boids(:,find(~AdjAlignment(jj,:)))=[];
        end
        separation_boids=position;
        if find(~AdjSeparation(jj,:))
            separation_boids(:,find(~AdjSeparation(jj,:)))=[];
        end
        
        alignment_ang=angle;
        alignment_ang(find(~AdjAlignment(jj,:)))=[];
        
        d=sort(D(jj,:));
        
        averagePosition = mean(cohesion_boids,2);
        averageHeading = averageAngles(alignment_ang);
        nearestNeighbor = find(D(jj,:)==d(2));
        alignmentTerm(jj) = averageHeading;
        cohesionTerm(jj) = atan2(averagePosition(2)-position(2,jj),averagePosition(1)-position(1,jj));
        separationTerm(jj) = atan2(position(2,jj)-position(2,nearestNeighbor),position(1,jj)-position(1,nearestNeighbor));
        v(jj) = averageAngles( [alignmentTerm(jj) alignmentTerm(jj) alignmentTerm(jj) cohesionTerm(jj) separationTerm(jj)]);
    end
angle = v;     
% u = separationTerm;
drawTriangle(position,angle);
s = size(AdjCohesion);

for ii = find(AdjCohesion)
    xPos = mod(, s[0]);
    position(ii)
end
%     u=-pi + (2*pi)*rand(1,N);
    pause(.001);
end