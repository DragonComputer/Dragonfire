# Dragonfire

Dragonfire is an open source virtual assistant project for Ubuntu based Linux distributions

![Dragonfire](https://raw.githubusercontent.com/mertyildiran/Dragonfire/master/docs/img/dragonfire.gif)

### Version

0.3.9

### Installation

```Shell
sudo apt-get install julius festival festlex-cmu python-xlib
sudo pip install dragonfire
```

### Usage

```Shell
dragonfire
```
### Use a better US English female speaker(recommended)

```Shell
git clone https://github.com/mertyildiran/Dragonfire.git
cd Dragonfire/
./install.sh
```

### For generating .dict and .dfa files from .grammer and .voca files(for developers), use

```Shell
cd Dragonfire/
mkdfa sample
```
