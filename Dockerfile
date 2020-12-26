# Use an official Python runtime as a parent image
FROM ubuntu:18.04
RUN rm /bin/sh && ln -s /bin/bash /bin/sh
ENV PYTHONUNBUFFERED 1 \
    PIP_NO_CACHE_DIR=off

ARG DEBIAN_FRONTEND=noninteractive

# Maintainer
LABEL maintainer="Mehmet Mert Yildiran mert.yildiran@boun.edu.tr"

# Update the apt index
RUN apt-get update
# Install git, make and wget
RUN apt-get install -y git make wget
# Install OpenSSL and libffi for Tensorflow
RUN apt-get -qqy install libssl-dev libffi-dev

# Set the working directory to /app
WORKDIR /app
# Copy the current directory contents into the container at /app
ADD . /app

# Install Dragonfire
RUN make dev-install
