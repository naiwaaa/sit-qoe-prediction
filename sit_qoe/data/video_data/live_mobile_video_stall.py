import numpy as np

from sit_qoe.data.video_data.base import VideoData
from sit_qoe.utils import cached_property


class MobileStallVideoData(VideoData):
    """LIVE Mobile Stall Video Database-II."""

    def __init__(self, subjective_data, metadata, video_idx):
        super().__init__()
        self.filename = metadata.vidNames[video_idx]

        self._qoe_continuous = subjective_data.continuousQoE_s[video_idx]
        self._qoe_continuous_CIhigh = subjective_data.continuousQoE_s_CIhigh[video_idx]
        self._qoe_continuous_CIlow = subjective_data.continuousQoE_s_CIlow[video_idx]
        self._qoe_overall = subjective_data.MOS_overall[video_idx]
        self._stall_waveforms = metadata.stallWaveforms_s[video_idx]

    @cached_property
    def len_in_sec(self):
        return self.qoe_continuous.shape[0]

    @cached_property
    def bitrate(self):
        bitrate = np.full(self.len_in_sec, 1, np.float)
        bitrate[self._stall_waveforms == 0] = 1
        bitrate[self._stall_waveforms == 100] = 0
        return bitrate

    # ========================================
    # QoE
    # ========================================
    @cached_property
    def qoe_continuous(self):
        return self._qoe_continuous

    @cached_property
    def qoe_continuous_CIhigh(self):
        return self._qoe_continuous_CIhigh

    @cached_property
    def qoe_continuous_CIlow(self):
        return self._qoe_continuous_CIlow

    @cached_property
    def qoe_overall(self):
        return self._qoe_overall

    # ========================================
    # Features
    # ========================================
    @cached_property
    def stsq_strred(self):
        raise AttributeError("property are not supported")

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
        nr[0] = 0 if self.bitrate[0] != 0 else 1 / 7
        for idx in range(1, self.len_in_sec):
            nr[idx] = nr[idx - 1] + (
                1 / 7 if self.bitrate[idx] == 0 and self.bitrate[idx - 1] != 0 else 0
            )
        return nr

    @cached_property
    def features(self):
        return np.dstack(
            [
                self.playback_indicator,
                self.time_elapsed_since_impairments,
                self.number_of_rebuff,
            ]
        )
