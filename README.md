# Dragonfire

<img src="https://travis-ci.org/DragonComputer/Dragonfire.svg?branch=master" align="right" />

Dragonfire is an open source virtual assistant project for Ubuntu based Linux distributions.

![Dragonfire](https://raw.githubusercontent.com/DragonComputer/Dragonfire/master/docs/img/demo.gif)

<p align="center"><sup><i>Special thanks to Jassu Ilama for the beautiful 3D modelling and material design of this avatar.</i></sup></p>

<br>

Dragonfire goes through these steps for each one of your commands, respectively:

 - Search across the built-in commands
 - Try to [Learn using Advanced NLP and Database Management Techniques](https://github.com/DragonComputer/Dragonfire/blob/master/dragonfire/learn.py)
 - Ask to [Omniscient Q&A Engine](https://github.com/DragonComputer/Dragonfire/blob/master/dragonfire/omniscient.py) (Thanks to all people who contributed to magnificent [spaCy](https://github.com/explosion/spaCy) project and [Wikipedia](https://en.wikipedia.org/), the free encyclopedia for this feature)

<br>

Dragonfire uses [Mozilla DeepSpeech](https://github.com/mozilla/DeepSpeech) to understand your voice commands and [Festival Speech Synthesis System](http://www.cstr.ed.ac.uk/projects/festival/) to handle text-to-speech tasks.

Feel free to join [our Gitter chat room](https://gitter.im/DragonComputer/Lobby).

#### Supported Environments

|                         |                                   |
|-------------------------|-----------------------------------|
| **Operating systems**   | Linux                             |
| **Python versions**     | Python 3.x (64-bit)               |
| **Distros**             | KDE neon, elementary OS, Ubuntu   |
| **Package managers**    | APT, pip                          |
| **Languages**           | English                           |
| **System requirements** | A decent GPU, 2GB free RAM        |
|                         |                                   |

### Installation

Download the [latest release](https://github.com/DragonComputer/Dragonfire/releases/latest) (the `.deb` file) and:

```Shell
sudo dpkg -i dragonfire_0.9.7_amd64.deb
```

<sup><i>To install the dependencies run `sudo apt-get -f install` right after the `dpkg -i` command. The installation will automatically download the pre-trained English model of Mozilla DeepSpeech (1.31 GB download size) and will place it under `/usr/share/deepspeech/models` directory. You can manually [download the model](https://github.com/mozilla/DeepSpeech/releases/download/v0.1.1/deepspeech-0.1.1-models.tar.gz) if you want.</i></sup>

### Usage

```
usage: dragonfire [-h] [-c] [-s] [--headless]

optional arguments:
  -h, --help    show this help message and exit
  -c, --cli     Command-line interface mode. Give commands to Dragonfire via
                command-line inputs (keyboard) instead of audio inputs
                (microphone).
  -s, --silent  Silent mode. Disable Text-to-Speech output. Dragonfire won't
                generate any audio output.
  --headless    Headless mode. Do not display an avatar animation on the
                screen. Disable the female head model.
```

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
WEB BROWSER
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
| **Dragonfire:** `PLEASE WAIT... NEW YORK CITY` :heavy_check_mark: | **Dragonfire:** `PLEASE WAIT... 1453` :heavy_check_mark:                    |
| **You:** `WHAT IS THE HEIGHT OF BURJ KHALIFA`                     | **You:** `WHAT IS THE CAPITAL OF TURKEY`                                    |
| **Dragonfire:** `PLEASE WAIT... 1,680 FT` :no_entry:              | **Dragonfire:** `PLEASE WAIT... ISTANBUL` :no_entry:                        |
| **You:** `WHERE IS BURJ KHALIFA`                                  | **You:** `WHAT IS THE LARGEST CITY OF TURKEY`                               |
| **Dragonfire:** `PLEASE WAIT... DUBAI` :heavy_check_mark:         | **Dragonfire:** `PLEASE WAIT... ISTANBUL` :heavy_check_mark:                |
| **You:** `WHAT IS THE HEIGHT OF GREAT PYRAMID OF GIZA`            | **You:** `WHAT IS THE NAME OF THE WORLD'S BEST UNIVERSITY`                  |
| **Dragonfire:** `PLEASE WAIT... (481 FEET` :heavy_check_mark:     | **Dragonfire:** `PLEASE WAIT... UNIVERSITIES ALUMNI ASSOCIATION` :no_entry: |
| **You:** `WHO IS PLAYING JON SNOW IN GAME OF THRONES`             | **You:** `WHO INVENTED GENERAL RELATIVITY`                                  |
| **Dragonfire:** `PLEASE WAIT... NED` :no_entry:                   | **Dragonfire:** `PLEASE WAIT... EINSTEIN` :heavy_check_mark:                |
| **You:** `WHAT IS THE ATOMIC NUMBER OF OXYGEN`                    | **You:** `WHEN WAS UNITED NATIONS FORMED`                                   |
| **Dragonfire:** `PLEASE WAIT... 8` :heavy_check_mark:             | **Dragonfire:** `PLEASE WAIT... 2017` :no_entry:                            |
| **You:** `WHAT IS THE LOWEST POINT IN THE OCEAN`                  | **You:** `WHAT IS THE NAME OF THE WORLD'S LONGEST RIVER`                    |
| **Dragonfire:** `PLEASE WAIT... EARTH` :no_entry:                 | **Dragonfire:** `PLEASE WAIT... AMAZON` :heavy_check_mark:                  |
| **You:** `WHAT IS THE OFFICIAL LANGUAGE OF JAPAN`                 | **You:** `WHAT IS THE BRAND OF THE WORLD'S MOST EXPENSIVE CAR`              |
| **Dragonfire:** `PLEASE WAIT... ENGLISH` :no_entry:               | **Dragonfire:** `PLEASE WAIT... MERCEDES-BENZ` :no_entry:                   |
| **You:** `WHAT IS THE REAL NAME OF IRON MAN`                      | **You:** `WHAT IS THE BLOODIEST WAR IN HUMAN HISTORY`                       |
| **Dragonfire:** `PLEASE WAIT... STARK` :heavy_check_mark:         | **Dragonfire:** `PLEASE WAIT... WORLD WAR II` :heavy_check_mark:            |
| **You:** `WHO IS THE CONQUEROR OF CONSTANTINOPLE`                 | **You:** `WHAT IS THE NAME OF THE BEST SELLER BOOK`                         |
| **Dragonfire:** `PLEASE WAIT... BYZANTIUM` :no_entry:             | **Dragonfire** `PLEASE WAIT... THE DISCIPLINE OF MARKET LEADERS` :no_entry: |
|                                                                   |                                                                             |

<br>

**Supported Distributions:** KDE neon, elementary OS and Ubuntu. All modern releases (Ubuntu 12.04 LTS and above) of these distributions are fully supported. Any other Ubuntu based distributions are partially supported.

### Contribute

If you want to contribute to Dragonfire then please read [this guide](https://github.com/DragonComputer/Dragonfire/blob/master/CONTRIBUTING.md#contributing-to-dragonfire).

Please consider to support us on Patreon:

<a href="https://www.patreon.com/DragonComputer">
  <p align="center">
    <img src="https://i.imgur.com/KDVHXg0.png" alt="Become a patron" height="80px"/>
  </p>
</a>
