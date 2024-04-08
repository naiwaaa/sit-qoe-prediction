from pathlib import Path

import numpy as np
import scipy.io as sio

from sit_qoe.data.video_data import (
    NetflixVideoData,
    NetflixIIVideoData,
    LfoviaVideoData,
    MobileStallVideoData,
)
from sit_qoe.data import Dataset, DatasetInfo


_SUPPORTED_DATASET = {
    "lfovia": lambda path: _load_lfovia(path),
    "live_mobile_stall_2": lambda path: _load_live_mobile_stall_2(path),
    "live_netflix": lambda path: _load_live_netflix(path),
    "live_netflix_2": lambda path: _load_live_netflix_2(path),
}

_DATASET_FOLDER = Path(__file__).parent.joinpath("../../datasets").absolute()


def list_datasets():
    return list(_SUPPORTED_DATASET.keys())


def load(name=None, split=None, preprocess=None, with_info=False):
    """Load the named dataset into a `sit_qoe.data.Dataset`.

    Parameters
    ----------
    name: str
    split: `sit_qoe.data.Split`
    with_info: bool

    """
    if name not in _SUPPORTED_DATASET:
        raise ValueError(
            f"Dataset {name} not found. Available datasets: {list_datasets()}"
        )
    try:
        dataset_path = Path(_DATASET_FOLDER) / name
        video_data_list = np.asarray(_SUPPORTED_DATASET[name](dataset_path))
        dataset = Dataset(video_data_list) if split is None else split(video_data_list)
        if with_info:
            return dataset, getattr(DatasetInfo, name)
        else:
            return dataset
    except Exception:
        print(f"Failed to load dataset {name}")
        raise


def _load_lfovia(lfovia_path):
    video_data_list = []
    mat_file_path_list = sorted((lfovia_path / "mat_files").glob("TV*.mat"))

    for mat_file_path in mat_file_path_list:
        video_data_list.append(LfoviaVideoData(mat_file_path))

    return video_data_list


def _load_live_mobile_stall_2(live_mobile_stall_path):
    video_data_list = []
    mat_subjective_data = sio.loadmat(
        live_mobile_stall_path / "subjectiveData.mat",
        squeeze_me=True,
        struct_as_record=False,
    )["liveMobileStall_subjectiveData"]
    mat_metadata = sio.loadmat(
        live_mobile_stall_path / "videoMetaData.mat",
        squeeze_me=True,
        struct_as_record=False,
    )["liveMobileStall_videoMetaData"]

    for idx in range(0, mat_subjective_data.continuousQoE_s.shape[0]):
        video_data_list.append(
            MobileStallVideoData(mat_subjective_data, mat_metadata, idx)
        )

    return video_data_list


def _load_live_netflix(live_netflix_path):
    video_data_list = []

    mat_metadata_file_path = live_netflix_path / "LIVE_NFLX_Network_Impairments.mat"
    mat_metadata = sio.loadmat(mat_metadata_file_path)["LIVE_NFLX_Network_Impairments"]

    mat_videodata_file_path_list = sorted(
        (live_netflix_path / "mat_files").glob("*.mat")
    )

    for mat_videodata_file_path in mat_videodata_file_path_list:
        # Each `mat` file have the following naming convention:
        # `content_<content_idx>_seq_<seq_idx>.mat`
        # The following code extract `content_idx` and `seq_idx` from mat filename
        # and compute its index in the `mat_metadata` array.
        filename_parts = mat_videodata_file_path.stem.split("_")
        content_idx = int(filename_parts[1])
        seq_idx = int(filename_parts[3])
        metadata_idx = (content_idx - 1) * 8 + seq_idx
        video_data_list.append(
            NetflixVideoData(mat_videodata_file_path, mat_metadata[metadata_idx][1:])
        )

    return video_data_list


def _load_live_netflix_2(live_netflix_2_path):
    video_data_list = []
    mat_file_path_list = sorted((live_netflix_2_path / "mat_files").glob("*.mat"))

    for mat_file_path in mat_file_path_list:
        video_data_list.append(NetflixIIVideoData(mat_file_path))

    return video_data_list
