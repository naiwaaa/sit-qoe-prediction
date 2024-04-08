% Function to evaluate QoE (pred_QoE_score) for a specified video given the trained SVR

function [pb_QoE_score, pb_pred_score, rebuf_QoE_score, rebuf_pred_score, overall_QoE_score,  overall_pred_score] = test_predict(video_no,trained_SVR,feedback_order,initial_QoE_score,linear_coeff)

%% Inputs

video_duration = 120; % in seconds

% recovery threshold
recovery_thresh = 2;

%% Initialize path and load files

path1 = 'QoE_matfiles/';

load rebuf_scores.mat

%% Initializations

[fps, rebuf_frequency, rebuf_duration] = identify_fps(video_no);

if video_no <= 18
    addr1 = [path1, 'TV0',num2str(ceil(video_no/2)), '_1080p', num2str(fps), '_', num2str(rebuf_frequency),'_',num2str(rebuf_duration), 's.mat'];
else
    addr1 = [path1, 'TV',num2str(ceil(video_no/2)), '_2160p', num2str(fps), '_', num2str(rebuf_frequency),'_',num2str(rebuf_duration), 's.mat'];
end

load(addr1);

load rebuf_scores.mat
rebuf_time_instances_video = rebuf_time_instances{video_no};

rebuf_instances_index = 1;
postbuf_flag = 0;
postbuf_flag_counter = 0;

pb_time = 0;
overall_time = 0;
rebuf_time = 0;

clear prebuf_QoE_score
clear postbuf_QoE_score

%% Begin Prediction

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
    
    % check if the time instant is a rebuffering time instant
    if(rebuf_instances_index <= length(rebuf_time_instances_video))
        if(rebuf_temp == 0)
            rebuf_temp = 1;
        end  
        
        if(t == rebuf_temp)  
            
            % predict the prebuf playback QoE
            
            % collect playback features
            pb_time = pb_time + 1;
            overall_time = overall_time + 1;
            
            pb_ft = qSTRRED(t);                                               
            
            if(overall_time > feedback_order)
                for ii = 1:feedback_order
                    pb_ft(ii+1) = overall_pred_score(overall_time-ii);
                end            
            end
            
            if(overall_time <= feedback_order)
                overall_pred_score(overall_time) = initial_QoE_score;
                pb_pred_score(pb_time) = initial_QoE_score;                
            else                
                overall_pred_score(overall_time) = predict(trained_SVR,pb_ft);
                pb_pred_score(pb_time) = overall_pred_score(overall_time);
            end

            % collect playback and overall QoE scores
            pb_QoE_score(pb_time) = subjective_score_continuous(overall_time);                      
            overall_QoE_score(overall_time) = subjective_score_continuous(overall_time); 
            
            % store prebuf QoE score
            prebuf_QoE_score = overall_pred_score(overall_time);
            
            rebuf_flag = 1; 
            
            % collect rebuffering QoE scores
            for tt = 1:rebuf_duration+(instant_rebuf_count*rebuf_duration)
                
                % if there is another rebuffering instance within the same playback time
                if(tt > rebuf_duration && rebuf_flag == 1)                    
                    prebuf_QoE_score = overall_pred_score(overall_time);
                    rebuf_flag = 0;
                end
                
                rebuf_time = rebuf_time + 1;
                overall_time = overall_time + 1;                               
                
                if(overall_time == 1)                    
                    overall_pred_score(overall_time) = initial_QoE_score;
                    rebuf_pred_score(rebuf_time) = initial_QoE_score;
                else
                    lambda = linear_coeff(1)*prebuf_QoE_score + linear_coeff(2);
                    overall_pred_score(overall_time) = overall_pred_score(overall_time-1)*exp(-lambda);                        
                    rebuf_pred_score(rebuf_time) = overall_pred_score(overall_time);                                           
                end
                
                % collect rebuffering and overall QoE scores
                rebuf_QoE_score(rebuf_time) = subjective_score_continuous(overall_time);
                overall_QoE_score(overall_time) = subjective_score_continuous(overall_time);
                
            end
            rebuf_instances_index = rebuf_instances_index + 1 + instant_rebuf_count;                        
          
            % if there are multiple rebuffering instances within a second                              
            postbuf_flag = 1;            
            postbuf_QoE_score = overall_pred_score(overall_time);
        
        else      
            
            if(postbuf_flag == 0)
                
                pb_time  = pb_time + 1;
                overall_time = overall_time + 1;
                
                % playback features
                pb_ft = qSTRRED(t);
                                         
                if(overall_time > feedback_order)                   
                    for ii = 1:feedback_order
                        pb_ft(ii+1) = overall_pred_score(overall_time-ii);
                    end            
                end
            
                if(overall_time <= feedback_order)
                    overall_pred_score(overall_time) = initial_QoE_score;
                    pb_pred_score(pb_time) = initial_QoE_score;
                else
                    overall_pred_score(overall_time) = predict(trained_SVR,pb_ft);
                    pb_pred_score(pb_time) = overall_pred_score(overall_time);
                end
            
                % collect playback and overall QoE scores
                pb_QoE_score(pb_time) = subjective_score_continuous(overall_time);            
                overall_QoE_score(overall_time) = subjective_score_continuous(overall_time);
            
            else
                
                postbuf_flag_counter = postbuf_flag_counter + 1;                
                
                pb_time  = pb_time + 1;
                overall_time = overall_time + 1;

                % playback features
                pb_ft = qSTRRED(t);                                                  
                
                for ff = 1:feedback_order
                    pb_ft(ff+1) = postbuf_QoE_score;
                end                
                for ff = 1:feedback_order    
                    if(ff <= postbuf_flag_counter)
                        pb_ft(ff+1) = overall_pred_score(overall_time-ff);
                    end
                end                
                
                if(overall_time <= feedback_order)
                    overall_pred_score(overall_time) = postbuf_QoE_score;
                    pb_pred_score(pb_time) = overall_pred_score(overall_time);
                else
                    overall_pred_score(overall_time) = predict(trained_SVR,pb_ft);
                    pb_pred_score(pb_time) = overall_pred_score(overall_time);
                end
                
                % collect playback and overall QoE scores
                pb_QoE_score(pb_time) = subjective_score_continuous(overall_time);            
                overall_QoE_score(overall_time) = subjective_score_continuous(overall_time);
            
                if(abs(overall_pred_score(overall_time) - prebuf_QoE_score) <= recovery_thresh)
                    postbuf_flag = 0;
                    postbuf_flag_counter = 0;
                    clear prebuf_QoE_score
                    clear postbuf_QoE_score 
                end                
            end
            
        end   
        
    else        
        
        % all rebufferings are done
        
        if(postbuf_flag == 0)
            
            pb_time  = pb_time + 1;
            overall_time = overall_time + 1;                

            pb_ft = qSTRRED(t);                

            if(overall_time > feedback_order)
                for ii = 1:feedback_order
                    pb_ft(ii+1) = overall_pred_score(overall_time-ii);
                end            
            end

            if(overall_time <= feedback_order)
                overall_pred_score(overall_time) = initial_QoE_score;
                pb_pred_score(pb_time) = overall_pred_score(overall_time);
            else
                overall_pred_score(overall_time) = predict(trained_SVR,pb_ft);
                pb_pred_score(pb_time) = overall_pred_score(overall_time);                    
            end

            % collect playback and overall QoE scores            
            pb_QoE_score(pb_time) = subjective_score_continuous(overall_time);
            overall_QoE_score(overall_time) = subjective_score_continuous(overall_time);
            
        else
            
            postbuf_flag_counter = postbuf_flag_counter + 1;
            
            pb_time  = pb_time + 1;
            overall_time = overall_time + 1;

            % collect playback features
            pb_ft = qSTRRED(t);            

            for ff = 1:feedback_order
                pb_ft(ff+1) = postbuf_QoE_score;
            end                
            for ff = 1:feedback_order    
                if(ff <= postbuf_flag_counter)
                    pb_ft(ff+1) = overall_pred_score(overall_time-ff);
                end
            end                

            if(overall_time <= feedback_order)
                overall_pred_score(overall_time) = postbuf_QoE_score;
                pb_pred_score(pb_time) = overall_pred_score(overall_time);
            else
                overall_pred_score(overall_time) = predict(trained_SVR,pb_ft);
                pb_pred_score(pb_time) = overall_pred_score(overall_time);
            end

            % collect playback and overall QoE scores
            pb_QoE_score(pb_time) = subjective_score_continuous(overall_time);
            overall_QoE_score(overall_time) = subjective_score_continuous(overall_time);
            
            if(abs(overall_pred_score(overall_time) - prebuf_QoE_score) <= recovery_thresh)
                postbuf_flag = 0;
                postbuf_flag_counter = 0;
                clear prebuf_QoE_score
                clear postbuf_QoE_score 
            end                
        end            

    end

end

end
