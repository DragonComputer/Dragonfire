# Contributing to Dragonfire

:+1::tada: First off, thanks for taking the time to contribute! :tada::+1:

The following is a set of guidelines for contributing to Dragonfire an open source virtual assistant project, which is hosted in the [Dragon Computer Organization](https://github.com/DragonComputer) on GitHub. These are mostly guidelines, not rules. Use your best judgment, and feel free to propose changes to this document in a pull request.

#### Table Of Contents

* [Code of Conduct](#code-of-conduct)

* [I don't want to read this whole thing, I just have a question!!!](#i-dont-want-to-read-this-whole-thing-i-just-have-a-question)

* [Getting Started](#getting-started)
  * [Install Dragonfire in Development Mode](#install-dragonfire-in-development-mode)
  * [Missing Software](#missing-software)
  * [Choice for Code Editor](#choice-for-code-editor)
  * [About Packaging](#about-packaging)

* [How Can I Contribute?](#how-can-i-contribute)
  * [Reporting Bugs](#reporting-bugs)
  * [Suggesting Enhancements](#suggesting-enhancements)
  * [Your First Code Contribution](#your-first-code-contribution)
  * [Pull Requests](#pull-requests)

[Styleguides](#styleguides)
  * [Git Commit Messages](#git-commit-messages)
  * [Python Styleguide](#python-styleguide)


## Code of Conduct

This project and everyone participating in it is governed by the [Dragonfire's Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to [mert.yildiran@bil.omu.edu.tr](mailto:mert.yildiran@bil.omu.edu.tr).

### I don't want to read this whole thing I just have a question!!!

> **Note:** Please don't file an issue to ask a question. You'll get faster results by using the resources below.

We have an official [chat room on Gitter](https://gitter.im/DragonComputer/Lobby) where the community chimes in with helpful advice if you have questions.

## Getting Started

|                       |                                   |
|-----------------------|-----------------------------------|
| **Operating systems** | Linux                             |
| **Python versions**   | CPython 2.7. Only 64 bit.         |
| **Distros**           | KDE neon, elementary OS, Ubuntu   |
| **Package managers**  | APT, pip                          |
| **Languages**         | English                           |
|                       |                                   |

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
remote: Counting objects: 1069, done.
remote: Compressing objects: 100% (3/3), done.
remote: Total 1069 (delta 0), reused 2 (delta 0), pack-reused 1066
Receiving objects: 100% (1069/1069), 13.84 MiB | 70.00 KiB/s, done.
Resolving deltas: 100% (593/593), done.
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

which means: `-U` (upgrade), `-v` (verbose), -e (editable/development mode)

Post-installation script consists of the [these lines](https://github.com/DragonComputer/Dragonfire/blob/master/setup.py#L19-L51). It's important to know it for troubleshooting installation problems.

### Use It

Try to experience every command listed in [README.md](https://github.com/DragonComputer/Dragonfire#built-in-commands). Please watch [this playlist](https://www.youtube.com/playlist?list=PLwnH1TEQvAWddw8iTwCJ333fwygL2-tWD) if you do not understand how to use Dragonfire.

### Missing Software Packages (Optional)

There could be missing software packages on your system like **blender**, **gimp**, **inkscape**, **kdenlive**, etc. So Dragonfire will be unable to open them. If you want to use commands like `PHOTO EDITOR`, `INKSCAPE` install the necessary software on your system. You can see the list of built-in commands [here](https://github.com/DragonComputer/Dragonfire/blob/master/dragonfire/__init__.py#L80-L395).

### Choice for Code Editor

We use [Atom Editor](https://atom.io/) with tabs(four whitespaces) without auto-indentation. Indentation mistakes can be troublesome in Python, please don't send files with messed up indentations.

### About Packaging

If you are wondering about the package structure and distribution then please take a look to the official [Packaging and Distributing Projects](https://packaging.python.org/tutorials/distributing-packages/) tutorial of Python.


## How Can I Contribute?

### Reporting Bugs

If you think you found a bug in Dragonfire then please [file an issue](https://github.com/DragonComputer/Dragonfire/issues/new) immediately. Don't forget to mention that it's bug or something going on very wrong.

<!-- This section guides you through submitting a bug report for Dragonfire. Following these guidelines helps maintainers and the community understand your report :pencil:, reproduce the behavior :computer: :computer:, and find related reports :mag_right:. -->

> **Note:** If you find a **Closed** issue that seems like it is the same thing that you're experiencing, open a new issue and include a link to the original issue in the body of your new one.

### Suggesting Enhancements

If you have a new enhancement idea or you are not happy with an ugly piece of code then please [file an issue](https://github.com/DragonComputer/Dragonfire/issues/new) and mention that it's an enhancement proposal.

<!-- This section guides you through submitting an enhancement suggestion for Dragonfire, including completely new features and minor improvements to existing functionality. Following these guidelines helps maintainers and the community understand your suggestion :pencil: and find related suggestions :mag_right:. -->

### Projects

Look at the cards pinned to **To Do** columns inside [open projects](https://github.com/DragonComputer/Dragonfire/projects) to find something suitable for you. If you are willing to take a card/task from there then contact with project maintainers via [Gitter chat room](https://gitter.im/DragonComputer/Lobby) so they will assign that task to you.

### Your First Code Contribution

Unsure where to begin contributing to Dragonfire? You can start by looking through these `beginner` and `help-wanted` issues:

* [Beginner issues][beginner] which should only require a few lines of code, and a test or two.
* [Help wanted issues][help-wanted] which should be a bit more involved than `beginner` issues.
* [Missing dependency issues][missing-dependency] which should be mostly platform/distro related issues.
* [Enhancement proposals][enhancement] which should be improvements ideas or alteration proposals on code.
* [Bugs][bug] which should be issued with proof of existence and expected to be hard to fix.


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

[beginner]:https://github.com/DragonComputer/Dragonfire/issues?q=is%3Aissue+is%3Aopen+label%3Abeginner
[help-wanted]:https://github.com/DragonComputer/Dragonfire/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22
[missing-dependency]:https://github.com/DragonComputer/Dragonfire/issues?q=is%3Aissue+is%3Aopen+label%3A%22missing+dependency%22
[enhancement]:https://github.com/DragonComputer/Dragonfire/issues?q=is%3Aissue+is%3Aopen+label%3Aenhancement
[bug]:https://github.com/DragonComputer/Dragonfire/issues?q=is%3Aissue+is%3Aopen+label%3Abug
