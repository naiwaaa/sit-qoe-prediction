import numpy as np

from sit_qoe.utils import cached_property


class VideoData(object):
    """An abstract class representing playback and user data during a video streaming session.

    All other video data should subclass it. All property should be in seconds.
    """

    def __init__(self):
        self._mat = None
        self._doi = None

    @property
    def mat(self):
        if self._mat is None:
            raise AttributeError("cannot get property before being initialized")
        return self._mat

    @mat.setter
    def mat(self, value):
        self._mat = value

    @cached_property
    def len_in_sec(self):
        raise NotImplementedError

    @cached_property
    def bitrate(self):
        raise NotImplementedError

    # ========================================
    # QoE
    # ========================================
    @cached_property
    def qoe_continuous(self):
        raise NotImplementedError

    @cached_property
    def qoe_continuous_CIhigh(self):
        raise NotImplementedError

    @cached_property
    def qoe_continuous_CIlow(self):
        raise NotImplementedError

    @cached_property
    def qoe_overall(self):
        raise NotImplementedError

    # ========================================
    # Features
    # ========================================
    @cached_property
    def stsq_strred(self):
        raise NotImplementedError

    @cached_property
    def playback_indicator(self):
        raise NotImplementedError

    @cached_property
    def time_elapsed_since_rebuff(self):
        raise NotImplementedError

    @cached_property
    def time_elapsed_since_impairments(self):
        raise NotImplementedError

    @cached_property
    def number_of_rebuff(self):
        raise NotImplementedError

    @property
    def degree_of_liking(self):
        if self._doi is None:
            raise AttributeError("cannot get property before being initialized")
        return self._doi

    @degree_of_liking.setter
    def degree_of_liking(self, value):
        self._doi = value

    @cached_property
    def features(self):
        return np.dstack(
            [
                self.stsq_strred,
                self.playback_indicator,
                self.time_elapsed_since_impairments,
                self.number_of_rebuff,
            ]
        )

    # ========================================
    # Methods
    # ========================================

    # ========================================
    # Private
    # ========================================

    # @cached_property
    # def _number_of_bitrate_switching(self):
    #     nb = np.full(self.len_in_sec, 0, np.float)
    #     previous_bitrate_value = self.bitrate[0]
    #     for idx in range(1, self.len_in_sec):
    #         if self.bitrate[idx] == 0 or self.bitrate[idx] == previous_bitrate_value:
    #             nb[idx] = nb[idx - 1]
    #             continue
    #         nb[idx] = nb[idx - 1] + 1
    #         previous_bitrate_value = self.bitrate[idx]
    #     return nb

    # @cached_property
    # def _time_varying_rebuff_length(self):
    #     rebuff_length = np.full(self.len_in_sec, 0, np.float)
    #     rebuff_length[0] = 0 if self.bitrate[0] != 0 else 1
    #     for idx in range(1, self.len_in_sec):
    #         rebuff_length[idx] = (
    #             0 if self.bitrate[idx] != 0 else rebuff_length[idx - 1] + 1
    #         )
    #     return rebuff_length

    # def _generate_time_series(self):
    #     f = []
    #     inp = []
    #     out = []
    #     for i in range(0, self.len_in_sec):
    #         f.append(
    #             [
    #                 self.stsq_strred[i],
    #                 self.pi[i],
    #                 self.tr_drop[i],
    #                 self.time_varying_n_rebuff_occurred[i],
    #             ]
    #         )
    #         inp.append(f[:])
    #         out.append([self.qoe_continuous[i]])

    #     inp = pad_sequences(inp, padding="post", maxlen=220, dtype="float64")
    #     return inp, out
