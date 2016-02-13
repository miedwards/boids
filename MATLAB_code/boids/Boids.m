clear all;
N=20;
separation_minrange = 0.0;
separation_maxrange = 0.5;
alignment_minrange = 0.2;
alignment_maxrange = 1.2;
cohesion_minrange = 0.8;
cohesion_maxrange = 1.9;

position =5*rand(2,N);
h=0.001;
angle=-pi + (2*pi)*rand(1,N);
for ii=2:30000
    position = position + h*[cos(angle);sin(angle)];
    
    axis([-10 10 -10 10])
    hold off;
    D=squareform(pdist(position')); % Distance Matrix
    AdjCohesion = D<cohesion_maxrange & D > cohesion_minrange;
    AdjAlignment = D<alignment_maxrange & D > alignment_minrange;
    AdjSeparation = D<separation_maxrange & D > separation_minrange;

    for jj=1:N
        cohesion_boids=position;
        if find(~AdjCohesion(jj,:))
            cohesion_boids(:,find(~AdjCohesion(jj,:)))=[];
        end
        alignment_boids=position;
        if find(~AdjAlignment(jj,:))
            alignment_boids(:,find(~AdjAlignment(jj,:)))=[];
        end
        
        alignment_ang=angle;
        alignment_ang(find(~AdjAlignment(jj,:)))=[];
        
        d=sort(D(jj,:));

        if( ~isempty(alignment_ang) ) % TODO balance the terms properly
            averageHeading = averageAngles(alignment_ang);
        else
            averageHeading = angle(jj);
        end
        
        if( ~isempty(cohesion_boids) )
            averagePosition = mean(cohesion_boids,2);
        else
            averagePosition = position(:,jj);
        end 
        
        separation_boids=position;
        if find(~AdjSeparation(jj,:))
            separation_boids(:,find(~AdjSeparation(jj,:)))=[];
        end        
        
        nearestNeighbor = find(D(jj,:)==d(2));
        alignmentTerm(jj) = averageHeading;
        cohesionTerm(jj) = atan2(averagePosition(2)-position(2,jj),averagePosition(1)-position(1,jj));
        separationTerm(jj) = ...
            atan2(position(2,jj)-position(2,nearestNeighbor),...
            position(1,jj)-position(1,nearestNeighbor));
        v(jj) = averageAngles( [alignmentTerm(jj) alignmentTerm(jj) alignmentTerm(jj) cohesionTerm(jj) separationTerm(jj)]);

    end
    angle = v;     
    % u = separationTerm;
    drawTriangle(position,angle);

    [fromBoid, toBoid] = find(AdjAlignment);
    adjEdges = [fromBoid';toBoid'];
    for iii = adjEdges
        fromBd = iii(1);
        toBd = iii(2);
        if fromBd < toBd
            fromPos = position(:,fromBd);
            toPos = position(:, toBd);
            plot(fromPos(1):(toPos(1) - fromPos(1))*1e-3:toPos(1),...
                fromPos(2):(toPos(2) - fromPos(2))*1e-3:toPos(2),'y');
            %hold on
        end
    end
    
    [fromBoid, toBoid] = find(AdjCohesion);
    adjEdges = [fromBoid';toBoid'];
    for iii = adjEdges
        fromBd = iii(1);
        toBd = iii(2);
        if fromBd < toBd
            fromPos = position(:,fromBd);
            toPos = position(:, toBd);
            plot(fromPos(1):(toPos(1) - fromPos(1))*1e-3:toPos(1),...
                fromPos(2):(toPos(2) - fromPos(2))*1e-3:toPos(2),'g');
            %hold on
        end
    end
    
    [fromBoid, toBoid] = find(AdjSeparation);
    adjEdges = [fromBoid';toBoid'];
    for iii = adjEdges
        fromBd = iii(1);
        toBd = iii(2);
        if fromBd < toBd
            fromPos = position(:,fromBd);
            toPos = position(:, toBd);
            plot(fromPos(1):(toPos(1) - fromPos(1))*1e-2:toPos(1),...
                fromPos(2):(toPos(2) - fromPos(2))*1e-2:toPos(2),'r');
            %hold on
        end
    end
    %     u=-pi + (2*pi)*rand(1,N);
    pause(.001);
end