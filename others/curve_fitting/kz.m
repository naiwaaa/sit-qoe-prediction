function out = kz(Z)

out = Z(2)/Z(1);

for i=3:numel(Z)
    out = out + Z(i-1)/Z(i);
end

out = 1/(numel(Z) -1) * out;

end