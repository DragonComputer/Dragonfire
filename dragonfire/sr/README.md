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

Test it using your microphone:

```
python __init__.py --audio 0
```

Test it using an audio file:

```
python __init__.py --audio ~/Downloads/audio_file.wav
```

> This program is currently nothing more than a visualizer.
