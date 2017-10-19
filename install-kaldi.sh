KALDI_DIRECTORY=/usr/share/kaldi

AVAILABLE_CORES=$(getconf _NPROCESSORS_ONLN)
if ! [[ $AVAILABLE_CORES =~ ^-?[0-9]+$ ]] || ! [ $AVAILABLE_CORES -gt 0 ]; then
  AVAILABLE_CORES=1
fi
if [ $AVAILABLE_CORES -gt 1 ]; then
  AVAILABLE_CORES=$(expr $AVAILABLE_CORES - 1)
fi

if [ ! -d "$KALDI_DIRECTORY" ]; then
  mkdir $KALDI_DIRECTORY
  cd $KALDI_DIRECTORY
  git clone https://github.com/kaldi-asr/kaldi.git .
else
  cd $KALDI_DIRECTORY
fi

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
