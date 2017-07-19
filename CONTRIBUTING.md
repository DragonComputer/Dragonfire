# Contributing to Dragonfire

:sparkles: First off all, thanks for taking the time to contribute! :sparkles:

The following is a set of guidelines for contributing to Dragonfire an open source virtual assistant project, which is hosted in the [Dragon Computer Organization](https://github.com/DragonComputer) on GitHub. These are mostly guidelines, not rules. Use your best judgment, and feel free to propose changes to this document in a pull request.

#### Table Of Contents

- [Code of Conduct](#code-of-conduct)

- [Getting Started](#getting-started)
  - [Fork The Repo](#fork-the-repo)
    - [Step 1: Set Up Git](#step-1-set-up-git)
    - [Step 2: Fork The Repo](#step-2-fork-the-repo)
    - [Step 3: Create a local clone of your fork](#step-3-create-a-local-clone-of-your-fork)
  - [Install Dragonfire in Development Mode](#install-dragonfire-in-development-mode)
    - [Use It](#use-it)
    - [Missing Software Packages (Optional)](#missing-software-packages-optional)
    - [Choice for Code Editor](#choice-for-code-editor)
    - [About Packaging](#about-packaging)

- [How Can I Contribute?](#how-can-i-contribute)
  - [Decide What To Do](#decide-what-to-do)
    - [Reporting Bugs](#reporting-bugs)
    - [Suggesting Enhancements](#suggesting-enhancements)
    - [Projects](#projects)
    - [Your First Code Contribution](#your-first-code-contribution)
  - [Push & Pull](#push--pull)
    - [Step 1: Go to the local clone of your fork](#step-1-go-to-the-local-clone-of-your-fork)
    - [Step 2: Pull the Latest Changes](#step-2-pull-the-latest-changes)
    - [Step 3: Write Your Code](#step-3-write-your-code)
    - [Step 4: Push To Your Fork](#step-4-push-to-your-fork)
    - [Step 5: Creating a Pull Request](#step-5-creating-a-pull-request)

- [Styleguides](#styleguides)
  - [Git Commit Messages](#git-commit-messages)
  - [Python Styleguide](#python-styleguide)

- [Troubleshooting](#troubleshooting)

- [Build the Debian package](#build-the-debian-package)

## Code of Conduct

This project and everyone participating in it is governed by the [Dragonfire's Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to [mert.yildiran@bil.omu.edu.tr](mailto:mert.yildiran@bil.omu.edu.tr).

#### I don't want to read this whole thing I just have a question!!!

> **Note:** Please don't file an issue to ask a question. You'll get faster results by using the resources below.

We have an official [chat room on Gitter](https://gitter.im/DragonComputer/Lobby) where the community chimes in with helpful advice if you have questions.


## Getting Started

|                         |                                   |
|-------------------------|-----------------------------------|
| **Operating systems**   | Linux                             |
| **Python versions**     | CPython 2.7. Only 64 bit.         |
| **Distros**             | KDE neon, elementary OS, Ubuntu   |
| **Package managers**    | APT, pip                          |
| **Languages**           | English                           |
| **System requirements** | Minimally 1 Core, 2GB free RAM    |
|                         |                                   |

**Supported Distributions:** KDE neon, elementary OS and Ubuntu. All modern releases (Ubuntu 12.04 LTS and above) of these distributions are fully supported. Any other Ubuntu based distributions are partially supported.

### Fork The Repo

#### Step 1: Set Up Git

If you haven't yet, you should first [set up Git](https://help.github.com/articles/set-up-git). Don't forget to [set up authentication to GitHub from Git](https://help.github.com/articles/set-up-git#next-steps-authenticating-with-github-from-git) as well.

#### Step 2: Fork The Repo

Forking a repository is a simple two-step process:

<img src="http://i.imgur.com/XlXtYBV.png" width="300" align="right" />

1. On GitHub, navigate to the [DragonComputer/Dragonfire](https://github.com/DragonComputer/Dragonfire) repository.
2. In the top-right corner of the page, click **Fork**.

That's it! Now, you have a **fork** of the original Dragonfire repository under your account.

#### Step 3: Create a local clone of your fork

Right now, you have a fork of the Dragonfire repository, but you don't have the files in that repository on your computer. Let's create a *clone* of your fork locally on your computer:

<img src="http://i.imgur.com/jB2aFXQ.png" width="300" align="right" />

1. On GitHub, navigate to **your fork** of the Dragonfire repository.
2. Under the repository name, click **Clone or download**.
3. Copy the given clone URL in the **Clone with HTTPs** section.
4. Open Terminal
5. Type `git clone`, and then paste the URL you copied in Step 2. It will look like this, with your GitHub username instead of `YOUR-USERNAME`:
```
git clone https://github.com/YOUR-USERNAME/Dragonfire.git
```
6. Press **Enter**. Your local clone will be created:
```
git clone https://github.com/YOUR-USERNAME/Dragonfire.git
Cloning into 'Dragonfire'...
remote: Counting objects: 1076, done.
remote: Compressing objects: 100% (6/6), done.
remote: Total 1076 (delta 4), reused 9 (delta 4), pack-reused 1066
Receiving objects: 100% (1076/1076), 13.85 MiB | 1.62 MiB/s, done.
Resolving deltas: 100% (597/597), done.
Checking connectivity... done.
```

### Install Dragonfire in Development Mode

You need to install Dragonfire with `sudo` rights, even if you are installing editable/development mode because there is a post-installation script needs `sudo` rights.

```Shell
git clone https://github.com/YOUR-USERNAME/Dragonfire.git
cd Dragonfire/
sudo pip install -e .
```

alternatively you can install it with:

```
sudo pip install -Uve .
```

which means: `-U` (upgrade), `-v` (verbose), `-e` (editable/development mode)

Post-installation script consists of the [these lines](https://github.com/DragonComputer/Dragonfire/blob/master/setup.py#L19-L51). It's important to know it for troubleshooting installation problems.

#### Use It

Try to experience every command listed in [README.md](https://github.com/DragonComputer/Dragonfire#built-in-commands). Please watch [this playlist](https://www.youtube.com/playlist?list=PLwnH1TEQvAWddw8iTwCJ333fwygL2-tWD) if you do not understand how to use Dragonfire.

If you face with a problem while installing or using Dragonfire then please take a look to the [Troubleshooting](#troubleshooting) section for cases that fitting to you situation. Our [chat room on Gitter](https://gitter.im/DragonComputer/Lobby) is also a viable option for support requests.

#### Missing Software Packages (Optional)

There could be missing software packages on your system like **blender**, **gimp**, **inkscape**, **kdenlive**, etc. So Dragonfire will be unable to open them. If you want to use commands like `PHOTO EDITOR`, `INKSCAPE` install the necessary software on your system. You can see the list of built-in commands [here](https://github.com/DragonComputer/Dragonfire/blob/master/dragonfire/__init__.py#L80-L395).

#### Choice for Code Editor

We use [Atom Editor](https://atom.io/) with tabs(four whitespaces) without auto-indentation. Indentation mistakes can be troublesome in Python, please don't send files with messed up indentations.

#### About Packaging

If you are wondering about the package structure and distribution then please take a look to the official [Packaging and Distributing Projects](https://packaging.python.org/tutorials/distributing-packages/) tutorial of Python.


## How Can I Contribute?

### Decide What To Do

#### Reporting Bugs

If you think you found a bug in Dragonfire then frist please check the all cases listed in [Troubleshooting](#troubleshooting) section. If you still think that's a bug then please [file an issue](https://github.com/DragonComputer/Dragonfire/issues/new) immediately. Don't forget to mention that it's a bug or something going on very wrong.

<!-- This section guides you through submitting a bug report for Dragonfire. Following these guidelines helps maintainers and the community understand your report :pencil:, reproduce the behavior :computer: :computer:, and find related reports :mag_right:. -->

> **Note:** If you find a **Closed** issue that seems like it is the same thing that you're experiencing, open a new issue and include a link to the original issue in the body of your new one.

#### Suggesting Enhancements

If you have a enhancement idea or you are not happy with an ugly piece of code then please [file an issue](https://github.com/DragonComputer/Dragonfire/issues/new) and mention that it's an enhancement proposal.

<!-- This section guides you through submitting an enhancement suggestion for Dragonfire, including completely new features and minor improvements to existing functionality. Following these guidelines helps maintainers and the community understand your suggestion :pencil: and find related suggestions :mag_right:. -->

#### Projects

Look at the cards pinned to **To Do** columns inside [open projects](https://github.com/DragonComputer/Dragonfire/projects) to find something suitable for you. If you are willing to take a card/task from there then contact with project maintainers via [Gitter chat room](https://gitter.im/DragonComputer/Lobby) so they will assign that task to you.

#### Your First Code Contribution

Unsure where to begin contributing to Dragonfire? You can start by looking through these `beginner` and `help-wanted` issues:

 - [Beginner issues][beginner] which should only require a few lines of code, and a test or two.
 - [Help wanted issues][help-wanted] which should be a bit more involved than `beginner` issues.
 - [Missing dependency issues][missing-dependency] which should be mostly platform/distro related issues.
 - [Enhancement proposals][enhancement] which should be improvements ideas or alteration proposals on code.
 - [Bugs][bug] which should be issued with proof of existence and expected to be hard to fix.

Now you must have decided what to do. Before starting to write some code, take a quick look to [PEP 8](https://www.python.org/dev/peps/pep-0008/) - [because](#python-styleguide) :point_down:

### Push & Pull

For working well disciplined, you need to know how to deal with **git**'s push and pull mechanisms.

#### Step 1: Go to the local clone of your fork

Now `cd` into the local clone of your fork. Wherever the folder of Dragonfire is:

```
cd Dragonfire/
```

#### Step 2: Pull the Latest Changes

Now make sure your repository is up to date first using:

```
git pull origin master
```

#### Step 3: Write Your Code

At this step you are free to make any changes inside the local clone of your fork. Make sure that your changes serve to **single well defined goal** which will be your commit message. **DO NOT** try to achieve multiple (and unrelated) tasks with a single commit.

Before proceeding to Step 4, make sure that you have done all tests and you did not break any existing feature of Dragonfire.

#### Step 4: Push To Your Fork

When you are done, you must push your changes from the local clone to your fork with:

```
git add -A
git commit -m "Change this functionality from here to there"
git push -u origin master
```

<sup>Replace the message in `git commit -m "Change this functionality from here to there"` line with your actual message.</sup>

#### Step 5: Creating a Pull Request

Now follow [this tutorial](https://help.github.com/articles/creating-a-pull-request/) to create a pull request. You will create your pull request via [this page](https://github.com/DragonComputer/Dragonfire/compare).

Once you have successfully created the pull request, wait for a response from the project maintainers. If your patch is OK then we will merge it within approximately 24 hours.


## Styleguides

### Git Commit Messages

 - Use the present tense ("Add feature" not "Added feature")
 - Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
 - Limit the first line to 72 characters or less
 - Reference issues and pull requests liberally after the first line
 - Consider starting the commit message with an applicable emoji:
   - :art: `:art:` when improving the format/structure of the code
   - :rocket: `:rocket:` when improving performance
   - :robot: `:robot:` when improving the AI
   - :memo: `:memo:` when writing docs
   - :penguin: `:penguin:` when fixing something related to Linux
   - :apple: `:apple:` when fixing something related to macOS
   - :bug: `:bug:` when fixing a bug
   - :bulb: `:bulb:` new idea
   - :construction: `:construction:` work in progress
   - :heavy_plus_sign: `:heavy_plus_sign:` when adding feature
   - :heavy_minus_sign: `:heavy_minus_sign:` when removing feature
   - :speaker: `:speaker:` when adding logging
   - :mute: `:mute:` when reducing logging
   - :fire: `:fire:` when removing code or files
   - :white_check_mark: `:white_check_mark:` when adding tests
   - :lock: `:lock:` when dealing with security
   - :arrow_up: `:arrow_up:` when upgrading dependencies
   - :arrow_down: `:arrow_down:` when downgrading dependencies
   - :shirt: `:shirt:` when removing linter warnings

### Python Styleguide

All Python must adhere to [PEP 8](https://www.python.org/dev/peps/pep-0008/).

[beginner]:https://github.com/DragonComputer/Dragonfire/issues?q=is%3Aissue+is%3Aopen+label%3Abeginner
[help-wanted]:https://github.com/DragonComputer/Dragonfire/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22
[missing-dependency]:https://github.com/DragonComputer/Dragonfire/issues?q=is%3Aissue+is%3Aopen+label%3A%22missing+dependency%22
[enhancement]:https://github.com/DragonComputer/Dragonfire/issues?q=is%3Aissue+is%3Aopen+label%3Aenhancement
[bug]:https://github.com/DragonComputer/Dragonfire/issues?q=is%3Aissue+is%3Aopen+label%3Abug


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

## Build the Debian package

Install build dependencies:

```
sudo apt-get install debhelper python dh-virtualenv python-all-dev libglib2.0-dev libcairo2-dev libgtk2.0-dev
```

To building the Debian package simply run:

```
cd Dragonfire/
dpkg-buildpackage -us -uc -b
```

It will save the `.deb` file into parent directory. `debian` directory is the directory contains all the configuration files and pre/post installation scripts related to Debian packaging.
