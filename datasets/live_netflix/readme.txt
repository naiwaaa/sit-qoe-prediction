LABORATORY FOR IMAGE AND VIDEO ENGINEERING 
The University of Texas at Austin
-----------COPYRIGHT NOTICE STARTS WITH THIS LINE------------
Copyright (c) 2016 The University of Texas at Austin. All rights reserved. Permission is hereby granted, without written agreement and without license or royalty fees, to use, copy, modify, and distribute this database (the videos, the results and the source files) and its documentation for any purpose, provided that the copyright notice in its entirety appear in all copies of this database, and the original source of this database, Laboratory for Image and Video Engineering (LIVE, http://live.ece.utexas.edu) at the University of Texas at Austin (UT Austin, http://www.utexas.edu), is acknowledged in any publication that reports research using this database. The database is to be cited in the bibliography as:
C. G. Bampis, Zhi Li, Anush K. Moorthy, Ioannis Katsavounidis, Anne Aaron, and A. C. Bovik, "Temporal Effects on Subjective Video Quality of Experience,"  submitted to IEEE Transactions on Image Processing
C. G. Bampis, Zhi Li, Anush K. Moorthy, Ioannis Katsavounidis, Anne Aaron, and A. C. Bovik, "LIVE-Netflix Video QoE Database," Online: http://live.ece.utexas.edu/research/LIVEStallStudy/index.html, 2016.
IN NO EVENT SHALL THE UNIVERSITY OF TEXAS AT AUSTIN BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT, SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE USE OF THIS DATABASE AND ITS DOCUMENTATION, EVEN IF THE UNIVERSITY OF TEXAS AT AUSTIN HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
THE UNIVERSITY OF TEXAS AT AUSTIN SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE. THE DATABASE PROVIDED HEREUNDER IS ON AN "AS IS" BASIS, AND THE UNIVERSITY OF TEXAS AT AUSTIN HAS NO OBLIGATION TO PROVIDE MAINTENANCE, SUPPORT, UPDATES, ENHANCEMENTS, OR MODIFICATIONS.
-----------COPYRIGHT NOTICE ENDS WITH THIS LINE------------
Please contact Christos Bampis (cbampis@gmail.com) if you have any questions.
The investigators on this research were:
Christos Bampis (cbampis@gmail.com) -- Department of ECE at UT Austin.
Dr. Alan C. Bovik (bovik@ece.utexas.edu) -- Department of ECE at UT Austin.
Zhi Li, Anush K. Moorthy, Ioannis Katsavounidis, Anne Aaron - Netflix Inc.
-------------------------------------------------------------------------
The subjective experiment release comes with the following files:
1. This readme file containing copyright information and usage information.
2. A VideoEncodes folder with a total of 39 publicly available videos:
	a. 3 reference 4:2:0 YUV videos (ref_yuv sub-folder)
	b. 24 distorted 4:2:0 YUV videos (dis_yuv sub-folder)
	c. 12 stall-removed 4:2:0 YUV videos (dis_yuv_stalls_removed)
These 39 videos are named using the following name convention:
“cont_” [content_index] “_seq_” [sequence_index]
The publicly available portion of this dataset consistes of 3 video sequences originating from the Consumer Digital Video Library (CDVL). These 3 contents were combined with 11 Netflix contents and were used the test phase of our video subjective study. Please find more details about the groups in our paper. 
3. A LIVE_NFLX_PublicData_Release folder containing the subjective data and the extracted features/metadata for all (public and Netflix) videos used in the subjective test.
DETAILS OF THE DATABASE AND THE SUBJECTIVE STUDY
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
We have created a new mobile video streaming database that models distortions caused by network impairments. In particular, we simulate adaptive HTTP streaming (HAS) strategies under mobile streaming scenarios. The LIVE-Netflix QoE Database consists of 112 videos generated from 14 reference videos with 8 unique playout patterns and almost 5000 (continuous and final) human opinions obtained from 56 subjects who viewed the videos on mobile devices. 
Details of the content and design of the database, our video subjective study framework can be found in:
C. G. Bampis, Zhi Li, Anush K. Moorthy, Ioannis Katsavounidis, Anne Aaron, and A. C. Bovik, "Temporal Effects on Subjective Video Quality of Experience,"  submitted to IEEE Transactions on Image Processing
C. G. Bampis, Zhi Li, Anush K. Moorthy, Ioannis Katsavounidis, Anne Aaron, and A. C. Bovik, "LIVE-Netflix Video QoE Database," Online: http://live.ece.utexas.edu/research/LIVEStallStudy/index.html, 2016.
DETAILS OF FILES PROVIDED IN THIS RELEASE
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
MATLAB .mat files
A. There are 112 .mat files having the following naming convention: “cont_” [content_index] “_seq_” [sequence_index]. The content index goes from 1 to 14 (14 contents) and the sequence index from 0 to 7 (8 playout patterns). These .mat files contain the following metadata (VideoData sub-folder):
1.	[quality_model]_vec: denotes the frame quality scores for each quality model
2.	[quality_model]_[pooling_type] denotes the pooled quality scores using average, hysteresis or VQpooling (indicated by kmeans)
3.	Nframes: number of frames
4.	vid_fps: frame rate
5.	final_subj_score: final (summary) QoE ratings after subject rejection and Z-scoring per viewing session and per subject
6.	continuous_subj_score: continuous QoE ratings after subject rejection and Z-scoring per viewing session and per subject
7.	ns: number of stalls (rebuffering events) for the video
8.	ds: duration of the stalls (in seconds)
9.	lt: duration of encoding bitrate less than 250 kbps (in seconds)
10.	VSQM: VsQM metric extracted for this video
11.	tsl: time since last impairment finished (bitrate or rebuffering) measured in seconds. This time interval is measured from the time the last impairment finished until the video finishes (where it is assumed that the subject is asked to give his retrospective QoE evaluation). For patterns 0 and 2 this value is set equal to the video duration. The assumption here is to consider only the adaptive streaming strategies when calculating the memory effect.
B. There is also a single .mat file called LIVE_NFLX_Network_Impairments.mat. This file contains the following metadata for all videos:
1.	first column: name of the video sequence (follows standard naming convention as shown before)
2.	second column: frame indices where the video has an encoding bitrate less than the maximum value (250 kbps)
3.	third column: frame indices of rebuffering for each video
Comments:
You can compute your own quality metric on the publicly available portion of the dataset by using the given 4:2:0 YUV files. The dis_yuv_stalls_removed folder allows you to do that for the videos having rebuffering. Extra care is needed when applying frame differencing on those videos (for VQA methods): make sure that the frame differences are applied on video frames with normal playback.
STRRED was computed on every two frames. PSNR_oss and PSNRhvs_oss: the “_oss” is only a naming convention to denote that these quality models were computed using the Netflix VMAF repository. PSNR _oss corresponds to the standard PSNR computation and PSNRhvs was implemented using the Daala codec.
