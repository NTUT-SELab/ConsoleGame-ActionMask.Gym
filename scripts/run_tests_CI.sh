#!/usr/bin/env bash

DOCKER_CMD="docker run --rm --network host --ipc=host --mount src=$(pwd),target=/root/code/env/,type=bind"
BASH_CMD="cd /root/code/env/"

if [[ ${DOCKER_IMAGE} = "" ]]; then
  echo "Need DOCKER_IMAGE environment variable to be set."
  exit 1
fi

set -e  # exit immediately on any error

${DOCKER_CMD} ${DOCKER_IMAGE} \
    bash -c "${BASH_CMD} && \
        pytest tests/ --cov-branch --cov-report html --cov-report xml --cov-report term --cov=. -v"

sudo python3 ./scripts/update_coverage_path.py
