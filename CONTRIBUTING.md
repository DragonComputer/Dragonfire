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

- [Troubleshooting](https://github.com/DragonComputer/Dragonfire/blob/master/docs/TROUBLESHOOTING.md#troubleshooting)

- [Build the Debian package](#build-the-debian-package)

- [API Reference](#api-reference)

## Code of Conduct

This project and everyone participating in it is governed by the [Dragonfire's Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to [mert.yildiran@bil.omu.edu.tr](mailto:mert.yildiran@bil.omu.edu.tr).

#### I don't want to read this whole thing I just have a question!!!

> **Note:** Please don't file an issue to ask a question. You'll get faster results by using the resources below.

We have an official [chat room on Gitter](https://gitter.im/DragonComputer/Lobby) where the community chimes in with helpful advice if you have questions.


## Getting Started

|                         |                                         |
|-------------------------|-----------------------------------------|
| **Operating systems**   | Linux                                   |
| **Python versions**     | Python 3.x (64-bit)                     |
| **Distros**             | KDE neon, elementary OS, Ubuntu         |
| **Package managers**    | APT, pip                                |
| **Languages**           | English                                 |
| **System requirements** | a [CUDA supported GPU](https://www.geforce.com/hardware/technology/cuda/supported-gpus), 2GB of free RAM   |
|                         |                                         |

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

You need to install Dragonfire with `sudo` rights, even if you are installing editable/development mode because there is a [post-installation script](https://github.com/DragonComputer/Dragonfire/blob/master/debian/postinst) that needs `sudo` rights.

```Shell
git clone https://github.com/YOUR-USERNAME/Dragonfire.git
cd Dragonfire/
chmod +x install-dev.sh
sudo ./install-dev.sh
```

#### Use It

Try to experience every command listed in [README.md](https://github.com/DragonComputer/Dragonfire#built-in-commands). Please watch [this playlist](https://www.youtube.com/playlist?list=PLwnH1TEQvAWddw8iTwCJ333fwygL2-tWD) if you did not understand how to use Dragonfire.

If you face with a problem while installing or using Dragonfire then please take a look at the [Troubleshooting](https://github.com/DragonComputer/Dragonfire/blob/master/docs/TROUBLESHOOTING.md#troubleshooting) section for the cases that fitting to your situation. Our [chat room on Gitter](https://gitter.im/DragonComputer/Lobby) is also a viable option for support requests.

#### Missing Software Packages (Optional)

There could be missing software packages on your system like **blender**, **gimp**, **inkscape**, **kdenlive**, etc. So Dragonfire will be unable to open them. If you want to use the commands like `PHOTO EDITOR`, `INKSCAPE` install the necessary software to your system. You can see the list of built-in commands [here](https://github.com/DragonComputer/Dragonfire/blob/78adeedf7a278bcb26786130c0c6dd46d914fc95/dragonfire/__init__.py#L126-L463).

#### Choice for Code Editor

We use [Atom Editor](https://atom.io/) with tabs(four whitespaces) without auto-indentation. Indentation mistakes can be troublesome in Python, please don't send files with messed up indentations.

#### About Packaging

If you are wondering about the package structure and distribution then please take a look to the official [Packaging and Distributing Projects](https://packaging.python.org/tutorials/distributing-packages/) tutorial of Python.


## How Can I Contribute?

### Decide What To Do

#### Reporting Bugs

If you think you found a bug in Dragonfire then frist please check the all cases listed in [Troubleshooting](https://github.com/DragonComputer/Dragonfire/blob/master/docs/TROUBLESHOOTING.md#troubleshooting) section. If you still think that's a bug then please [file an issue](https://github.com/DragonComputer/Dragonfire/issues/new) immediately. Don't forget to mention that it's a bug or something going on very wrong.

<!-- This section guides you through submitting a bug report for Dragonfire. Following these guidelines helps maintainers and the community understand your report :pencil:, reproduce the behavior :computer: :computer:, and find related reports :mag_right:. -->

> **Note:** If you find a **Closed** issue that seems like it is the same thing that you're experiencing, open a new issue and include a link to the original issue in the body of your new one.

#### Suggesting Enhancements

If you have an enhancement idea or you are not happy with an ugly piece of code then please [file an issue](https://github.com/DragonComputer/Dragonfire/issues/new) and mention that it's an enhancement proposal.

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

Before proceeding to Step 4, make sure that you have done all the tests and you did not break any existing feature of Dragonfire.

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

## Build the Debian package

Install build dependencies:

```
sudo apt-get install debhelper python2.7-minimal python3 python3-all-dev python-setuptools python3-setuptools libglib2.0-dev libcairo2-dev libgtk2.0-dev
```

To building the Debian package simply run:

```
cd Dragonfire/
dpkg-buildpackage -us -uc
```

It will save the `.deb` file into parent directory. `debian/` directory is the directory contains all the configuration files and pre/post-installation scripts related to Debian packaging.

## API Reference

API reference of Dragonfire [hosted on Read the Docs](https://dragonfire.readthedocs.io/en/latest/dragonfire.html#module-dragonfire.api) and the build of documentation is automatically triggered by a webhook so you don't have to really do anything about it.

We use [Google Style Python Docstrings](http://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html) and [Sphinx](http://sphinx-doc.org/) to build the documentation.

If you want to build the documentation on your local machine for some reason then do the following:

```
cd docs/
sphinx-apidoc -f -o source/ ../dragonfire/
sphinx-build -b html source/ build/
```
