#!/bin/bash
# Launch an experiment using the docker cpu image
# https://github.com/NTUT-SELab/scripts/tree/master/stable-baselines

cmd_line="$@"

echo "Executing in the docker (cpu image):"
echo $cmd_line

if [[ -z ${TARGET_PORT} ]]; then
    TARGET_PORT=6006
fi

docker run -it --rm --network host --ipc=host --publish 6006:${TARGET_PORT} \
 --mount src=$(pwd),target=/root/code/env/,type=bind \
  tensorflow/tensorflow:1.14.0 \
  bash -c "cd /root/code/env/ && $cmd_line"
