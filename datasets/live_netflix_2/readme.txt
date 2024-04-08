LABORATORY FOR IMAGE AND VIDEO ENGINEERING 
The University of Texas at Austin
-----------COPYRIGHT NOTICE STARTS WITH THIS LINE------------
Copyright (c) 2018 The University of Texas at Austin. All rights reserved. Permission is hereby granted, without written agreement and without license or royalty fees, to use, copy, modify, and distribute this database (the videos, the results and the source files) and its documentation for any purpose, provided that the copyright notice in its entirety appear in all copies of this database, and the original source of this database, Laboratory for Image and Video Engineering (LIVE, http://live.ece.utexas.edu) at the University of Texas at Austin (UT Austin, http://www.utexas.edu), is acknowledged in any publication that reports research using this database. The database is to be cited in the bibliography as:

Christos G. Bampis, Zhi Li, Ioannis Katsavounidis, Te-Yuan Huang, Chaitanya Ekanadham and Alan C. Bovik, "Towards Perceptually Optimized End-to-end Adaptive Video Streaming," submitted to IEEE Transactions on Image Processing

IN NO EVENT SHALL THE UNIVERSITY OF TEXAS AT AUSTIN BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT, SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE USE OF THIS DATABASE AND ITS DOCUMENTATION, EVEN IF THE UNIVERSITY OF TEXAS AT AUSTIN HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
THE UNIVERSITY OF TEXAS AT AUSTIN SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE. THE DATABASE PROVIDED HEREUNDER IS ON AN "AS IS" BASIS, AND THE UNIVERSITY OF TEXAS AT AUSTIN HAS NO OBLIGATION TO PROVIDE MAINTENANCE, SUPPORT, UPDATES, ENHANCEMENTS, OR MODIFICATIONS.
-----------COPYRIGHT NOTICE ENDS WITH THIS LINE------------

Please contact Christos Bampis (cbampis@gmail.com) if you have any questions.
The investigators on this research were:

Christos Bampis (cbampis@gmail.com) -- Netflix Inc., Department of ECE at UT Austin.
Alan C. Bovik (bovik@ece.utexas.edu) -- Department of ECE at UT Austin.
Zhi Li, Ioannis Katsavounidis, Te-Yuan Huang, Chaitanya Ekanadham -- Netflix Inc.
-------------------------------------------------------------------------

Details about the database:

This database contains continuous time and retrospective subjective scores collected on a large colllection of videos with an emphasis on adaptive video streaming applications. The database contains 15 YUV 420P video sequences (in the files contents_org_yuv_part_1.zip and contents_org_yuv_part_2.zip). These YUV videos can be used to extract features about the source sequences and compute video quality metrics.

Together with the source videos, there are 420 distorted video sequences in the zip files assets_mp4_part_1.zip and assets_mp4_part_2.zip. To keep the video size and the download times reasonable, we provide the mp4 files, so in case the YUV 420P files are required, you can decode them using ffmpeg.

Alongside the videos, we also provide metadata and subjective scores. These can be found in the file DtasetInformation.zip file, where there are both .mat files and .pkl files, one for each of the 420 distorted videos. For each .mat (or. pkl) file, you will find the following information inside:

adaptation_algorithm: the type of streaming adaptation algorithm used to generate this specific video. There are four different algorithms in total.

content_name: the name of the source video content

content_name_acronym: acronym for the content name, following the conventions in the paper

content_spatial_information: SI measure for the corresponding source video

content_temporal_information: TI measure for the corresponding source video

continuous_zscored_mos: the continuous subjective scores, after performing z-scoring per subject and then averaging over all subjects (that watched this particular video sequence)

cropping_parameters: ffmpeg-style cropping parameters in case of black bars (useful if you want to remove them for video quality calculations)

distorted_mp4_video: name of the distorted video sequence

frame_rate: the frame rate of the video sequence

width: the width of the video (display width)

height: the height of the video (display height)

is_rebuffered_bool: a vector with zeros and ones, denoting the presence of a rebuffered frame with 1, else with 0

PSNR: the per-frame PSNR scores calculated between the reference and distorted videos, after removing black bars and rebuffered frames

SSIM: the per-frame SSIM scores calculated between the reference and distorted videos, after removing black bars and rebuffered frames

MSSIM: the per-frame MS-SSIM scores calculated between the reference and distorted videos, after removing black bars and rebuffered frames

STRRED: the per-frame ST-RRED scores calculated between the reference and distorted videos, after removing black bars and rebuffered frames

VMAF: the per-frame VMAF scores calculated between the reference and distorted videos, after removing black bars and rebuffered frames

N_playback_frames: the number of frames where there was no rebuffering

N_rebuffer_frames: the number of frames where there was rebuffering

N_total_frames: the total number of framse (with and without rebuffering)

per_segment_encoding_width: the encoding width for each segment in the video sequence (before adding rebuffering events, if any)

per_segment_encoding_height: the encoding height for each segment in the video sequence (before adding rebuffering events, if any)

per_segment_encoding_QP: the QP value for each segment in the video sequence (excluding rebuffering)

playback_duration_sec: duration of the video excluding rebuffering

rebuffer_duration_sec: duration of all rebuffering events in the video sequence

video_duration_sec: the total duration of the video sequence (with and without rebuffering)

playout_bitrate: the bitrate for each frames belonging to a segment. If it is a rebuffering event, the bitrate is set to 0 for that frame

rebuffer_number: the number of rebuffering events in the video sequence

reference_yuv_video: the name of the corresponding source video (in YUV 420P format)

retrospective_zscored_mos: the retrospective subjective scores, after performing z-scoring per subject and then averaging over all subjects (that watched this particular video sequence)

scene_cuts: the frames that were selected as scene boundaries, with each pair defining a segment that was encoded at a specific resolution and QP value

scene_cuts_detected: the "actual" scene cuts. These are the places where the scene detection algorithm determined the existence of scene cut. These scene cuts are different from the ones we used in the scene_cuts variable, to enforce a maximum segment size (see paper).

throughput_trace_kbps: the corresponding network trace used to generate this video. There are seven different throughput traces overall.

throughput_trace_name: the name of the throughput trace. The naming convention is: means of transportation_start_end.

For any questions please contact cbampis@gmail.com.
