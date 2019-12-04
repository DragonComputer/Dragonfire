#!/bin/bash

OPTS=`getopt \
-o n --long no-model \
-o d --long dev \
-o p --long pip \
-- "$@"`
if [ $? != 0 ] ; then echo "Failed parsing options." >&2 ; exit 1 ; fi
eval set -- "$OPTS"

NO_MODEL=false
DEV=false
PIP=false
while true; do
  case "$1" in
    -n | --no-model )
      NO_MODEL=true;
      shift
    ;;
    -d | --dev )
      DEV=true;
      shift
    ;;
    -p | --pip )
      PIP=true;
      shift
    ;;
    -- )
      shift;
      break
    ;;
    * )
      break
    ;;
  esac
done

apt-get update

if [ "$DEV" = true ] ; then
  apt-get -y install debhelper dpkg
fi
apt-get -y install python3 python3-all-dev libglib2.0-dev libcairo2-dev libgtk2.0-dev
apt-get -y install python3-minimal ${misc:Pre-Depends}
apt-get -y install ${python3:Depends} ${misc:Depends} flite python3-xlib portaudio19-dev python3-all-dev flac libnotify-bin python3-lxml python3-nltk python3-pyaudio python3-httplib2 python3-pip python3-setuptools python3-wheel libgstreamer1.0-dev gstreamer1.0-plugins-good gstreamer1.0-tools subversion libatlas-base-dev automake autoconf libtool libgtk2.0-0 gir1.2-gtk-3.0

if [ "$PIP" = true ] ; then
  pip3 install -e .
fi

#DEBHELPER#
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color
CHECKSUM="21198f6b6f24ef1f45082aebc6fd452e"
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
      wget -nc -O - https://github.com/mozilla/DeepSpeech/releases/download/v0.4.1/deepspeech-0.4.1-models.tar.gz | tar xvfz -
    fi
fi

DEEPCONV_DIR=/usr/share/dragonfire/deepconv
if [ ! -d "$DEEPCONV_DIR" ]; then
  mkdir $DEEPCONV_DIR
fi
cd $DEEPCONV_DIR
verified=$(find . -type f -exec md5sum {} \; | md5sum)
if [ ! ${verified::-3} = "$CHECKSUM2" ]; then
  wget -nc -O - https://github.com/DragonComputer/Dragonfire/releases/download/v1.0.4/deepconv-v3.tar.gz | tar xvfz -
fi

pip3 install --upgrade wikipedia==1.4.0 PyUserInput==0.1.11 tinydb==3.9.0.post1 youtube_dl spacy==2.1.3 pyowm==2.9.0 tensorflow==1.14.0 deepspeech==0.4.1 SpeechRecognition tweepy==3.7.0 metadata_parser==0.9.20 hug==2.4.0 hug-middleware-cors==1.0.0 waitress==1.1.0 requests>=2.20.0 pyjwt==1.6.4 SQLAlchemy\>=1.3.0 PyMySQL==0.8.1 msgpack==0.5.6 neuralcoref==4.0 deeppavlov==0.6.1

if [ "$DEV" = true ] ; then
  pip3 install --upgrade flake8 sphinx sphinx_rtd_theme recommonmark m2r pytest pytest-cov codecov
fi

python3 -m spacy download en
python3 -m deeppavlov install squad_bert

printf "import logging\nlogging.getLogger('tensorflow').setLevel(logging.ERROR)\nimport warnings\nwarnings.simplefilter(action='ignore', category=FutureWarning)\nfrom deeppavlov import build_model, configs\nmodel = build_model(configs.squad.squad, download=True)" | python3
pip3 install https://github.com/huggingface/neuralcoref-models/releases/download/en_coref_sm-3.0.0/en_coref_sm-3.0.0.tar.gz
printf "import nltk\nnltk.download('names')\nnltk.download('brown')\nnltk.download('wordnet')\nnltk.download('punkt')" | python3

echo -e "\n\n${GREEN}Dragonfire is successfully installed to your computer.${NC}\n"
