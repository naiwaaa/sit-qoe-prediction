function out = f_test(params, input)

disp(input)
disp('===')
out = params(1) + params(2)*exp(-params(3)*input);

end

