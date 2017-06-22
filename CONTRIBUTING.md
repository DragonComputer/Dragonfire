# Contributing to Dragonfire

:+1::tada: First off, thanks for taking the time to contribute! :tada::+1:

The following is a set of guidelines for contributing to Dragonfire and its packages, which are hosted in the [Dragon Computer Organization](https://github.com/DragonComputer) on GitHub. These are mostly guidelines, not rules. Use your best judgment, and feel free to propose changes to this document in a pull request.

#### Table Of Contents

[Code of Conduct](#code-of-conduct)

[I don't want to read this whole thing, I just have a question!!!](#i-dont-want-to-read-this-whole-thing-i-just-have-a-question)

[What should I know before I get started?](#what-should-i-know-before-i-get-started)
  * [Install Dragonfire in Development Mode](#install-dragonfire-in-development-mode)
  * [Missing Software](#missing-software)
  * [Choice for Code Editor](#choice-for-code-editor)
  * [About Packaging](#about-packaging)

[How Can I Contribute?](#how-can-i-contribute)
  * [Reporting Bugs](#reporting-bugs)
  * [Suggesting Enhancements](#suggesting-enhancements)
  * [Your First Code Contribution](#your-first-code-contribution)
  * [Pull Requests](#pull-requests)

[Styleguides](#styleguides)
  * [Git Commit Messages](#git-commit-messages)
  * [Python Styleguide](#python-styleguide)


## Code of Conduct

This project and everyone participating in it is governed by the [Dragonfire Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to [mert.yildiran@bil.omu.edu.tr](mailto:mert.yildiran@bil.omu.edu.tr).

## I don't want to read this whole thing I just have a question!!!

> **Note:** Please don't file an issue to ask a question. You'll get faster results by using the resources below.

We have an official chat room and where the community chimes in with helpful advice if you have questions.

* [Gitter chat room](https://gitter.im/DragonComputer/Lobby)


## What should I know before I get started?

### Install Dragonfire in Development Mode

|                      |                                   |
|----------------------|-----------------------------------|
| **Operating system** | Linux                             |
| **Python version**   | CPython 2.7. Only 64 bit.         |
| **Distro**           | KDE neon, elementary OS, Ubuntu   |
| **Package managers** | [pip] (source packages only)      |

All modern releases (Ubuntu 12.04 LTS and above) of these distributions are fully supported. Any other Ubuntu based distributions are partially supported.

You need to install Dragonfire with sudo rights, even if you are installing editable/development mode because there is a post-installation script needs sudo rights.

```Shell
git clone https://github.com/DragonComputer/Dragonfire.git
cd Dragonfire/
sudo pip install -e .
```

Post-installation script consists of the [these lines](https://github.com/DragonComputer/Dragonfire/blob/master/setup.py#L19-L51). It's important to know it for troubleshooting installation problems.

Please watch [this playlist](https://www.youtube.com/playlist?list=PLwnH1TEQvAWddw8iTwCJ333fwygL2-tWD) if you do not understand how to use Dragonfire.

### Missing Software

There could be missing softwares on your system like **blender**, **gimp**, **inkscape**, **kdenlive**, etc. So Dragonfire will be unable to open them. If you want to use commands like `PHOTO EDITOR`, `INKSCAPE` install the necessary software on your system. You can see the list of built-in commands [here](https://github.com/DragonComputer/Dragonfire/blob/master/dragonfire/__init__.py#L80-L395).

### Choice for Code Editor

We use [Atom Editor](https://atom.io/) with tabs(four whitespaces) without auto-indentation. Indentation mistakes can be troublesome in Python, please don't send files with messed up indentations.

### About Packaging

If you are wondering about the directory structure then please take a look to official [Packaging and Distributing](https://packaging.python.org/tutorials/distributing-packages/) Projects tutorial of Python.


## How Can I Contribute?

### Reporting Bugs

This section guides you through submitting a bug report for Dragonfire. Following these guidelines helps maintainers and the community understand your report :pencil:, reproduce the behavior :computer: :computer:, and find related reports :mag_right:.

> **Note:** If you find a **Closed** issue that seems like it is the same thing that you're experiencing, open a new issue and include a link to the original issue in the body of your new one.

### Suggesting Enhancements

This section guides you through submitting an enhancement suggestion for Dragonfire, including completely new features and minor improvements to existing functionality. Following these guidelines helps maintainers and the community understand your suggestion :pencil: and find related suggestions :mag_right:.

### Your First Code Contribution

Unsure where to begin contributing to Dragonfire? You can start by looking through these `beginner` and `help-wanted` issues:

* [Beginner issues][beginner] - issues which should only require a few lines of code, and a test or two.
* [Help wanted issues][help-wanted] - issues which should be a bit more involved than `beginner` issues.

Both issue lists are sorted by total number of comments. While not perfect, number of comments is a reasonable proxy for impact a given change will have.

### Pull Requests

Feel free to send [pull requests](https://github.com/DragonComputer/Dragonfire/pulls).


## Styleguides

### Git Commit Messages

* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* Limit the first line to 72 characters or less
* Reference issues and pull requests liberally after the first line
* When only changing documentation, include `[ci skip]` in the commit description
* Consider starting the commit message with an applicable emoji:
    * :art: `:art:` when improving the format/structure of the code
    * :racehorse: `:racehorse:` when improving performance
    * :non-potable_water: `:non-potable_water:` when plugging memory leaks
    * :memo: `:memo:` when writing docs
    * :penguin: `:penguin:` when fixing something on Linux
    * :apple: `:apple:` when fixing something on macOS
    * :checkered_flag: `:checkered_flag:` when fixing something on Windows
    * :bug: `:bug:` when fixing a bug
    * :fire: `:fire:` when removing code or files
    * :green_heart: `:green_heart:` when fixing the CI build
    * :white_check_mark: `:white_check_mark:` when adding tests
    * :lock: `:lock:` when dealing with security
    * :arrow_up: `:arrow_up:` when upgrading dependencies
    * :arrow_down: `:arrow_down:` when downgrading dependencies
    * :shirt: `:shirt:` when removing linter warnings

### Python Styleguide

All Python must adhere to [PEP 8](https://www.python.org/dev/peps/pep-0008/).
