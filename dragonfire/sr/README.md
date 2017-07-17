# SpeechRecognition

<p align="center">
	<img src="http://i.imgur.com/pp33AYX.png" alt="SpectrumAnalyzer"/>
</p>

<p align="center">
	<img src="http://i.imgur.com/gGsooR6.png" alt="Waveform"/>
</p>

### Install Dependencies

```
sudo apt-get -y install python-pyaudio python-scipy python-qt4 python-tk
pip install -r requirements.txt
```

### Usage

#### Create the training data

Create it using your microphone:

```
python __init__.py --create --audio 0
```

> To end your microphone session press `CTRL + C` (KeyboardInterrupt).

or create it using an audio file:

```
python __init__.py --create --audio ~/Downloads/audio_file.wav
```

You should repeat the words, `REPEAT_N_TIMES` times in consecutive manner like: For 3 for example; one, one, one, two, two, two, three, ... Same thing is valid for audio file option. At the end, it will ask for list of words that you need to enter from command-line. When it's finished, it will create one `.wav` file and one `.txt` inside `training_data/` directory.

:star2: This method is necessary because the program needs a perfectly aligned (word-by-word) training data.

#### Train your model

Just run the below command. It will automatically import all the data from `training_data/` directory:

```
python __init__.py --train
```

When it's finished, it will dump the model and word list as `model.npz` and `words.txt` into `out/` directory.

#### Test your model

Test it using your microphone:

```
python __init__.py --audio 0
```

or test it using an audio file:

```
python __init__.py --audio ~/Downloads/audio_file.wav
```

> This program is currently not performing good results.
