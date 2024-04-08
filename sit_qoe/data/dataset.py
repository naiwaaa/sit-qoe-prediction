import numpy as np


class Dataset(object):
    def __init__(self, video_data_list):
        if not isinstance(video_data_list, (list, np.ndarray)):
            raise Exception("`video_data_list` must be a list or numpy array")
        self.video_data_list = np.asarray(video_data_list)
        self.X = None
        self.y = None
        self.y_CIhigh = None
        self.y_CIlow = None

    def __len__(self):
        return len(self.video_data_list)

    def __getitem__(self, idx):
        return self.video_data_list[idx]

    def __getattribute__(self, attr):
        if attr in ("X", "y") and super().__getattribute__(attr) is None:
            raise AttributeError(
                f"cannot get property `{attr}` before calling `generate_timeseries`"
            )
        return super().__getattribute__(attr)

    def __str__(self):
        try:
            if self.X is not None and self.y is not None:
                return f"X shape: {self.X.shape}\n" + f"y shape: {self.y.shape}"
        except Exception:
            return super().__str__()

    def map(self, f):
        return list(map(f, self.video_data_list))

    def filter(self, f):
        return Dataset(list(filter(f, self.video_data_list)))
