#!/bin/bash
apt-get -y install python python-all-dev libglib2.0-dev libcairo2-dev libgtk2.0-dev python-wxgtk3.0 && \
apt-get -y install python2.7-minimal ${misc:Pre-Depends} && \
apt-get -y install ${python:Depends} ${misc:Depends} flite python-xlib portaudio19-dev python-all-dev flac libnotify-bin python-egenix-mx-base-dev python-lxml python-nltk python-pyaudio python-httplib2 python-pip python-wxgtk3.0 git libgstreamer1.0-dev gstreamer1.0-plugins-good gstreamer1.0-tools subversion libatlas-base-dev && \

cd dragonfire/sr/models/english/
wget https://github.com/DragonComputer/Dragonfire/releases/download/v0.9.6/sr_model_en.tar.gz
tar -xvf sr_model_en.tar.gz
rm sr_model_en.tar.gz
cd ../../tests/
wget https://github.com/DragonComputer/Dragonfire/releases/download/v0.9.6/sr_model_tests.tar.gz
tar -xvf sr_model_tests.tar.gz
rm sr_model_tests.tar.gz
cd ../../../

pip install .

#DEBHELPER#
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

KALDI_DIRECTORY=/usr/share/kaldi

AVAILABLE_CORES=$(getconf _NPROCESSORS_ONLN)
if ! [[ $AVAILABLE_CORES =~ ^-?[0-9]+$ ]] || ! [ $AVAILABLE_CORES -gt 0 ]; then
  AVAILABLE_CORES=1
fi
if [ $AVAILABLE_CORES -gt 1 ]; then
  AVAILABLE_CORES=$(expr $AVAILABLE_CORES - 1)
fi

if [ -d "$KALDI_DIRECTORY" ]; then
  rm -rf $KALDI_DIRECTORY
fi
mkdir $KALDI_DIRECTORY
cd $KALDI_DIRECTORY
git clone https://github.com/kaldi-asr/kaldi.git .

cd tools/
extras/check_dependencies.sh
make -j $AVAILABLE_CORES

cd ../
cd src/
./configure --shared
make depend -j $AVAILABLE_CORES
make -j $AVAILABLE_CORES

make ext -j $AVAILABLE_CORES
cd gst-plugin/
make depend -j $AVAILABLE_CORES
make -j $AVAILABLE_CORES

pip install wikipedia PyUserInput tinydb youtube_dl spacy pyowm && sudo pip install -U PyAudio && python -m spacy download en \
&& printf "import nltk\nnltk.download('names')\nnltk.download('brown')\nnltk.download('wordnet')" | python && echo -e "\n\n${GREEN}Dragonfire is successfully installed to your computer.${NC}\n"
