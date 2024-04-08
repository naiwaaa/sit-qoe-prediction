class DatasetInfo:
    lfovia = {
        "id": "lfovia",
        "name": "LFOVIA Video QoE Database",
        "data_range": {
            "duration": [0, 210],
            "strred": [0.0, 5000.0],
            # "strred": [0.0, 13040.0],
            "nr": [0, 10],
            "qoe": [0.0, 100.0],
        },
    }
    live_mobile_stall_2 = {
        "id": "live_mobile_stall_2",
        "name": "LIVE Mobile Stall Video Database-II",
        "data_range": {
            "duration": [0, 135],
            "strred": [None, None],
            "nr": [0, 7],
            "qoe": [0, 100],
        },
    }
    live_netflix = {
        "id": "live_netflix",
        "name": "LIVE Netflix Video QoE Database",
        "data_range": {
            "duration": [0, 2198],
            # "strred": [0.0, 4570.0],
            "strred": [0.0, 3140.0],
            "nr": [0, 2],
            "qoe": [-2.28, 1.53],
        },
    }
    live_netflix_2 = {
        "id": "live_netflix_2",
        "name": "LIVE-NFLX-II Subjective Video QoE Database",
        "data_range": {
            "duration": [0, 1069],
            "strred": [0.0, 4990],
            "nr": [0, 8],
            "qoe": [-1.98, 1.94],
        },
    }
