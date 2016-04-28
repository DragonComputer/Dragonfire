# Dragonfire

Dragonfire is an open source virtual assistant project for Ubuntu based Linux distributions

![Dragonfire](https://raw.githubusercontent.com/mertyildiran/Dragonfire/master/docs/img/dragonfire.gif)

*Dragonfire will never leave your questions unanswered.*

Dragonfire does following tasks for each separate command, respectively:

 - Search across the built-in functions of Dragonfire
 - Explore A.L.I.C.E. AIML
 - Run Wikipedia Answering Machine

### Version

0.5.0

### Installation

```Shell
sudo pip install dragonfire
```

### Usage

```Shell
dragonfire
```

To activate Dragonfire say *DRAGONFIRE* or *HEY* or *WAKE UP*.
To deactivate her say *GO TO SLEEP*.
To silence her say *ENOUGH*.
To kill her say *GOODBYE* or *BYE BYE* or *SEE YOU LATER*.

For generating .dict and .dfa files from .grammer and .voca files(for developers only), use:

```Shell
cd Dragonfire/dragonfire/
mkdfa sample
```
