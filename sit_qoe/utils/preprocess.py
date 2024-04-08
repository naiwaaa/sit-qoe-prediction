import numpy as np


def normalize(array, data_range):
    min = data_range[0]
    max = data_range[1]
    array = (array - min) / (max - min)
    array[array < min] = 0
    array[array > max] = 1
    return array


def scale(array, old_range, new_range):
    old_min, old_max = old_range
    new_min, new_max = new_range
    return (array - old_min) * (new_max - new_min) / (old_max - old_min) + new_min


def to_sec(array, video_data):
    if "fps" not in video_data.__dict__:
        raise ValueError("cannot get fps of video data")
    length = video_data.len_in_sec / video_data.fps
    sec = np.zeros(np.round(length).astype(np.int))

    for i in range(sec.shape[0]):
        start = i * video_data.fps
        end = (i + 1) * video_data.fps
        end = end if end < video_data.len_in_sec else video_data.len_in_sec
        sec[i] = array[start:end].mean()
    return sec
