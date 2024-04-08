function c = f_cumulative(params, input)

c = zeros(size(input, 1), 1);
for k = 1:size(input, 1)
    qoe = input{k, 1};
    nr = input{k, 2};
    tr = input{k, 3};
    doi = input{k, 4};
    
    alpha_p = 0.6807;
    alpha_r = 0.6807;
    alpha_rp = 0.3404;
    
    length = numel(qoe);
    
    memory_weight = zeros(1, length);
    
    for i = 1:length
        memory_weight(i) = params(3)*f_primacy(i, alpha_p)...
            + params(4)*f_recency(i, length, alpha_r)...
            + params(5)*f_repetition(tr(i), nr(i), alpha_rp);
    end
    memory_weight = memory_weight/sum(memory_weight);
    past = memory_weight * qoe';
    
%     disp(params(1) * past)
    
    c(k) = params(1) * past + params(2)*doi;
end

end
