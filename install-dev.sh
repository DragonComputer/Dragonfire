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

apt-get update
apt-get -y install debhelper python3 python3-all-dev libglib2.0-dev libcairo2-dev libgtk2.0-dev && \
apt-get -y install dpkg python3-minimal ${misc:Pre-Depends} && \
apt-get -y install ${python3:Depends} ${misc:Depends} flite python3-xlib portaudio19-dev python3-all-dev flac libnotify-bin python3-lxml python3-nltk python3-pyaudio python3-httplib2 python3-pip python3-setuptools python3-wheel libgstreamer1.0-dev gstreamer1.0-plugins-good gstreamer1.0-tools subversion libatlas-base-dev automake autoconf libtool && \

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

DEEPCONV_DIR=/usr/share/dragonfire/deepconv
if [ ! -d "$DEEPCONV_DIR" ]; then
  mkdir $DEEPCONV_DIR
fi
cd $DEEPCONV_DIR
verified=$(find . -type f -exec md5sum {} \; | md5sum)
if [ ! ${verified::-3} = "$CHECKSUM2" ]; then
  wget -nc -O - https://github.com/DragonComputer/Dragonfire/releases/download/v0.9.9/deepconv-v2.tar.gz | tar xvfz -
fi

pip3 install --upgrade wikipedia==1.4.0 PyUserInput==0.1.11 tinydb==3.9.0.post1 youtube_dl spacy==2.0.11 pyowm==2.9.0 tensorflow==1.0.0 deepspeech==0.2.0a5 SpeechRecognition tweepy==3.6.0 metadata_parser==0.9.20 hug==2.4.0 hug-middleware-cors==1.0.0 waitress==1.1.0 requests==2.19.1 pyjwt==1.6.4 SQLAlchemy==1.2.10 PyMySQL==0.8.1 && \
pip3 install --upgrade flake8 sphinx sphinx_rtd_theme recommonmark m2r pytest && \
python3 -m spacy download en && \
pip3 install https://github.com/huggingface/neuralcoref-models/releases/download/en_coref_sm-3.0.0/en_coref_sm-3.0.0.tar.gz && \
printf "import nltk\nnltk.download('names')\nnltk.download('brown')\nnltk.download('wordnet')\nnltk.download('punkt')" | python3 && echo -e "\n\n${GREEN}Dragonfire is successfully installed to your computer.${NC}\n"
