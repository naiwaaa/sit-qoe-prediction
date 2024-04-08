#!/usr/bin/env zsh

SCRIPT_DIR="$( cd "$(dirname "$0")" ; pwd -P )"

H5_PATH="${SCRIPT_DIR}/../notebooks/saved_models"
PB_PATH="${SCRIPT_DIR}/../notebooks/mobile/model"

for filepath in "$H5_PATH"/*.h5; do
    filename=${filepath##*/}
    video_id=${${filename#*lfovia_}%_TV*}
    echo $filepath
    echo "$PB_PATH/model_${video_id}.pb"
    python "${SCRIPT_DIR}/keras_to_tensorflow/keras_to_tensorflow.py" \
        --input_model="$filepath" \
        --output_model="$PB_PATH/model_${video_id}.pb"
done
