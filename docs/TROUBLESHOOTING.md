## Troubleshooting

#### No sound is coming out of my computer?

If there is no sound coming from your speakers when you see `Dragonfire: GOOD MORNING SIR` on your terminal or *To activate say 'Dragonfire!' or 'Wake Up!'* notification after you run Dragonfire with `dragonfire` command then there are two possibilities causing this problem:

1. Dragonfire's audio output (ALSA plug-in [aplay]: ALSA Playback) could be mapped to wrong audio device:

![](http://i.imgur.com/dsKHaKS.png)

you can fix this either by changing it to correct device using the audio settings of your operating system or you can choose to use Phonon `sudo apt-get install phonon` to configure your device priority:

![](http://i.imgur.com/tALl6UG.png)

2. The problem could be related to missing `festival` package on your system. It should normally be installed on post-installation automatically but try to install it one more time with:

```
sudo apt-get update
sudo apt-get install festival
```

If `festival` is missing in your repositories then [download](https://packages.ubuntu.com/xenial/amd64/festival/download) it and try to install it with `sudo dpkg -i festival_2.4-release-2_amd64.deb`.

#### Dragonfire is not reacting to my voice?

 - First of all, Dragonfire's speech recognition ability needs an Internet connection so make sure your machine is connected to the Internet.
 - If Internet connection is not the issue then check the output of `ps -aux | grep julius` while Dragonfire is running. You must see an output like this:
```
mertyil+  2402  4.0  0.3 443656 27780 pts/2    Sl+  04:48   0:00 julius -input mic -C /home/mertyildiran/Documents/Dragonfire/dragonfire/julian.jconf
```
 - If you cannot see such an output then that means speech recognition is not even started so that means [padsp](https://linux.die.net/man/1/padsp) and/or [julius](https://packages.ubuntu.com/xenial/julius) is missing on your system.
 - If you see such an output then most probably Dragonfire's audio input (ALSA plug-in [julius]: ALSA Capture) is mapped to wrong audio device:

![](http://i.imgur.com/SdQlY9Q.png)

you can fix this either by changing it to correct device using the audio settings of your operating system or you can choose to use Phonon `sudo apt-get install phonon` to configure your device priority:

![](http://i.imgur.com/9b8ttnP.png)

#### Dragonfire is understanding my commands but doing nothing?

Dragonfire starts on sleeping mode to do not disturb your acoustic environment. You need to active her by saying *DRAGONFIRE* or *HEY* or *WAKE UP* to your microphone.

#### Dragonfire is unnecessarily jumping into real world conversation of me?

Then you need to deactivate her by saying *GO TO SLEEP*.

#### Dragonfire confusing with her own voice?

Simply use your headphones:headphones: instead of the speakers:speaker: to listen Dragonfire or lower the volume.

#### Dragonfire started to read something and now she is not stopping?

Then you need to silence her by saying *ENOUGH* OR *SHUT UP*.

#### I'm done with Dragonfire, how can I shut her down?

By saying *GOODBYE* or *BYE BYE* or *SEE YOU LATER*.

#### Dragonfire calls me "Lady" but I'm a boy?

Dragonfire analyzes your name that registered on the operating system to determine your gender. Sometimes she makes mistakes (mostly if your name is not an English name) and call you by your opposite gender. To fix this you can say *MY TITLE IS SIR* or *I'M A MAN* or *I'M A BOY*.

#### Dragonfire calls me "Sir" but I'm a girl?

Dragonfire analyzes your name that registered on the operating system to determine your gender. Sometimes she makes mistakes (mostly if your name is not an English name) and call you by your opposite gender. To fix this you can say *MY TITLE IS LADY* or *I'M A LADY* or *I'M A WOMAN* or *I'M A GIRL*.

#### I want to be called as something different?

Sure, there is a command for that. You can usee `CALL ME *` command to manipulate her form of address for you to anything you want. For example: *CALL ME MASTER* or *CALL ME MY LORD* or *CALL ME MY FRIEND* etc.

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
wget https://raw.githubusercontent.com/DragonComputer/Dragonfire/master/install.sh
chmod +x install.sh
sudo ./install.sh
```

#### Dragonfire started to give me senseless answers?

Dragonfire's learning is far from perfect so by the time, the conversations filled with incorrect information can lead her to wrong answers like `THE SUN IS HOT AND COLD`. To fix this kind of situations you can always wipe out her memories about the subject by calling: `FORGET ABOUT THE SUN`

#### Learning feature is blocking my way to reach to Omniscient Q&A Engine?

Learning feature has a priority so if in the past, you said something like `ALBERT EINSTEIN IS A PHYSICIST` then it will block your way when you asked anything about **Albert Einstein**. To fix this you should say: `FORGET ABOUT ALBERT EINSTEIN`

:checkered_flag: If none of the cases listed above are fitting to your situation then always consider to [file an issue](https://github.com/DragonComputer/Dragonfire/issues/new) or visit our [chat room on Gitter](https://gitter.im/DragonComputer/Lobby).
