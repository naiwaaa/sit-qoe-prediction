function out = rmse(y_pred, y_test)

out = sqrt(mean((y_pred - y_test).^2));

end

