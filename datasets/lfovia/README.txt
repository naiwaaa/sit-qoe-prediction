Laboratory FOr Video And Image Analysis (LFOVIA)
Indian Institute of Technology Hyderabad (IITH), India

~~~~~~~~~~~~~~~~~~~~~~~~~
LFOVIA Video QoE Database
~~~~~~~~~~~~~~~~~~~~~~~~~

License and Copyright
~~~~~~~~~~~~~~~~~~~~~

1. The database is available for free. Please write to "sumohana@iith.ac.in" for password information.
2. Please cite the following paper if you use this database.

N. Eswara, M. K, A. Kommineni, S. Chakraborty, H. P. Sethuram, K. Kuchi, A. Kumar, S. S. Channappayya, “A Continuous QoE Evaluation Framework for Video Streaming over HTTP,” accepted for publication in IEEE Transactions on Circuits and Systems for Video Technology.

Database Description
~~~~~~~~~~~~~~~~~~~~

The LFOVIA QoE database consists of 54 videos at Full High Definition and Ultra High Definition resolutions along with continuous time subjective QoE scores and an overall QoE score for each of these videos. Out of 54 videos, 18 are reference videos that encompass a wide variety in content, from whom the remaining 36 test (or distorted) videos are derived. The distorted videos include various QoE influencing patterns that are caused by a combination of time-varying quality due of rate adaptation, and rebuffering events as typically encountered in video streaming.

For more details, please refer the paper mentioned in the License and Copyright section.

Details of the Database
~~~~~~~~~~~~~~~~~~~~~~~

The database provides the following:

(1) Reference Videos

The nomenclature for the reference videos is as follows.

"RVx_yz.mp4", where

x: Reference video no. (01-18)
y: 1080p (FHD) or 2160p (UHD). Indicates the video resolution.
z: Video frame rate

(2) Test Videos

The nomenclature for the test videos is as follows.

"TVx_z_rf_rds.mp4", where

x: Refers to the reference video no. from which the test video is derived
y: 1080p (FHD) or 2160p (UHD). Indicates the video resolution.
z: Video frame rate
rf: Rebuffering frequency
rd: Rebuffering duration (in seconds)

(3) QoE matfiles

In addition to videos, the database provides a set of attributes for each video. These attributes primarily contains the subjective QoE scores obtained through a subjective evaluation of all the videos in the database. The subjective scores for the QoE are in the range [0,100], with 0 being the worst and 100 the best. Further, the matfiles also provide 95% confidence interval bounds for the continuous QoE scores. Following are some of the key attributes that are common to both the reference and the test videos.

Reference and Test Videos
~~~~~~~~~~~~~~~~~~~~~~~~

(a) subjective_score_continuous: Continuous QoE scores for the video.
(b) subjective_score_continuous_CIhigh, subjective_score_continuous_CIlow: Upper and lower bounds of the 95% confidence interval for the continuous QoE scores, respectively.
(c) subjective_score_overall: Overall QoE score for the video.

Following are some of the key attributes of the test videos.

Test Videos
~~~~~~~~~~~

bitrate: Temporally varying video bitrate information in kbps.
rebuf_frame: Frame no in the reference video at which the rebuffering event occurs in the test video.
rebuf_position: Time (in seconds) with respect to the playback of the reference video at which the rebuffering event occurs in the test video. rebuf_position = rebuf_frame/fps.

Objective Evaluation
~~~~~~~~~~~~~~~~~~~~

The database also provides the results of objective evaluation of the test videos. A subset of QoE attributes for the test videos include QoE predicted scores computed using popular objective image/video quality assessment (I/VQA) metrics such as PSNR, SSIM, MS-SSIM, NIQE and STRRED. Since all of these I/VQA metrics do not account for the rebuffering events, we consider only the playback portion of the test videos for the objective evaluation. Following are the details of these attributes.

X_frame: Objective metric "X" evaluated on the test video at frame level.
X: Per second scores computed using objective metric "X" on the test video. Per second scores are computed by averaging frame level scores corresponding to 1 second.
qX: Predicted QoE scores using objective metric "X" after performing the logistic fit as desribed in the paper.

subjective_score_continuous_pb: Continuous QoE playback scores i.e., "subjective_score_continuous" with scores corresponding to the rebuffering event(s) excluded.
subjective_score_continuous_pb_CIhigh, subjective_score_continuous_pb_CIlow: Upper and lower bounds of the 95% confidence interval for the continuous QoE playback scores, respectively.

Note: Kindly note that the attributes "subjective_score_continuous_pb", "subjective_score_continuous_pb_CIhigh", "subjective_score_continuous_pb_CIlow" are not the ground truth subjective scores for the "playback only" test videos. These are simply the scores obtained by discarding the continuous scores that correspond to the rebuffering events.
