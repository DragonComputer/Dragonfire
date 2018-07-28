# Use an official Python runtime as a parent image
FROM ubuntu:16.04
RUN rm /bin/sh && ln -s /bin/bash /bin/sh
ENV PYTHONUNBUFFERED 1

# Maintainer
MAINTAINER Mehmet Mert Yıldıran "mert.yildiran@bil.omu.edu.tr"

# Install all APT dependencies
RUN apt-get update
RUN apt-get -qqy install python3 python3-all-dev libglib2.0-dev libcairo2-dev libgtk2.0-dev
RUN apt-get -qqy install python3-minimal ${misc:Pre-Depends}
RUN apt-get -qqy install ${python3:Depends} ${misc:Depends} flite python3-xlib portaudio19-dev python3-all-dev flac libnotify-bin python-egenix-mx-base-dev python3-lxml python3-nltk python3-pyaudio python3-httplib2 python3-pip libgstreamer1.0-dev gstreamer1.0-plugins-good gstreamer1.0-tools subversion libatlas-base-dev automake autoconf libtool

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install pip3
RUN apt-get install -y python3-pip

# Install Dragonfire Python package
RUN pip3 install .

# Define environment variables
ENV DRAGONFIRE_DIR /usr/share/dragonfire
ENV DEEPCONV_DIR /usr/share/dragonfire/conversational

# Create the necessary directories for the Tensorflow models
RUN mkdir $DRAGONFIRE_DIR
RUN mkdir $DEEPCONV_DIR

# Download the DeepConversation Tensorflow model
ADD https://github.com/DragonComputer/Dragonfire/releases/download/v0.9.9/deepconv-v2.tar.gz $DEEPCONV_DIR
RUN cd $DEEPCONV_DIR && tar xvfz deepconv-v2.tar.gz

# Install OpenSSL and libffi for Tensorflow
RUN apt-get -qqy install libssl-dev libffi-dev

# Retry to install the Python package dependencies in case of a failure
RUN pip3 install --upgrade PyAudio wikipedia PyUserInput tinydb youtube_dl spacy pyowm tensorflow==1.0.0 deepspeech==0.2.0a5 SpeechRecognition tweepy metadata_parser hug hug-middleware-cors waitress PyMySQL requests==2.18.4

# Download the spaCy English model
RUN python3 -m spacy download en

# Download the necessary NLTK models
RUN printf "import nltk\nnltk.download('names')\nnltk.download('brown')\nnltk.download('wordnet')\nnltk.download('punkt')" | python3

# Print success message
RUN echo -e "\n\nDragonfire is successfully installed into the container.\n"

# Make port 3031 available to the world outside this container
EXPOSE 3031

# Start Dragonfire
ENTRYPOINT ["dragonfire"]

# Default arguments
CMD ["--server", "API_KEY"]
