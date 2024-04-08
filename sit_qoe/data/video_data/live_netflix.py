from pathlib import Path

import numpy as np
import scipy.io as sio

from sit_qoe.data.video_data.base import VideoData
from sit_qoe.utils import cached_property


class NetflixVideoData(VideoData):
    """LIVE Netflix Video Quality of Experience Database."""

    def __init__(self, mat_file_path, metadata):
        super().__init__()
        self.mat = sio.loadmat(mat_file_path, squeeze_me=True)
        self.filename = Path(mat_file_path).stem

        self.fps = self.mat["vid_fps"]
        self._n_frames = self.mat["Nframes"]
        self._birate_lt_250 = metadata[0]
        self._rebuff_idx = metadata[1]

    @cached_property
    def len_in_sec(self):
        # return self.mat["Nframes"]
        return self.mat["continuous_subj_score_avg1sec"].shape[0]

    @cached_property
    def bitrate(self):
        # bitrate = np.full(self.len_in_sec, 1, np.float)
        # bitrate[self._rebuff_idx - 1] = 0
        # bitrate[self._birate_lt_250 - 1] = 0.5
        # return bitrate
        return self.mat["bitrate_levels_avg1sec"]

    # ========================================
    # QoE
    # ========================================
    @cached_property
    def qoe_continuous(self):
        # return self.mat["continuous_subj_score"]
        return self.mat["continuous_subj_score_avg1sec"]

    @cached_property
    def qoe_overall(self):
        return self.mat["final_subj_score"]

    # ========================================
    # Features
    # ========================================
    @cached_property
    def stsq_strred(self):
        # strred = np.full(self.len_in_sec, 0, np.float)
        # j = 0
        # for idx in range(0, self.len_in_sec):
        #     if self.bitrate[idx] == 0:
        #         strred[idx] = strred[idx - 1]
        #     else:
        #         # strred[idx] = self.mat["STRRED_vec"][j]
        #         j += 1

        strred = self.mat["STRRED_vec_avg1sec_with_rebuf"]
        return strred

    @cached_property
    def playback_indicator(self):
        pi = np.full(self.len_in_sec, 0, np.float)
        pi[self.bitrate == 0] = 1
        return pi

    @cached_property
    def time_elapsed_since_rebuff(self):
        tr = np.full(self.len_in_sec, 0, np.float)
        for idx in range(1, self.len_in_sec):
            if self.bitrate[idx] == 0:
                tr[idx] = 0
            else:
                tr[idx] = tr[idx - 1] + 1 / self.len_in_sec
        return tr

    @cached_property
    def time_elapsed_since_impairments(self):
        tr = np.full(self.len_in_sec, 0, np.float)
        for idx in range(1, self.len_in_sec):
            if self.bitrate[idx] == 0 or self.bitrate[idx] < self.bitrate[idx - 1]:
                tr[idx] = 0
            else:
                tr[idx] = tr[idx - 1] + 1 / self.len_in_sec
        return tr

    @cached_property
    def number_of_rebuff(self):
        nr = np.full(self.len_in_sec, 0, np.float)
        nr[0] = 0 if self.bitrate[0] != 0 else 1 / 2
        for idx in range(1, self.len_in_sec):
            nr[idx] = nr[idx - 1] + (
                1 / 2 if self.bitrate[idx] == 0 and self.bitrate[idx - 1] != 0 else 0
            )
        return nr
