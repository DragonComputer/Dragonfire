#!/bin/bash
apt-get -y install debhelper python3 python3-all-dev libglib2.0-dev libcairo2-dev libgtk2.0-dev && \
apt-get -y install dpkg python3-minimal ${misc:Pre-Depends} && \
apt-get -y install ${python3:Depends} ${misc:Depends} flite python3-xlib portaudio19-dev python3-all-dev flac libnotify-bin python-egenix-mx-base-dev python3-lxml python3-nltk python3-pyaudio python3-httplib2 python3-pip libgstreamer1.0-dev gstreamer1.0-plugins-good gstreamer1.0-tools subversion libatlas-base-dev automake autoconf libtool && \

pip3 install -e .

#DEBHELPER#
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

DEEPSPEECH_DIR=/usr/share/deepspeech

if [ ! -d "$DEEPSPEECH_DIR" ]; then
  mkdir $DEEPSPEECH_DIR
fi
if [ ! -d "${DEEPSPEECH_DIR}/models" ]; then
  cd $DEEPSPEECH_DIR
  wget -nc -O - https://github.com/mozilla/DeepSpeech/releases/download/v0.1.1/deepspeech-0.1.1-models.tar.gz | tar xvfz -
fi

pip3 install wikipedia PyUserInput tinydb youtube_dl spacy pyowm tensorflow-gpu deepspeech-gpu && pip3 install -U PyAudio && python3 -m spacy download en \
&& printf "import nltk\nnltk.download('names')\nnltk.download('brown')\nnltk.download('wordnet')" | python3 && echo -e "\n\n${GREEN}Dragonfire is successfully installed to your computer.${NC}\n"
