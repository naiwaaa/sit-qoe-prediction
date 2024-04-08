import numpy as np
from keras.preprocessing.sequence import pad_sequences

from sit_qoe.data import Dataset
from sit_qoe.utils import preprocess


UNK = -5.0


def generate_timeseries(
    data, data_info, normalize=True, split=None, split_method="more"
):
    """Generate timeseries from a Dataset or a list of Dataset.

    Parameters
    ----------
        data: VideoData, Dataset, List[Dataset]
            A Dataset or a list of Dataset
        maxlen: int
            Padding zeros
        normalize: bool
            Normalize data
        split: tuple
            Split sequence

    """
    if hasattr(data, "features"):
        return _generate([data], data_info, normalize, split, split_method)
    elif isinstance(data, Dataset):
        data.X, data.y = _generate(data, data_info, normalize, split, split_method)
    elif isinstance(data, list):
        [generate_timeseries(d, data_info, normalize, split) for d in data]
    else:
        raise TypeError("data must be Dataset or a list of Dataset")


def _generate(dataset, data_info, normalize, split, split_method="more"):
    X, y = [], []
    for video_data in dataset:
        features, target = (
            np.copy(video_data.features),
            np.copy(video_data.qoe_continuous).reshape((1, -1, 1)),
        )
        if normalize:
            features, target = _normalize(features, target, data_info)
        if split is None:
            features = pad_sequences(
                features,
                padding="pre",
                maxlen=data_info["data_range"]["duration"][1],
                dtype="float64",
                value=UNK,
            )
            target = pad_sequences(
                target,
                padding="pre",
                maxlen=data_info["data_range"]["duration"][1],
                dtype="float64",
                value=UNK,
            )
        else:
            pass

        if split_method == "more":
            features, target = _split_sequence(features, target, split)
        else:
            features, target = _split_sequence__(features, target, split)
        X.append(features)
        y.append(target)
    return np.vstack(X), np.vstack(y)


def _normalize(features, target, data_info):
    if features.shape[2] == 4:
        STSQ_idx, NR_idx = 0, 3
    elif features.shape[2] == 3:
        STSQ_idx, NR_idx = -1, 2

    if STSQ_idx >= 0:
        features[:, :, STSQ_idx] = preprocess.normalize(
            features[:, :, STSQ_idx], data_info["data_range"]["strred"]
        )
    features[:, :, NR_idx] = preprocess.normalize(
        features[:, :, NR_idx], data_info["data_range"]["nr"]
    )
    target = preprocess.normalize(target, data_info["data_range"]["qoe"])
    return features, target


def _split_sequence__(features, target, split):
    len_in_sec = features.shape[1]
    n_features = features.shape[2]
    features = features[:, : len_in_sec // split[0] * split[0], :].reshape(
        -1, split[0], n_features
    )
    target = target[:, : len_in_sec // split[0] * split[0], :].reshape(-1, split[0], 1)[
        :, -1:, :
    ]
    return features, target


def _split_sequence(features, target, split):
    X, y = [], []
    for i in range(features.shape[1]):
        end_idx = i + split[0]
        if end_idx > features.shape[1]:
            break
        seq_x, seq_y = (
            features[0, i:end_idx, :],
            target[0, (end_idx - split[1]) : end_idx, :],
        )
        X.append(seq_x)
        y.append(seq_y)
    return np.array(X), np.array(y)
