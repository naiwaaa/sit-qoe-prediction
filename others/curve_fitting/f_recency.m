function r = f_recency(t, length, alpha)
r = exp(-alpha*(length - t));
end