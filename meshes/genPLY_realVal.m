[V,F] = readPLY('spot_10K.ply');

L = -cotmatrix(V,F);
M = massmatrix(V,F);
[eVec,~] = eigs(L,M,5,'sm');
C = eVec(:,3);

writePLY('spot_10K.ply', V,F,'ascii');

fileID = fopen(strcat('spot_10K_realVal.txt'),'w');
for ii = 1:length(C)
    fprintf(fileID,'%f\n',C(ii));
end
fclose(fileID);