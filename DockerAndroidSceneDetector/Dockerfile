# Ubuntu docker file
# https://hub.docker.com/_/ubuntu/

# Pull base image of ubuntu
FROM ubuntu:latest

# Install default programs
RUN \
  useradd --create-home \
    --home-dir /home/dnlab \
    --shell /bin/bash \
    --groups sudo \
    --password dnlab \
    dnlab && \
  sed -i 's/^#force_color_prompt=yes/force_color_prompt=yes/' /home/dnlab/.bashrc && \
  apt-get update && \
  apt-get install -y apt-utils && \
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
