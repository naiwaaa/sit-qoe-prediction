function rp = f_repetition(tr, nr, alpha)
if nr < 1.e-6
    rp = 0;
else
    rp = exp(-alpha/nr * tr);
end
end
