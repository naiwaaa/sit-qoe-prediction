from typing import List, Type, Union
import re

import numpy as np
from sklearn.model_selection import train_test_split

from sit_qoe.data.video_data import VideoData
from sit_qoe.data import Dataset


class TrainTestValSplit(object):
    pass


class TimeSeriesSplit(object):
    pass


# ========================================
# TrainTestValSplit
# ========================================


class TrainTestValRatioSplit(TrainTestValSplit):
    """Split video data list in a ratio.

    Parameters
    ----------
    ratio: list of float (default=[0.8, 0.8])
    shuffle: bool (default=False)
    random_state: int (default=None)

    """

    def __init__(
        self,
        ratio: List[float] = [0.8, 0.8],
        shuffle: bool = False,
        random_state: int = None,
    ):
        super().__init__()

        if type(ratio) is list and (1 <= len(ratio) and len(ratio) <= 2):
            self.ratio = ratio
        else:
            raise ValueError("ratio has inappropriate value")
        self.shuffle = shuffle
        self.random_state = random_state

    def __call__(self, video_data_list: List[Type[VideoData]]):
        if len(self.ratio) == 1:
            first_subset, second_subset = train_test_split(
                video_data_list,
                train_size=self.ratio[0],
                shuffle=self.shuffle,
                random_state=self.random_state,
            )
            return Dataset(first_subset), Dataset(second_subset)
        else:
            first_second_subset, third_subset = train_test_split(
                video_data_list,
                train_size=self.ratio[0],
                shuffle=self.shuffle,
                random_state=self.random_state,
            )
            first_subset, second_subset = train_test_split(
                first_second_subset,
                train_size=self.ratio[1],
                shuffle=self.shuffle,
                random_state=self.random_state,
            )
            return Dataset(first_subset), Dataset(second_subset), Dataset(third_subset)


class TrainTestValRandomSplit(TrainTestValSplit):
    """Split live_mobile_stall_2 video data list.

    Parameters
    ----------
    random_state: int (default=None)

    """

    def __init__(self, random_state: int = None):
        super().__init__()

        self.random_state = random_state

    def __call__(self, video_data_list: List[Type[VideoData]]):
        train_test_sets = []
        for video_idx, video_data in enumerate(video_data_list):
            test_set = [video_data]
            mask = np.ones_like(video_data_list, dtype=bool)
            mask[video_idx] = 0
            train_set, val_set = train_test_split(
                video_data_list[mask], train_size=0.8, random_state=self.random_state
            )

            train_test_sets.append(
                [Dataset(train_set), Dataset(test_set), Dataset(val_set)]
            )

        return train_test_sets


class TrainTestValPatternSplit(TrainTestValSplit):
    """Split the dataset based on playout pattern of each video data.

    Parameters
    ----------
    dataset_name: str, {"live_netflix", "live_netflix_2", "lfovia"}

    """

    _SUPPORTED_DATASET = {"live_netflix": r"\d+", "lfovia": r"(?<=_)[\d.]+(?=_|s)"}

    def __init__(self, dataset_name: str):
        super().__init__()

        if dataset_name not in self._SUPPORTED_DATASET:
            raise ValueError(
                f"Dataset {dataset_name} not available. "
                + f"Available dataset: {list(self._SUPPORTED_DATASET.keys())}"
            )
        self.pattern = self._SUPPORTED_DATASET[dataset_name]

    def __call__(self, video_data_list: List[Type[VideoData]]):
        train_test_sets = []
        for video_data in video_data_list:
            test_set = [video_data]
            test_vid_idx = self._extract_idx(video_data)
            train_set = list(
                filter(
                    lambda vd: self._filter_train_set(test_vid_idx, vd), video_data_list
                )
            )
            val_set = list(
                filter(
                    lambda vd: self._filter_val_set(test_vid_idx, vd), video_data_list
                )
            )

            train_test_sets.append(
                [Dataset(train_set), Dataset(test_set), Dataset(val_set)]
            )

        return train_test_sets

    # "content_[content_index]_seq_[sequence_index]
    def _extract_idx(self, video_data):
        return re.findall(self.pattern, video_data.filename)

    def _filter_train_set(self, test_vid_idx, video_data):
        train_vid_idx = self._extract_idx(video_data)
        return (
            test_vid_idx[0] != train_vid_idx[0] and test_vid_idx[1] != train_vid_idx[1]
        )

    def _filter_val_set(self, test_vid_idx, video_data):
        val_vid_idx = self._extract_idx(video_data)
        return test_vid_idx != val_vid_idx and (
            test_vid_idx[0] == val_vid_idx[0] or test_vid_idx[1] == val_vid_idx[1]
        )


# ========================================
# TimeSeriesSplit
# ========================================


class TimeSeriesWindowSplit(TimeSeriesSplit):
    """Split the time series data.

    Parameters
    ----------
    window_size: int
    Length of output time series (in number of timesteps).
    stride: int
    Period between two windows.
    padding: str, {"pre", "post", "none"}
    Pad either before or after time series data.
    padding_value: int or float
    Padding value.
    choice: List[bool]
    The with each entry in window.

    """

    def __init__(
        self,
        window_size: int,
        stride: int,
        padding: str,
        padding_value: Union[int, float] = 0.0,
        choice: List[bool] = None,
    ):
        super().__init__()

        if padding not in ["pre", "right", "none"]:
            raise ValueError(
                f"`padding` argument must be one of 'left', 'right' or 'none'. "
                + f"Received: ${padding}"
            )

        self.window_size = window_size
        self.stride = stride
        self.padding = padding
        self.padding_value = padding_value

    def __call__(self, input: np.ndarray):
        timeseries_input = input
        if input.ndim == 1:
            timeseries_input = timeseries_input.reshape([1, -1, 1])
        if input.ndim == 2:
            timeseries_input = np.expand_dims(timeseries_input, axis=0)
        elif input.ndim != 3:
            raise ValueError("`input` argument has an inappropriate dimension.")

        if self.padding != "none":
            pass

        timeseries_input_length = timeseries_input.shape[1]
        samples = []
        for batch_idx in range(timeseries_input.shape[0]):
            for start_idx in range(0, timeseries_input_length, self.stride):
                end_idx = start_idx + self.window_size
                if end_idx > timeseries_input_length:
                    break
                samples.append(timeseries_input[batch_idx, start_idx:end_idx, :])

        return np.array(samples)


class TimeSeriesVariableSplit(TimeSeriesSplit):
    def __init__(self):
        super().__init__()

    def __call__(self, input):
        raise NotImplementedError
