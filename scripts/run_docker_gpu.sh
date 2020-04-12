#!/bin/bash
# Launch an experiment using the docker gpu image
# https://github.com/NTUT-SELab/scripts/tree/master/stable-baselines

cmd_line="$@"

echo "Executing in the docker (gpu image):"
echo $cmd_line

docker run --gpus all -it --rm --network host --ipc=host \
 --mount src=${SB_PATH}/stable_baselines/,target=/root/code/stable_baselines/,type=bind \
 --mount src=$(pwd),target=/root/code/env/,type=bind \
  ntutselab/stable-baselines-gpu:latest \
  bash -c "cd /root/code/env/ && $cmd_line"
