#!/bin/bash

docker rm scene_detector

docker run --rm \
  -u dnlab \
  -i \
  -t \
  ubuntu:dnlab \
  --name scene_detector \

