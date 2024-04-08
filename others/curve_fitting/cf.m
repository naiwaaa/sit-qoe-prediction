function [train, test, train_pred, test_pred, params] = cf()

train = load('train.mat');
test = load('test');
init = [2,2,2, 2,2];

opts = optimoptions('lsqcurvefit', 'FiniteDifferenceType', 'central');
params = lsqcurvefit(@(b, x)(f_cumulative(b, x)), init, train.x, train.y', [0,0,0,0,0], [1,1,1,1,1], opts) 
% params = nlinfit(train.x, train.y', @(b, x)(f_cumulative(b, x)), init, opts)

train_pred = f_cumulative(params, train.x);
test_pred = f_cumulative(params, test.x);

disp(['PCC: ', num2str(corr(train_pred, train.y')), ' ', num2str(corr(test_pred, test.y', 'type', 'Spearman'))])
disp(['SROCC: ', num2str(corr(train_pred, train.y', 'type', 'Spearman')), ' ', num2str(corr(test_pred, test.y', 'type', 'Spearman'))])
disp(['RMSE: ', num2str(rmse(train_pred, train.y')), ' ', num2str(rmse(test_pred, test.y'))])

end