#!/bin/bash
# Launch an experiment using the docker cpu image
# https://github.com/NTUT-SELab/scripts/tree/master/stable-baselines

cmd_line="$@"

SB_PATH="/mnt/c/Users/Mino/Downloads/VScode/stable-baselines"

echo "Executing in the docker (cpu image):"
echo $cmd_line
rm -rf ./tensorboard/*
docker run --rm -ti --network host --name env --ipc=host \
 --mount src=${SB_PATH}/stable_baselines/,target=/root/code/stable_baselines/,type=bind \
 --mount src=$(pwd),target=/root/code/env/,type=bind \
  ntutselab/stable-baselines-cpu:latest \
  bash -c "cd /root/code/env/ && $cmd_line" 
