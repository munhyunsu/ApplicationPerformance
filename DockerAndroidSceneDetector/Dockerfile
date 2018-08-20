# Ubuntu docker file
# https://hub.docker.com/_/ubuntu/

# Pull base image of ubuntu
FROM ubuntu:latest

# Install default programs
RUN \
  apt-get update && \
  apt-get -y dist-upgrade && \
  apt-get install -y build-essential && \
  apt-get install -y vim && \
  rm -rf /var/lib/apt/lists/*

# Set default user
USER dnlab

# Set Working directory
WORKDIR /home/dnlab

# Default shell
CMD ["bash"]
