#!/bin/bash
OPTS=`getopt -o n --long no-model -- "$@"`
if [ $? != 0 ] ; then echo "Failed parsing options." >&2 ; exit 1 ; fi
eval set -- "$OPTS"

NO_MODEL=false
while true; do
  case "$1" in
    -n | --no-model ) NO_MODEL=true; shift ;;
    -- ) shift; break ;;
    * ) break ;;
  esac
done
NO_MODEL=$NO_MODEL

apt-get -y install debhelper python3 python3-all-dev libglib2.0-dev libcairo2-dev libgtk2.0-dev && \
apt-get -y install dpkg python3-minimal ${misc:Pre-Depends} && \
apt-get -y install ${python3:Depends} ${misc:Depends} flite python3-xlib portaudio19-dev python3-all-dev flac libnotify-bin python-egenix-mx-base-dev python3-lxml python3-nltk python3-pyaudio python3-httplib2 python3-pip libgstreamer1.0-dev gstreamer1.0-plugins-good gstreamer1.0-tools subversion libatlas-base-dev automake autoconf libtool && \

pip3 install -e .

#DEBHELPER#
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color
CHECKSUM="1449d83e0a0b834c033067bf62f06277"
CHECKSUM2="c775d819ffc06118053a48808003df84"

DRAGONFIRE_DIR=/usr/share/dragonfire
if [ ! -d "$DRAGONFIRE_DIR" ]; then
  mkdir $DRAGONFIRE_DIR
fi

DEEPSPEECH_DIR=/usr/share/dragonfire/deepspeech
if [ "$NO_MODEL" = false ] ; then
    if [ ! -d "$DEEPSPEECH_DIR" ]; then
      mkdir $DEEPSPEECH_DIR
    fi
    cd $DEEPSPEECH_DIR
    verified=$(md5sum models/* | md5sum)
    if [ ! ${verified::-3} = "$CHECKSUM" ]; then
      wget -nc -O - https://github.com/mozilla/DeepSpeech/releases/download/v0.1.1/deepspeech-0.1.1-models.tar.gz | tar xvfz -
    fi
fi

DEEPCONV_DIR=/usr/share/dragonfire/conversational
if [ ! -d "$DEEPCONV_DIR" ]; then
  mkdir $DEEPCONV_DIR
fi
cd $DEEPCONV_DIR
verified=$(find . -type f -exec md5sum {} \; | md5sum)
if [ ! ${verified::-3} = "$CHECKSUM2" ]; then
  wget -nc -O - https://github.com/DragonComputer/Dragonfire/releases/download/v0.9.9/deepconv-v2.tar.gz | tar xvfz -
fi

pip3 install wikipedia PyUserInput tinydb youtube_dl spacy pyowm tensorflow-gpu deepspeech-gpu tweepy metadata_parser && pip3 install -U PyAudio && python3 -m spacy download en \
&& printf "import nltk\nnltk.download('names')\nnltk.download('brown')\nnltk.download('wordnet')\nnltk.download('punkt')" | python3 && echo -e "\n\n${GREEN}Dragonfire is successfully installed to your computer.${NC}\n"
