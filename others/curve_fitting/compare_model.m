function out = compare_model(X, k)
lambda = 0.67;
    if k > 0
        out = lambda*compare_model(X, k-1) + (1-lambda)*X(k);
    else
        out = 1-lambda;
    end
end