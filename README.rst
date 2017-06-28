Dragonfire
==========

Dragonfire is an open source virtual assistant project for Ubuntu based
Linux distributions

Dragonfire will never leave your questions unanswered.

Dragonfire is not The Next Big Thing but a spectacular combination of
freely available technologies.

Dragonfire goes through these steps for your commands, respectively:

-  Search across the built-in commands
-  Try to `Learn using Advanced NLP and Database Management Techniques`_
-  Ask to `Omniscient Q&A Engine`_ (Thanks to all people who contributed
   to magnificent `spaCy`_ project and `Wikipedia`_, the free
   encyclopedia for this feature)

Feel free to join `our Gitter chat room`_.

Supported Environments
^^^^^^^^^^^^^^^^^^^^^^

+-------------------------+-----------------------------------+
| **Operating systems**   | Linux                             |
+-------------------------+-----------------------------------+
| **Python versions**     | CPython 2.7. Only 64 bit.         |
+-------------------------+-----------------------------------+
| **Distros**             | KDE neon, elementary OS, Ubuntu   |
+-------------------------+-----------------------------------+
| **Package managers**    | APT, pip                          |
+-------------------------+-----------------------------------+
| **Languages**           | English                           |
+-------------------------+-----------------------------------+

Installation
~~~~~~~~~~~~

.. code:: shell

    sudo pip install dragonfire

Usage
~~~~~

.. code:: shell

    dragonfire

To activate Dragonfire say *DRAGONFIRE* or *HEY* or *WAKE UP*.

To deactivate her say *GO TO SLEEP*.

To silence her say *ENOUGH* or *SHUT UP*.

To kill her say *GOODBYE* or *BYE BYE* or *SEE YOU LATER*.

Facing with a problem? Take a look to the `Troubleshooting`_ section.

Built-in Commands
^^^^^^^^^^^^^^^^^

`Dragonfire DEVLOG #3 - Built-in Commands`_

::

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
    (SEARCH|FIND) * (IN|ON|AT|USING) WIKIPEDA
    (SEARCH|FIND) * (IN|ON|AT|USING) YOUTUBE



.. _Learn using Advanced NLP and Database Management Techniques: https://github.com/DragonComputer/Dragonfire/blob/master/dragonfire/learn.py
.. _Omniscient Q&A Engine: https://github.com/DragonComputer/Dragonfire/blob/master/dragonfire/omniscient.py
.. _spaCy: https://github.com/explosion/spaCy
.. _Wikipedia: https://en.wikipedia.org/
.. _our Gitter chat room: https://gitter.im/DragonComputer/Lobby
.. _Troubleshooting: https://github.com/DragonComputer/Dragonfire/blob/master/CONTRIBUTING.md#troubleshooting
.. _Dragonfire DEVLOG #3 - Built-in Commands: https://youtu.be/krHUzY2DylI
