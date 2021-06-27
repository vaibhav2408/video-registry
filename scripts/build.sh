#!/bin/bash -x

#
# Build a docker image of the application.
#

IMAGE=${1:-"fampay:development"}
docker build \
    --tag "${IMAGE}" \
    --file docker/Dockerfile \
    .
