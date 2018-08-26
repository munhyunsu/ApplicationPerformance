#!/bin/bash

docker rm scene_detector

docker run --rm \
  -u dnlab \
  -i \
  -t \
  --name scene_detector \
  ubuntu:dnlab
