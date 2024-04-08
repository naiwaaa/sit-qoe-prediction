function [fps, rebuf_frequency, rebuf_duration] = identify_fps(video_no)

rebuf_info = [1 7; 2 2; 2 5; 4 9; 2 9; 4 2; 0.5 5; 3 1; 0.5 2; 5 3; 1 3; 5 7; 0.5 9; 4 5; 3 7; 5 1; 1 1; 3 3;
              0.5 1; 5 5; 0.5 7; 5 2; 0.5 3; 4 7; 2 7; 3 2; 1 5; 4 1; 1 9; 2 3; 2 1; 3 9; 3 5; 4 3; 1 2; 5 9];

rebuf_frequency = rebuf_info(video_no,1);
rebuf_duration = rebuf_info(video_no,2);

if(video_no <= 18)
        
        fps = 30;
        YUV = '422';
    
        % for 1080p videos only
        if(ceil(video_no/2) == 5)
            fps = 25;        
        end

        if(ceil(video_no/2) == 6)
            fps = 60;
            YUV = '420';
        end

        if(ceil(video_no/2) == 8)
            fps = 24;
            YUV = '420';
        end
        
else        
        fps = 30;
        YUV = '420';
end