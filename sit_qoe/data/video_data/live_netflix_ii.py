from pathlib import Path

import numpy as np
import scipy.io as sio

from sit_qoe.data.video_data.base import VideoData
from sit_qoe.utils import cached_property


class NetflixIIVideoData(VideoData):
    """LIVE-NFLX-II Subjective Video QoE Database."""

    def __init__(self, mat_file_path):
        super().__init__()
        self.mat = sio.loadmat(mat_file_path, squeeze_me=True)
        self.filename = Path(mat_file_path).stem

        self._fps = self.mat["frame_rate"]
        self._n_frames = self.mat["N_total_frames"]

    @cached_property
    def len_in_sec(self):
        return self.mat["N_total_frames"]

    @cached_property
    def bitrate(self):
        return self.mat["playout_bitrate"]

    # ========================================
    # QoE
    # ========================================
    @cached_property
    def qoe_continuous(self):
        return self.mat["continuous_zscored_mos"]

    @cached_property
    def qoe_overall(self):
        return self.mat["retrospective_zscored_mos"]

    # ========================================
    # Features
    # ========================================
    @cached_property
    def stsq_strred(self):
        strred = np.full(self.len_in_sec, 0, np.float)
        j = 0
        for idx in range(0, self.len_in_sec):
            if self.bitrate[idx] == 0:
                strred[idx] = strred[idx - 1]
            else:
                strred[idx] = self.mat["STRRED"][j]
                j += 1
        return strred

    @cached_property
    def playback_indicator(self):
        pi = np.full(self.len_in_sec, 0, np.float)
        pi[self.bitrate == 0] = 1
        assert (pi == self.mat["is_rebuffered_bool"]).all(), "pi != is_rebuffered_bool"
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
        nr[0] = 0 if self.bitrate[0] != 0 else 1 / 8
        for idx in range(1, self.len_in_sec):
            nr[idx] = nr[idx - 1] + (
                1 / 8 if self.bitrate[idx] == 0 and self.bitrate[idx - 1] != 0 else 0
            )
        return nr
