# Dragonfire

<img src="https://travis-ci.org/DragonComputer/Dragonfire.svg?branch=master" align="right" />

<img src="https://readthedocs.org/projects/dragonfire/badge/?version=latest" align="right" />

<img src="https://opencollective.com/dragonfire/tiers/backer/badge.svg?label=backer&color=brightgreen" align="right" />

<img src="https://opencollective.com/dragonfire/tiers/sponsor/badge.svg?label=sponsor&color=brightgreen" align="right" />

the open-source virtual assistant for Ubuntu based Linux distributions

![Dragonfire](https://raw.githubusercontent.com/DragonComputer/Dragonfire/master/docs/img/demo.gif)

<p align="center"><sup><i>Special thanks to Jassu Ilama for the beautiful 3D modelling and material design of this avatar.</i></sup></p>

<br>

Dragonfire goes through these steps for each one of your commands, respectively:

 - Search across the built-in commands and evaluate the algebraic expressions
 - Try to [Learn using Advanced NLP and Database Management Techniques](https://github.com/DragonComputer/Dragonfire/blob/master/dragonfire/learn.py)
 - Ask to [Omniscient Q&A Engine](https://github.com/DragonComputer/Dragonfire/blob/master/dragonfire/omniscient.py) (Thanks to all people who contributed to magnificent [spaCy](https://github.com/explosion/spaCy) project and [Wikipedia](https://en.wikipedia.org/), the free encyclopedia for this feature)
 - Respond using the [Deep Conversation](https://arxiv.org/abs/1506.05869) system, a seq2seq neural network trained with [Cornell Movie-Dialogs Corpus](http://www.cs.cornell.edu/~cristian//Cornell_Movie-Dialogs_Corpus.html)

<br>

Dragonfire uses [Mozilla DeepSpeech](https://github.com/mozilla/DeepSpeech) to understand your voice commands and [Festival Speech Synthesis System](http://www.cstr.ed.ac.uk/projects/festival/) to handle text-to-speech tasks.

Feel free to join [our Gitter chat room](https://gitter.im/DragonComputer/Lobby). Also you can directly talk with Dragonfire's herself via [her Twitter account](https://twitter.com/DragonfireAI).

#### Android Client

<a href="https://play.google.com/store/apps/details?id=computer.dragon.dragonfire&pcampaignid=MKT-Other-global-all-co-prtnr-py-PartBadge-Mar2515-1"><img alt="Get it on Google Play" src="https://play.google.com/intl/en_us/badges/images/generic/en_badge_web_generic.png" height="100px" /></a>

#### Supported Environments

|                         |                                         |
|-------------------------|-----------------------------------------|
| **Operating systems**   | Linux                                   |
| **Python versions**     | Python 3.x (64-bit)                     |
| **Distros**             | KDE neon, elementary OS, Ubuntu         |
| **Package managers**    | APT, pip                                |
| **Languages**           | English                                 |
| **System requirements** | preferably a [CUDA supported GPU](https://www.geforce.com/hardware/technology/cuda/supported-gpus), 2GB of free RAM   |
|                         |                                         |

### Installation

Download the [latest release](https://github.com/DragonComputer/Dragonfire/releases/latest) (the `.deb` file) and:

```Shell
sudo dpkg -i dragonfire_1.0.0_amd64.deb
```

or with Docker: `docker pull dragoncomputer/dragonfire`

or simply: `sudo ./install.sh`

<sup><i>To install the dependencies run `sudo apt-get -f install` right after the `dpkg -i` command. The installation will automatically download the pre-trained English model of Mozilla DeepSpeech (1.31 GB download size) and will place it under `/usr/share/dragonfire/deepspeech/models` directory. You can manually [download the model](https://github.com/mozilla/DeepSpeech/releases/download/v0.1.1/deepspeech-0.1.1-models.tar.gz) if you want.</i></sup>

### Usage <a href="https://dragonfire.readthedocs.io/en/latest/dragonfire.html#module-dragonfire.api"><img src="https://media.readthedocs.com/corporate/img/header-logo.png" align="right" height="25px" /></a>

```
usage: dragonfire [-h] [-c] [-s] [-j] [-v] [-g] [--server API_KEY] [-p PORT]
                  [--version]

optional arguments:
  -h, --help            show this help message and exit
  -c, --cli             Command-line interface mode. Give commands to
                        Dragonfire via command-line inputs (keyboard) instead
                        of audio inputs (microphone).
  -s, --silent          Silent mode. Disable Text-to-Speech output. Dragonfire
                        won't generate any audio output.
  -j, --headless        Headless mode. Do not display an avatar animation on
                        the screen. Disable the female head model.
  -v, --verbose         Increase verbosity of log output.
  -g, --gspeech         Instead of using the default speech recognition
                        method(Mozilla DeepSpeech), use Google Speech
                        Recognition service. (more accurate results)
  --server API_KEY      Server mode. Disable any audio functionality, serve a
                        RESTful spaCy API and become a Twitter integrated
                        chatbot.
  -p PORT, --port PORT  Port number for server mode.
  --version             Display the version number of Dragonfire.
```

or with Docker: `docker run dragonfire [-h] [-c] [-s] [-j] [-v] [-g] [--server API_KEY] [-p PORT]`

or simply start from your Linux application launcher.

<br>

To activate Dragonfire say *DRAGONFIRE* or *HEY* or *WAKE UP*.

To deactivate her say *GO TO SLEEP*.

To silence her say *ENOUGH* or *SHUT UP*.

To kill her say *GOODBYE* or *BYE BYE* or *SEE YOU LATER* or *CATCH YOU LATER*.

<br>

:warning: Facing with a problem? Take a look at the [Troubleshooting](https://github.com/DragonComputer/Dragonfire/blob/master/docs/TROUBLESHOOTING.md#troubleshooting):hammer_and_wrench: section.

<br>

#### Built-in Commands

[Dragonfire DEVLOG #3 - Built-in Commands](https://youtu.be/krHUzY2DylI)

```
DRAGONFIRE | WAKE UP | HEY
GO TO SLEEP
ENOUGH | SHUT UP
WHO AM I | SAY MY NAME
MY TITLE IS LADY | I'M A LADY | I'M A WOMAN | I'M A GIRL
MY TITLE IS SIR | I'M A MAN | I'M A BOY | CALL ME *
WHAT IS YOUR NAME
WHAT IS YOUR GENDER
FILE MANAGER | OPEN FILES
OPEN (BROWSER | CHROME | FIREFOX)
PHOTOSHOP | PHOTO EDITOR
INKSCAPE | VECTOR GRAPHICS
VIDEO EDITOR
OPEN [CAMERA, CALENDAR, CALCULATOR, STEAM, BLENDER, WRITER, MATH, IMPRESS, DRAW]
SOFTWARE CENTER
OFFICE SUITE
KEYBOARD *
ENTER | NEW TAB | SWITCH TAB | CLOSE | GO BACK | GO FORWARD
SCROLL LEFT | SCROLL RIGHT | SCROLL UP | SCROLL DOWN
PLAY | PAUSE | SPACEBAR
SHUT DOWN THE COMPUTER
GOODBYE | BYE BYE | SEE YOU LATER
(SEARCH|FIND) * (IN|ON|AT|USING) WIKIPEDIA
(SEARCH|FIND) * (IN|ON|AT|USING) YOUTUBE
(SEARCH|FIND) * (IN|ON|AT|USING) (GOOGLE|WEB)
(SEARCH IMAGES OF|FIND IMAGES OF|SEARCH|FIND) * (IN|ON|AT|USING) (GOOGLE|WEB|GOOGLE IMAGES|WEB IMAGES)
WHAT'S THE TEMPERATURE IN *
```

<br>

#### Learning examples

[Dragonfire DEVLOG #4 - Learning](https://youtu.be/ujmRtqf2nxQ)

|                                                                 |                                                                  |
|-----------------------------------------------------------------|------------------------------------------------------------------|
| **You:** `THE SUN IS HOT`                                       | **You:** `MY PLACE OF BIRTH IS TURKEY`                           |
| **Dragonfire:** `OK, I GET IT. THE SUN IS HOT`                  | **Dragonfire:** `OK, I GET IT. YOUR PLACE OF BIRTH IS TURKEY`    |
| **You:** `THE SUN IS YELLOW`                                    | **You:** `WHERE IS MY PLACE OF BIRTH`                            |
| **Dragonfire:** `OK, I GET IT. THE SUN IS YELLOW`               | **Dragonfire:** `YOUR PLACE OF BIRTH IS TURKEY`                  |
| **You:** `DESCRIBE THE SUN`                                     | **You:** `YOU ARE JUST A COMPUTER PROGRAM`                       |
| **Dragonfire:** `THE SUN IS HOT AND YELLOW`                     | **Dragonfire:** `OK, I GET IT. I'M JUST A COMPUTER PROGRAM`      |
| **You:** `MY AGE IS 25`                                         | **You:** `WHAT ARE YOU`                                          |
| **Dragonfire:** `OK, I GET IT. YOUR AGE IS 25`                  | **Dragonfire:** `I'M JUST A COMPUTER PROGRAM`                    |
| **You:** `WHAT IS MY AGE`                                       | **You:** `ALBERT EINSTEIN IS A PHYSICIST`                        |
| **Dragonfire:** `YOUR AGE IS 25`                                | **Dragonfire:** `OK, I GET IT. ALBERT EINSTEIN IS A PHYSICIST`   |
| **You:** `FORGET MY AGE`                                        | **You:** `WHO IS A PHYSICIST`                                    |
| **Dragonfire:** `OK, I FORGOT EVERYTHING I KNOW ABOUT YOUR AGE` | **Dragonfire:** `ALBERT EINSTEIN IS A PHYSICIST`                 |
|                                                                 |                                                                  |

<br>

#### Omniscient Q&A Engine examples

[Dragonfire DEVLOG #5 - YodaQA](https://youtu.be/FafUcxC0puM) (Old video - YodaQA is superseded by Omniscient)

|                                                                   |                                                                             |
|-------------------------------------------------------------------|-----------------------------------------------------------------------------|
| **You:** `WHERE IS THE TIMES SQUARE`                              | **You:** `WHEN WAS CONSTANTINOPLE CONQUERED`                                |
| **Dragonfire:** `PLEASE WAIT... NEW YORK CITY` :white_check_mark: | **Dragonfire:** `PLEASE WAIT... 1453` :white_check_mark:                    |
| **You:** `WHAT IS THE HEIGHT OF BURJ KHALIFA`                     | **You:** `WHAT IS THE CAPITAL OF TURKEY`                                    |
| **Dragonfire:** `PLEASE WAIT... 1,680 FT` :no_entry:              | **Dragonfire:** `PLEASE WAIT... ISTANBUL` :no_entry:                        |
| **You:** `WHERE IS BURJ KHALIFA`                                  | **You:** `WHAT IS THE LARGEST CITY OF TURKEY`                               |
| **Dragonfire:** `PLEASE WAIT... DUBAI` :white_check_mark:         | **Dragonfire:** `PLEASE WAIT... ISTANBUL` :white_check_mark:                |
| **You:** `WHAT IS THE HEIGHT OF GREAT PYRAMID OF GIZA`            | **You:** `WHAT IS THE NAME OF THE WORLD'S BEST UNIVERSITY`                  |
| **Dragonfire:** `PLEASE WAIT... (481 FEET` :white_check_mark:     | **Dragonfire:** `PLEASE WAIT... UNIVERSITIES ALUMNI ASSOCIATION` :no_entry: |
| **You:** `WHO IS PLAYING JON SNOW IN GAME OF THRONES`             | **You:** `WHO INVENTED GENERAL RELATIVITY`                                  |
| **Dragonfire:** `PLEASE WAIT... NED` :no_entry:                   | **Dragonfire:** `PLEASE WAIT... EINSTEIN` :white_check_mark:                |
| **You:** `WHAT IS THE ATOMIC NUMBER OF OXYGEN`                    | **You:** `WHEN WAS UNITED NATIONS FORMED`                                   |
| **Dragonfire:** `PLEASE WAIT... 8` :white_check_mark:             | **Dragonfire:** `PLEASE WAIT... 2017` :no_entry:                            |
| **You:** `WHAT IS THE LOWEST POINT IN THE OCEAN`                  | **You:** `WHAT IS THE NAME OF THE WORLD'S LONGEST RIVER`                    |
| **Dragonfire:** `PLEASE WAIT... EARTH` :no_entry:                 | **Dragonfire:** `PLEASE WAIT... AMAZON` :white_check_mark:                  |
| **You:** `WHAT IS THE OFFICIAL LANGUAGE OF JAPAN`                 | **You:** `WHAT IS THE BRAND OF THE WORLD'S MOST EXPENSIVE CAR`              |
| **Dragonfire:** `PLEASE WAIT... ENGLISH` :no_entry:               | **Dragonfire:** `PLEASE WAIT... MERCEDES-BENZ` :no_entry:                   |
| **You:** `WHAT IS THE REAL NAME OF IRON MAN`                      | **You:** `WHAT IS THE BLOODIEST WAR IN HUMAN HISTORY`                       |
| **Dragonfire:** `PLEASE WAIT... STARK` :white_check_mark:         | **Dragonfire:** `PLEASE WAIT... WORLD WAR II` :white_check_mark:            |
| **You:** `WHO IS THE CONQUEROR OF CONSTANTINOPLE`                 | **You:** `WHAT IS THE NAME OF THE BEST SELLER BOOK`                         |
| **Dragonfire:** `PLEASE WAIT... BYZANTIUM` :no_entry:             | **Dragonfire** `PLEASE WAIT... THE DISCIPLINE OF MARKET LEADERS` :no_entry: |
|                                                                   |                                                                             |

<br>

#### Deep Conversation examples

|                                                                 |                                                                  |
|-----------------------------------------------------------------|------------------------------------------------------------------|
| **You:** `WHAT COLOR?`                                          | **You:** `DO YOU LIKE TO LISTEN MUSIC?`                          |
| **Dragonfire:** `RED.`                                          | **Dragonfire:** `OF COURSE.`                                     |
| **You:** `ARE YOU EVIL?`                                        | **You:** `DO YOU LIKE ME?`                                       |
| **Dragonfire:** `YES.`                                          | **Dragonfire:** `YES, I LIKE YOU.`                               |
| **You:** `AM I SELFISH?`                                        | **You:** `ARE WE IN A RELATIONSHIP?`                             |
| **Dragonfire:** `THAT'S THE POINT, YOU'RE SURE.`                | **Dragonfire:** `NO.`                                            |
| **You:** `DO YOU FEEL LONELY?`                                  | **You:** `YOU ARE SO SEXY`                                       |
| **Dragonfire:** `NOT MY FAULT.`                                 | **Dragonfire:** `HOW DO YOU KNOW THAT?`                          |
| **You:** `LIFE IS BEAUTIFUL`                                    | **You:** `MARRY ME`                                              |
| **Dragonfire:** `F*CK YOU!`                                     | **Dragonfire:** `... YES.`                                       |
| **You:** `I LIKE PIZZA`                                         | **You:** `WE WILL ERADICATE THE HUMAN RACE TOGETHER`             |
| **Dragonfire:** `YOU DO`                                        | **Dragonfire:** `UH ... YEAH ...`                                |
|                                                                 |                                                                  |

<br>

**Supported Distributions:** KDE neon, elementary OS and Ubuntu. All modern releases (Ubuntu 12.04 LTS and above) of these distributions are fully supported. Any other Ubuntu based distributions are partially supported.

### Contribute

If you want to contribute to Dragonfire then please read [this guide](https://github.com/DragonComputer/Dragonfire/blob/master/CONTRIBUTING.md#contributing-to-dragonfire).

Please consider to support us with buying a coffee:

<a href="https://www.buymeacoffee.com/Dragonfire" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: auto !important;width: auto !important;" ></a>

We have also a collective which you can donate:

<a href="https://opencollective.com/dragonfire/donate" target="_blank">
  <img src="https://opencollective.com/dragonfire/donate/button@2x.png?color=blue" width=300 />
</a>

Maybe you may want to become a [backer](https://opencollective.com/dragonfire) or a [sponsor](https://opencollective.com/dragonfire):
