#!/bin/bash
# Launch an experiment using the docker cpu image
# https://github.com/NTUT-SELab/scripts/tree/master/stable-baselines

cmd_line="$@"

SB_PATH="/mnt/c/Users/Mino/Downloads/VScode/stable-baselines"

echo "Executing in the docker (cpu image):"
echo $cmd_line
rm -rf ./tensorboard/*
docker run --rm -d --network host --name env --ipc=host \
 --mount src=${SB_PATH}/stable_baselines/,target=/root/code/stable_baselines/,type=bind \
 --mount src=$(pwd),target=/root/code/env/,type=bind \
  ntutselab/stable-baselines-cpu:latest \
  bash -c "cd /root/code/env/ && $cmd_line" 


if [[ -z ${TARGET_PORT} ]]; then
    TARGET_PORT=6006
fi

docker run --rm -d --network host --name tensorboard --ipc=host --publish 6006:${TARGET_PORT} \
 --mount src=$(pwd),target=/root/code/env/,type=bind \
  tensorflow/tensorflow:1.14.0 \
  bash -c "cd /root/code/env/ && tensorboard --logdir=./tensorboard --host=0.0.0.0"

echo "http://localhost:${TARGET_PORT}"