function RMSE = compute_RMSE(x,y)

z = x - y;

RMSE = sqrt(sum(z.^2)/length(z));

