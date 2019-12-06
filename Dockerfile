# Use an official Python runtime as a parent image
FROM ubuntu:18.04
RUN rm /bin/sh && ln -s /bin/bash /bin/sh
ENV PYTHONUNBUFFERED 1
ARG DEBIAN_FRONTEND=noninteractive

# Maintainer
LABEL maintainer="Mehmet Mert Yıldıran mert.yildiran@boun.edu.tr"

# Update the apt index
RUN apt update
# Install git and make
RUN apt install -y git make
# Install OpenSSL and libffi for Tensorflow
RUN apt -qqy install libssl-dev libffi-dev

# Set the working directory to /app
WORKDIR /app
# Copy the current directory contents into the container at /app
ADD . /app

# Install Dragonfire
RUN make dev-install
