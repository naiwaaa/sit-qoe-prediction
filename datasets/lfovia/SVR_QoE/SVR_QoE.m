%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%% MATLAB Code for SVR-QoE %%%%%%%%%%%%%%%%%%

% The code provides the performance of SVR-QoE on the LFOVIA QoE Database.

% Please cite the following work if you use this code:

% N. Eswara, M. K, A. Kommineni, S. Chakraborty, H. P. Sethuram, K. Kuchi, A. Kumar, S. S. Channappayya,
% “A Continuous QoE Evaluation Framework for Video Streaming over HTTP,” 
% accepted to IEEE Transactions on Circuits and Systems for Video Technology. 

% Author: Nagabhushan Eswara
% Date: December 2017

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


close all
clear
clc

warning off

tic

%% Inputs

% video duration
video_duration = 120; % in seconds

% No. of videos
no_videos = 36;

% Feedback order
feedback_order = 1;

% Initial QoE
initial_QoE_score = 50;

% VQA for STSQ
VQA = 'qSTRRED';

% training:test split percentage
training_percentage = 0.8;

% no. of realizations of training:test split
no_iter = 1000;

% filename for saving results
save_results = 'QoE_results.mat';

%% Initializing paths and loading matfiles

path1 = 'QoE_matfiles/';

load rebuf_scores.mat

no_training_videos = floor(training_percentage * no_videos);
no_test_videos = no_videos - no_training_videos;

%% Begin iterations

for iter = 1:no_iter
   
    clc
    disp('iteration')
    disp(iter)
    
    randseq = randperm(no_videos);
    TrV = randseq(1:no_training_videos);
    TrV = unique(TrV);

    % check the training-test split is unique every iteration
    if(iter > 1)
        TrV_flag = 0;
        while(TrV_flag == 0)
            for ii = 1:size(TrV_iter,1)
                while(TrV == TrV_iter(iter-ii,:))
                    randseq = randperm(no_videos);
                    TrV = randseq(1:no_training_videos);
                    TrV = unique(TrV);
                    break;
                end
            end
            TrV_flag = 1;
        end
    end
    TrV_iter(iter,:) = TrV; 
    
    TeV = setdiff(1:no_videos,TrV);
    TeV_iter(iter,:) = TeV;

%% Initializations

clear pb_row_count
clear pb_feature
clear rebuf_row_count
clear rebuf_loc_duration
clear rebuf_loc_index

clear pb_QoE_score
clear rebuf_QoE_score
clear rebuf_init_score
clear rebuf_init_score_index

pb_row_count = 0;
rebuf_row_count = 0;

rebuf_loc_duration = [];
rebuf_loc_index = 0;
rebuf_init_score_index = 0;

count_all = 0;
clear PrBQ_all
clear PrBQ_all_sorted
clear lambda_all
clear lambda_all_sorted

%% Training videos

for kk = 1:no_training_videos
    
training_video_no = TrV(kk);

[fps, rebuf_frequency, rebuf_duration] = identify_fps(training_video_no);

if training_video_no <= 18
    addr1 = [path1, 'TV0',num2str(ceil(training_video_no/2)), '_1080p', num2str(fps), '_', num2str(rebuf_frequency),'_',num2str(rebuf_duration), 's.mat'];
else
    addr1 = [path1, 'TV',num2str(ceil(training_video_no/2)), '_2160p', num2str(fps), '_', num2str(rebuf_frequency),'_',num2str(rebuf_duration), 's.mat'];
end

load(addr1)

rebuf_time_instances_video = rebuf_time_instances{training_video_no};

rebuf_instances_index = 1;
subjective_score_continuous_index = 0;
postbuf_flag = 0;

%% Collect features from the training video

for t = 1:video_duration
    
    % obtain the next rebuffering time instance
    if(rebuf_instances_index <= length(rebuf_time_instances_video))
        clear rebuf_temp
        rebuf_temp = floor(rebuf_time_instances_video(rebuf_instances_index));
        instant_rebuf_count = 0;
        for mm = rebuf_instances_index+1:length(rebuf_time_instances_video)
            if(floor(rebuf_time_instances_video(mm)) == rebuf_temp)
                instant_rebuf_count = instant_rebuf_count + 1;
            end
        end
    end
    
    % check whether the current time instant is a rebuffering time instant or not
    if(rebuf_instances_index <= length(rebuf_time_instances_video))
        if(rebuf_temp == 0)
            rebuf_temp = 1;
        end
        
        if(t == rebuf_temp)                    
            % collect playback features
            pb_row_count = pb_row_count + 1; 
            pb_feature_qSTRRED(pb_row_count,1) = qSTRRED(t);                

            if(pb_row_count <= feedback_order)
                for ff = 1:feedback_order
                    pb_feature_qSTRRED(pb_row_count,ff+1) = initial_QoE_score;                    
                end
                for ff = 1:pb_row_count-1                        
                    pb_feature_qSTRRED(pb_row_count,ff+1) = pb_QoE_score(pb_row_count-ff,1);
                end
            else
                for ff = 1:feedback_order
                    pb_feature_qSTRRED(pb_row_count,ff+1) = pb_QoE_score(pb_row_count-ff,1);
                end
            end
            
            % collect playback scores
            subjective_score_continuous_index = subjective_score_continuous_index + 1;            
            pb_QoE_score(pb_row_count,1) = subjective_score_continuous(subjective_score_continuous_index); 
            
            % store initial/prebuffering scores
            rebuf_init_score_index = rebuf_init_score_index + 1;
            rebuf_init_score(rebuf_init_score_index) = subjective_score_continuous(subjective_score_continuous_index);            
                        
            % this section identifies the rebufferings location w.r.t. playback time
            rebuf_loc_index = rebuf_loc_index + 1;
            rebuf_loc_duration(rebuf_loc_index) = rebuf_duration;
               
            rebuf_flag = 1;
            
            % collect rebuffering QoE scores
            for tt = 1:rebuf_duration+(instant_rebuf_count*rebuf_duration)                
            	rebuf_row_count = rebuf_row_count + 1;
                subjective_score_continuous_index = subjective_score_continuous_index + 1;
                rebuf_QoE_score(rebuf_row_count) = subjective_score_continuous(subjective_score_continuous_index);
                
                % if there is another rebuffering instance within the same playback time
                if(tt > rebuf_duration && rebuf_flag == 1)
                    rebuf_init_score_index = rebuf_init_score_index + 1;
                    rebuf_init_score(rebuf_init_score_index) = subjective_score_continuous(subjective_score_continuous_index-1);
                    rebuf_flag = 0;
                    rebuf_loc_index = rebuf_loc_index + 1;
                    rebuf_loc_duration(rebuf_loc_index) = rebuf_duration;
                end
            end
            rebuf_instances_index = rebuf_instances_index + 1 + instant_rebuf_count;                        
          
            % if there are multiple rebuffering instances within a second                              
            postbuf_flag = 1;            
            postbuf_QoE_score = subjective_score_continuous(subjective_score_continuous_index);                                    
            
        else                 
            if(postbuf_flag == 0) 
                
                pb_row_count = pb_row_count + 1;                
                pb_feature_qSTRRED(pb_row_count,1) = qSTRRED(t);                    

                if(pb_row_count <= feedback_order)
                    for ff = 1:feedback_order
                        pb_feature_qSTRRED(pb_row_count,ff+1) = initial_QoE_score;
                    end
                    for ff = 1:pb_row_count-1                        
                        pb_feature_qSTRRED(pb_row_count,ff+1) = pb_QoE_score(pb_row_count-ff,1);
                    end
                else
                    for ff = 1:feedback_order
                        pb_feature_qSTRRED(pb_row_count,ff+1) = pb_QoE_score(pb_row_count-ff,1);
                    end
                end
                      
                subjective_score_continuous_index = subjective_score_continuous_index + 1;            
                pb_QoE_score(pb_row_count,1) = subjective_score_continuous(subjective_score_continuous_index);
                
            else
                
                pb_row_count = pb_row_count + 1;                                
                pb_feature_qSTRRED(pb_row_count,1) = qSTRRED(t);
                
                if(pb_row_count <= feedback_order)
                    for ff = 1:feedback_order
                        pb_feature_qSTRRED(pb_row_count,ff+1) = postbuf_QoE_score;
                    end
                    for ff = 1:pb_row_count-1                        
                        pb_feature_qSTRRED(pb_row_count,ff+1) = pb_QoE_score(pb_row_count-ff,1);
                    end
                else
                    for ff = 1:feedback_order
                        pb_feature_qSTRRED(pb_row_count,ff+1) = pb_QoE_score(pb_row_count-ff,1);
                    end
                end
                      
                subjective_score_continuous_index = subjective_score_continuous_index + 1;            
                pb_QoE_score(pb_row_count,1) = subjective_score_continuous(subjective_score_continuous_index);
                
                postbuf_flag = 0;
                clear postbuf_QoE_score
                
            end
            
        end   
        
    else  
        
        % no more rebufferings
        
        if(postbuf_flag == 0)            

            pb_row_count = pb_row_count + 1;            
            pb_feature_qSTRRED(pb_row_count,1) = qSTRRED(t);

            if(pb_row_count <= feedback_order)
                for ff = 1:feedback_order
                    pb_feature_qSTRRED(pb_row_count,ff+1) = initial_QoE_score;
                end
                for ff = 1:pb_row_count-1                        
                    pb_feature_qSTRRED(pb_row_count,ff+1) = pb_QoE_score(pb_row_count-ff,1);
                end
            else
                for ff = 1:feedback_order
                    pb_feature_qSTRRED(pb_row_count,ff+1) = pb_QoE_score(pb_row_count-ff,1);
                end
            end                      
               
            subjective_score_continuous_index = subjective_score_continuous_index + 1;       
            pb_QoE_score(pb_row_count,1) = subjective_score_continuous(subjective_score_continuous_index);            

        else
            
            pb_row_count = pb_row_count + 1;            
            pb_feature_qSTRRED(pb_row_count,1) = qSTRRED(t);

            if(pb_row_count <= feedback_order)
                for ff = 1:feedback_order
                    pb_feature_qSTRRED(pb_row_count,ff+1) = postbuf_QoE_score;
                end
                for ff = 1:pb_row_count-1                        
                    pb_feature_qSTRRED(pb_row_count,ff+1) = pb_QoE_score(pb_row_count-ff,1);
                end
            else
                for ff = 1:feedback_order
                    pb_feature_qSTRRED(pb_row_count,ff+1) = pb_QoE_score(pb_row_count-ff,1);
                end
            end
                      
            subjective_score_continuous_index = subjective_score_continuous_index + 1;            
            pb_QoE_score(pb_row_count,1) = subjective_score_continuous(subjective_score_continuous_index);
                
            postbuf_flag = 0;
            clear postbuf_QoE_score
              
        end            

    end

end

%% Modeling rebuffering QoE scores, finding lambda

expfun = @(lambda,x) (exp(-lambda*x));
x = 0:rebuf_duration;
for ii = 1:2*rebuf_frequency
    QPrB = rebuf_scores{training_video_no,ii}(1);
    y = rebuf_scores{training_video_no,ii}/QPrB;    
    
    count_all = count_all + 1;
    lambda0 = 0.1;
    lambda_all(count_all) = nlinfit(x,y,expfun,lambda0);
        
    PrBQ_all(count_all) = QPrB;
end

end

%% SVR Training

pb_svr_qSTRRED = fitrsvm(pb_feature_qSTRRED,pb_QoE_score,'Standardize',true,'kernelfunction','rbf','KernelScale','auto');

%% Linear fit between prebuf QoE and lambda

% Sort in the increasing order of prebuf QoE score
[PrBQ_all_sorted, ind] = sort(PrBQ_all);
lambda_all_sorted = lambda_all(ind);

% linear fit
myfit = fit(PrBQ_all_sorted',lambda_all_sorted','poly1');
linear_coeff = [myfit.p1 myfit.p2];
       
%% Predict QoE for each test video using the trained SVR and lambda linear coefficients

for ii = 1:no_test_videos
	[QoE_score_pb_qSTRRED{iter,ii}, pred_score_pb_qSTRRED{iter,ii}, QoE_score_rebuf_qSTRRED{iter,ii},  pred_score_rebuf_qSTRRED{iter,ii}, QoE_score_overall_qSTRRED{iter,ii}, pred_score_overall_qSTRRED{iter,ii}] = test_predict(TeV(ii),pb_svr_qSTRRED,feedback_order,initial_QoE_score,linear_coeff);   
end

%% Evaluate the performance 

% for quantifying playback performance
Q_pb_qSTRRED = [];
p_pb_qSTRRED = [];

% for quantifying rebuffering performance
Q_rebuf_qSTRRED = [];
p_rebuf_qSTRRED = [];

% for quantifying overall performance
Q_overall_qSTRRED = [];
p_overall_qSTRRED = [];

for ii = 1:no_test_videos
    Q_pb_qSTRRED = [Q_pb_qSTRRED QoE_score_pb_qSTRRED{iter,ii}];
    p_pb_qSTRRED = [p_pb_qSTRRED pred_score_pb_qSTRRED{iter,ii}];

    Q_rebuf_qSTRRED = [Q_rebuf_qSTRRED QoE_score_rebuf_qSTRRED{iter,ii}];
    p_rebuf_qSTRRED = [p_rebuf_qSTRRED pred_score_rebuf_qSTRRED{iter,ii}];

    Q_overall_qSTRRED = [Q_overall_qSTRRED QoE_score_overall_qSTRRED{iter,ii}];
    p_overall_qSTRRED = [p_overall_qSTRRED pred_score_overall_qSTRRED{iter,ii}];      
end

%% Compute LCC, SROCC, and RMSE

LCC_test_pb_qSTRRED(iter) = corr(Q_pb_qSTRRED',p_pb_qSTRRED');
SROCC_test_pb_qSTRRED(iter) = corr(Q_pb_qSTRRED',p_pb_qSTRRED','type','Spearman');
RMSE_test_pb_qSTRRED(iter) = compute_RMSE(Q_pb_qSTRRED,p_pb_qSTRRED);

LCC_test_rebuf_qSTRRED(iter) = corr(Q_rebuf_qSTRRED',p_rebuf_qSTRRED');
SROCC_test_rebuf_qSTRRED(iter) = corr(Q_rebuf_qSTRRED',p_rebuf_qSTRRED','type','Spearman');
RMSE_test_rebuf_qSTRRED(iter) = compute_RMSE(Q_rebuf_qSTRRED,p_rebuf_qSTRRED);

LCC_test_overall_qSTRRED(iter) = corr(Q_overall_qSTRRED',p_overall_qSTRRED');
SROCC_test_overall_qSTRRED(iter) = corr(Q_overall_qSTRRED',p_overall_qSTRRED','type','Spearman');
RMSE_test_overall_qSTRRED(iter) = compute_RMSE(Q_overall_qSTRRED,p_overall_qSTRRED);

end


%% Display the results

disp('%%%%%%%%%%%%%%%%%%%%%% playback performance %%%%%%%%%%%%%%%%%%%%%%%')
disp('%%%%%%%%%%%%% mean %%%%%%%%%%%%%%%%%%')
disp('LCC_playback')
disp(mean(LCC_test_pb_qSTRRED))
disp('SROCC_playback')
disp(mean(SROCC_test_pb_qSTRRED))
disp('RMSE_playback')
disp(mean(RMSE_test_pb_qSTRRED))

disp('%%%%%%%%%%%%% median %%%%%%%%%%%%%%%%%%')
disp('LCC_playback')
disp(median(LCC_test_pb_qSTRRED))
disp('SROCC_playback')
disp(median(SROCC_test_pb_qSTRRED))
disp('RMSE_playback')
disp(median(RMSE_test_pb_qSTRRED))

disp('%%%%%%%%%%%%%%%%%%%%%% rebuffering performance %%%%%%%%%%%%%%%%%%%%%%%')
disp('%%%%%%%%%%%%% mean %%%%%%%%%%%%%%%%%%')
disp('LCC_rebuffering')
disp(mean(LCC_test_rebuf_qSTRRED))
disp('SROCC_rebuffering')
disp(mean(SROCC_test_rebuf_qSTRRED))
disp('RMSE_rebuffering')
disp(mean(RMSE_test_rebuf_qSTRRED))

disp('%%%%%%%%%%%%% median %%%%%%%%%%%%%%%%%%')
disp('LCC_rebuffering')
disp(median(LCC_test_rebuf_qSTRRED))
disp('SROCC_rebuffering')
disp(median(SROCC_test_rebuf_qSTRRED))
disp('RMSE_rebuffering')
disp(median(RMSE_test_rebuf_qSTRRED))

disp('%%%%%%%%%%%%%%%%%%%%%% overall performance %%%%%%%%%%%%%%%%%%%%%%%')
disp('%%%%%%%%%%%%% mean %%%%%%%%%%%%%%%%%%')
disp('LCC_overall')
disp(mean(LCC_test_overall_qSTRRED))
disp('SROCC_overall')
disp(mean(SROCC_test_overall_qSTRRED))
disp('RMSE_overall')
disp(mean(RMSE_test_overall_qSTRRED))

disp('%%%%%%%%%%%%% median %%%%%%%%%%%%%%%%%%')
disp('LCC_overall')
disp(median(LCC_test_overall_qSTRRED))
disp('SROCC_overall')
disp(median(SROCC_test_overall_qSTRRED))
disp('RMSE_overall')
disp(median(RMSE_test_overall_qSTRRED))

%% Save the results

save(save_results,'VQA','no_iter','TrV_iter','TeV_iter','feedback_order','training_percentage')
save(save_results,'-append','LCC_test_pb_qSTRRED','LCC_test_rebuf_qSTRRED','LCC_test_overall_qSTRRED');
save(save_results,'-append','SROCC_test_pb_qSTRRED','SROCC_test_rebuf_qSTRRED','SROCC_test_overall_qSTRRED');
save(save_results,'-append','RMSE_test_pb_qSTRRED','RMSE_test_rebuf_qSTRRED','RMSE_test_overall_qSTRRED');
save(save_results,'-append','QoE_score_pb_qSTRRED','pred_score_pb_qSTRRED');
save(save_results,'-append','QoE_score_rebuf_qSTRRED','pred_score_rebuf_qSTRRED');
save(save_results,'-append','QoE_score_overall_qSTRRED','pred_score_overall_qSTRRED');

toc