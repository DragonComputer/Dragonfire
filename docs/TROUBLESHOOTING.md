## Troubleshooting

#### No sound is coming out of my computer?

If there is no sound coming from your speakers when you see `Dragonfire: GOOD MORNING SIR` on your terminal or *To activate say 'Dragonfire!' or 'Wake Up!'* notification after you run Dragonfire with `dragonfire` command then there are two possibilities causing this problem:

1. Dragonfire's audio output (ALSA plug-in [flite]: ALSA Playback) could be mapped to wrong audio device:

![](https://i.imgur.com/mOie7G6.png)

you can fix this either by changing it to correct device using the audio settings of your operating system or you can choose to use Phonon `sudo apt-get install phonon` to configure your device priority:

![](http://i.imgur.com/tALl6UG.png)

2. The problem could be related to missing `flite` package on your system. It should normally be installed on post-installation automatically but try to re-install it one more time with:

```
sudo apt-get update
sudo apt-get install flite
```

If `flite` is missing in your distro's repositories then [download](https://packages.ubuntu.com/xenial/amd64/flite/download) it and try to install it with `sudo dpkg -i flite_2.0.0-release-1_amd64.deb`.

#### Dragonfire is not reacting to my voice?

 - Since we migrated to [Kaldi Speech Recognition Toolkit](https://github.com/kaldi-asr/kaldi), Dragonfire's speech recognition procedure runs fully on local.
 - First of all, please make sure that Kaldi is compiled and installed under `/usr/share/kaldi` directory. If you suspect that Kaldi's compilation failed on installation procedure then please clone the repository `git clone https://github.com/DragonComputer/Dragonfire.git`and run [install.sh](https://github.com/DragonComputer/Dragonfire/blob/master/install.sh) script with either `sudo ./install.sh` or `sudo bash install.sh`. Make sure that [this block](https://github.com/DragonComputer/Dragonfire/blob/master/install.sh#L23-L53) runs without any problem because it clones Kaldi under `/usr/share/kaldi` and compiles it directory by directory.
 - If you are sure that Kaldi installation is OK then first run `export GST_PLUGIN_PATH=/usr/share/kaldi/src/gst-plugin` after that run [decoder_test.py](https://github.com/DragonComputer/Dragonfire/blob/master/dragonfire/sr/decoder_test.py) (`python decoder_test.py`) to test the speech recognition. It will run two tests:
   1. Microphone test so you will speak and it will recognize the speech.
   2. Audio file(located under `tests/ten_digits.wav`) test. The output should look like this:

```
INFO:decoder:recognize: Pushing EOS to pipeline
INFO:decoder:recognize: Got word: DRAGON
INFO:decoder:recognize: Got word: FIRE
INFO:decoder:recognize: Got word: <#s>
INFO:decoder:recognize: Pipeline received eos signal
INFO:decoder:recognize: Finishing request
['DRAGON', 'FIRE', '<#s>']
.INFO:decoder:testWav: Pipeline initialized
INFO:decoder:testWav: Connecting audio decoder
INFO:decoder:testWav: Connected audio decoder
INFO:decoder:testWav: Pushing EOS to pipeline
INFO:decoder:testWav: Got word: ONE
INFO:decoder:testWav: Got word: TWO
INFO:decoder:testWav: Got word: THREE
INFO:decoder:testWav: Got word: FOUR
INFO:decoder:testWav: Got word: FIVE
INFO:decoder:testWav: Got word: SIX
INFO:decoder:testWav: Got word: SEVEN
INFO:decoder:testWav: Got word: EIGHT
INFO:decoder:testWav: Got word: <#s>
INFO:decoder:testWav: Pipeline received eos signal
INFO:decoder:testWav: Finishing request
.
----------------------------------------------------------------------
Ran 2 tests in 23.039s

OK
```

 - If you face with a problem in above test then most probably Dragonfire's audio input (ALSA plug-in [python]: ALSA Capture) is mapped to wrong audio device:

![](https://i.imgur.com/8YJMery.png)

you can fix this either by changing it to correct device using the audio settings of your operating system or you can choose to use Phonon `sudo apt-get install phonon` to configure your device priority:

![](http://i.imgur.com/9b8ttnP.png)

#### I got AttributeError: 'NoneType' object has no attribute 'set_property'?

```
File "/usr/bin/dragonfire", line 11, in <module>
  load_entry_point('dragonfire', 'console_scripts', 'dragonfire')()
File "/home/tardog/Dokumente/Spielweise/Dragonfire/dragonfire/__init__.py", line 544, in initiate
  start(args)
File "/home/tardog/Dokumente/Spielweise/Dragonfire/dragonfire/__init__.py", line 60, in start
  recognizer = KaldiRecognizer()
File "/home/tardog/Dokumente/Spielweise/Dragonfire/dragonfire/sr/kaldi.py", line 34, in __init__
  self.decoder_pipeline = DecoderPipeline({"decoder" : decoder_conf})
File "/home/tardog/Dokumente/Spielweise/Dragonfire/dragonfire/sr/decoder.py", line 17, in __init__
  self.create_pipeline(conf)
File "/home/tardog/Dokumente/Spielweise/Dragonfire/dragonfire/sr/decoder.py", line 47, in create_pipeline
  self.asr.set_property(key, val)
AttributeError: 'NoneType' object has no attribute 'set_property'
```

If you got the above error then;
 - either Kaldi installation has a problem so follow the instructions in **Dragonfire is not reacting to my voice?**
 - or Kaldi installation is OK but somehow [this line](https://github.com/DragonComputer/Dragonfire/blob/78adeedf7a278bcb26786130c0c6dd46d914fc95/dragonfire/__init__.py#L65) is not working so run `export GST_PLUGIN_PATH=/usr/share/kaldi/src/gst-plugin` before launching Dragonfire (in the same shell).

#### Dragonfire is understanding my commands but doing nothing?

Dragonfire starts on sleeping mode to do not disturb your acoustic environment. You need to activate her by saying *DRAGONFIRE* or *HEY* or *WAKE UP* to your microphone.

#### Dragonfire is unnecessarily jumping into real world conversation of mine?

Then you need to deactivate her by saying *GO TO SLEEP*.

#### Dragonfire confusing with her own voice?

Simply use your headphones:headphones: instead of the speakers:speaker: to listen Dragonfire or lower the volume of your speakers:speaker:.

#### Dragonfire started to read something but I don't know how to stop her?

Then you need to silence her by saying *ENOUGH* OR *SHUT UP*.

#### I'm done with Dragonfire, how can I shut her down?

By saying *GOODBYE* or *BYE BYE* or *SEE YOU LATER*.

#### I'm not seeing any 3D female head model(avatar) on the screen?

If you did not run Dragonfire with `--headless` option then you should be able to see the below avatar every time you hear a text-to-speech output.

![](https://github.com/DragonComputer/Dragonfire/raw/master/dragonfire/realhud/animation/avatar.gif)

Although, our [C program](https://github.com/DragonComputer/Dragonfire/blob/master/dragonfire/realhud/realhud.c) that runs the avatar animation has not the best compatibility across the different desktop environments or window managers. For example; in Unity desktop environment, it flashes badly but in KDE Plasma 5, it runs pretty smooth.

#### Dragonfire calls me "Lady" but I'm a man?

Dragonfire analyzes your name that registered on the operating system to determine your gender. Sometimes she makes mistakes (mostly if your name is not an English name) and call you by your opposite gender. To fix this you can say *MY TITLE IS SIR* or *I'M A MAN* or *I'M A BOY*.

#### Dragonfire calls me "Sir" but I'm a woman?

Dragonfire analyzes your name that registered on the operating system to determine your gender. Sometimes she makes mistakes (mostly if your name is not an English name) and call you by your opposite gender. To fix this you can say *MY TITLE IS LADY* or *I'M A LADY* or *I'M A WOMAN* or *I'M A GIRL*.

#### I want to be called as something different?

Sure, there is a command for that. You can use `CALL ME *` command to manipulate her form of address for you to anything you want. For example: *CALL ME MASTER* or *CALL ME MY LORD* or *CALL ME MY FRIEND* etc.

#### I'm saying FILE MANAGER but file manager is not opening?

Probably you don't have any of the supported file manager software packages: `dolphin`, `pantheon-files`, `nautilus`

#### I'm saying WEB BROWSER but web browser is not opening?

Check the existence of `sensible-browser` command. It's a command that points out to your default web browser.

#### I'm saying PHOTO EDITOR but no software is opening?

Probably you don't have [GIMP](https://www.gimp.org/) installed on your system: `sudo apt-get install gimp`

#### I'm saying INKSCAPE but Inskcape is not opening?

Probably you don't have [Inkscape](https://inkscape.org/en/) installed on your system: `sudo apt-get install inkscape`

#### I'm saying VIDEO EDITOR but no software is opening?

Probably you don't have any of the supported video editor software packages: `openshot`, `lightworks`, `kdenlive`

#### Something went wrong on the installation, I'm not sure what?

[This script](https://github.com/DragonComputer/Dragonfire/blob/master/install.sh) will try to install dependencies for you. Run these commands, respectively:

```
git clone https://github.com/DragonComputer/Dragonfire.git
cd Dragonfire/
chmod +x install.sh
sudo ./install.sh
```

#### Dragonfire started to give me senseless answers?

Dragonfire's learning is far from perfect so by the time, the conversations filled with incorrect information can lead her to wrong answers like `THE SUN IS HOT AND COLD`. To fix this kind of situations you can always wipe out her memories about the subject by calling: `FORGET ABOUT THE SUN`

#### Learning feature is blocking my way to reach to Omniscient Q&A Engine?

Learning feature has a priority so if in the past, you said something like `ALBERT EINSTEIN IS A PHYSICIST` then it will block your way when you asked anything about **Albert Einstein**. To fix this you should say: `FORGET ABOUT ALBERT EINSTEIN`

:checkered_flag: If none of the cases listed above are fitting to your situation then always consider to [file an issue](https://github.com/DragonComputer/Dragonfire/issues/new) or visit our [chat room on Gitter](https://gitter.im/DragonComputer/Lobby).
