Dragonfire
==========

Dragonfire is an open source virtual assistant project for Ubuntu based
Linux distributions.

Dragonfire will never leave your questions unanswered.

Dragonfire is not The Next Big Thing but a spectacular combination of
freely available technologies.

Dragonfire goes through these steps for your commands, respectively:

-  Search across the built-in commands
-  Try to `Learn using Advanced NLP and Database Management
   Techniques <https://github.com/DragonComputer/Dragonfire/blob/master/dragonfire/learn.py>`__
-  Ask to `Omniscient Q&A
   Engine <https://github.com/DragonComputer/Dragonfire/blob/master/dragonfire/omniscient.py>`__
   (Thanks to all people who contributed to magnificent
   `spaCy <https://github.com/explosion/spaCy>`__ project and
   `Wikipedia <https://en.wikipedia.org/>`__, the free encyclopedia for
   this feature)

Feel free to join `our Gitter chat
room <https://gitter.im/DragonComputer/Lobby>`__.

Supported Environments
^^^^^^^^^^^^^^^^^^^^^^

+---------------------------+-----------------------------------+
| **Operating systems**     | Linux                             |
+---------------------------+-----------------------------------+
| **Python versions**       | CPython 2.7. Only 64 bit.         |
+---------------------------+-----------------------------------+
| **Distros**               | KDE neon, elementary OS, Ubuntu   |
+---------------------------+-----------------------------------+
| **Package managers**      | APT, pip                          |
+---------------------------+-----------------------------------+
| **Languages**             | English                           |
+---------------------------+-----------------------------------+
| **System requirements**   | Minimally 1 Core, 2GB free RAM    |
+---------------------------+-----------------------------------+

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

Facing with a problem? Take a look to the
`Troubleshooting <https://github.com/DragonComputer/Dragonfire/blob/master/CONTRIBUTING.md#troubleshooting>`__
section.

Built-in Commands
^^^^^^^^^^^^^^^^^

`Dragonfire DEVLOG #3 - Built-in
Commands <https://youtu.be/krHUzY2DylI>`__

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

Learning examples
^^^^^^^^^^^^^^^^^

`Dragonfire DEVLOG #4 - Learning <https://youtu.be/ujmRtqf2nxQ>`__

+-------------------------------------+--------------------------------------+
| **You:** ``THE SUN IS HOT``         | **You:**                             |
|                                     | ``WHERE IS MY PLACE OF BIRTH``       |
+-------------------------------------+--------------------------------------+
| **Dragonfire:**                     | **Dragonfire:**                      |
| ``OK, I GET IT. THE SUN IS HOT``    | ``YOUR PLACE OF BIRTH IS TURKEY``    |
+-------------------------------------+--------------------------------------+
| **You:** ``THE SUN IS YELLOW``      | **You:**                             |
|                                     | ``YOU ARE JUST A COMPUTER PROGRAM``  |
+-------------------------------------+--------------------------------------+
| **Dragonfire:**                     | **Dragonfire:**                      |
| ``OK, I GET IT. THE SUN IS YELLOW`` | ``OK, I GET IT. I'M JUST A COMPUTER  |
|                                     | PROGRAM``                            |
+-------------------------------------+--------------------------------------+
| **You:** ``DESCRIBE THE SUN``       | **You:** ``WHAT ARE YOU``            |
+-------------------------------------+--------------------------------------+
| **Dragonfire:**                     | **Dragonfire:**                      |
| ``THE SUN IS HOT AND YELLOW``       | ``I'M JUST A COMPUTER PROGRAM``      |
+-------------------------------------+--------------------------------------+
| **You:** ``MY AGE IS 25``           | **You:** ``FORGET MY AGE``           |
+-------------------------------------+--------------------------------------+
| **Dragonfire:**                     | **Dragonfire:**                      |
| ``OK, I GET IT. YOUR AGE IS 25``    | ``OK, I FORGOT EVERYTHING I KNOW ABO |
|                                     | UT YOUR AGE``                        |
+-------------------------------------+--------------------------------------+
| **You:** ``WHAT IS MY AGE``         | **You:** ``UPDATE MY AGE``           |
+-------------------------------------+--------------------------------------+
| **Dragonfire:** ``YOUR AGE IS 25``  | **Dragonfire:**                      |
|                                     | ``I WASN'T EVEN KNOW ANYTHING ABOUT  |
|                                     | YOUR AGE``                           |
+-------------------------------------+--------------------------------------+
| **You:**                            |                                      |
| ``MY PLACE OF BIRTH IS TURKEY``     |                                      |
+-------------------------------------+--------------------------------------+
| **Dragonfire:**                     |                                      |
| ``OK, I GET IT. YOUR PLACE OF BIRTH |                                      |
|  IS TURKEY``                        |                                      |
+-------------------------------------+--------------------------------------+

Omniscient Q&A Engine examples
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

`Dragonfire DEVLOG #5 - YodaQA <https://youtu.be/FafUcxC0puM>`__ (Old
video - YodaQA is deprecated)

+------------------------------------+---------------------------------------+
| **You:**                           | **You:**                              |
| ``WHERE IS THE TIMES SQUARE``      | ``WHEN WAS CONSTANTINOPLE CONQUERED`` |
+------------------------------------+---------------------------------------+
| **Dragonfire:**                    | **Dragonfire:**                       |
| ``PLEASE WAIT... NEW YORK CITY``   | ``PLEASE WAIT... THE 5TH CENTURY``    |
| :white\_check\_mark:               | :no\_entry:                           |
+------------------------------------+---------------------------------------+
| **You:**                           | **You:**                              |
| ``WHAT IS THE HEIGHT OF BURJ KHALI | ``WHAT IS THE CAPITAL OF TURKEY``     |
| FA``                               |                                       |
+------------------------------------+---------------------------------------+
| **Dragonfire:**                    | **Dragonfire:**                       |
| ``PLEASE WAIT... 1,680 FT``        | ``PLEASE WAIT... ROME`` :no\_entry:   |
| :no\_entry:                        |                                       |
+------------------------------------+---------------------------------------+
| **You:** ``WHERE IS BURJ KHALIFA`` | **You:**                              |
|                                    | ``WHAT IS THE LARGEST CITY OF TURKEY` |
|                                    | `                                     |
+------------------------------------+---------------------------------------+
| **Dragonfire:**                    | **Dragonfire:**                       |
| ``PLEASE WAIT... DUBAI``           | ``PLEASE WAIT... ISTANBUL``           |
| :white\_check\_mark:               | :white\_check\_mark:                  |
+------------------------------------+---------------------------------------+
| **You:**                           | **You:**                              |
| ``WHAT IS THE HEIGHT OF GREAT PYRA | ``WHAT IS THE OLDEST RELIGION``       |
| MID OF GIZA``                      |                                       |
+------------------------------------+---------------------------------------+
| **Dragonfire:**                    | **Dragonfire:**                       |
| ``PLEASE WAIT... (481 FEET``       | ``PLEASE WAIT... GERMAN`` :no\_entry: |
| :white\_check\_mark:               |                                       |
+------------------------------------+---------------------------------------+
| **You:**                           | **You:**                              |
| ``WHO IS PLAYING JON SNOW IN GAME  | ``WHAT IS THE WORLD'S BUSIEST AIRPORT |
| OF THRONES``                       | ``                                    |
+------------------------------------+---------------------------------------+
| **Dragonfire:**                    | **Dragonfire:**                       |
| ``PLEASE WAIT... NED`` :no\_entry: | ``PLEASE WAIT... THE AIRPORTS COUNCIL |
|                                    |  INTERNATIONAL``                      |
+------------------------------------+---------------------------------------+
| **You:**                           | **You:**                              |
| ``WHAT IS THE ATOMIC NUMBER OF OXY | ``WHAT IS THE NAME OF THE WORLD'S BES |
| GEN``                              | T UNIVERSITY``                        |
+------------------------------------+---------------------------------------+
| **Dragonfire:**                    | **Dragonfire:**                       |
| ``PLEASE WAIT... 8``               | ``PLEASE WAIT... U.S. NEWS``          |
| :white\_check\_mark:               | :no\_entry:                           |
+------------------------------------+---------------------------------------+
| **You:**                           | **You:**                              |
| ``WHAT IS THE POPULATION OF CHINA` | ``WHAT IS THE NAME OF THE WORLD'S LON |
| `                                  | GEST RIVER``                          |
+------------------------------------+---------------------------------------+
| **Dragonfire:**                    | **Dragonfire:**                       |
| ``PLEASE WAIT... 66,537,177``      | ``PLEASE WAIT... THE NORTH SEA``      |
| :no\_entry:                        | :no\_entry:                           |
+------------------------------------+---------------------------------------+
| **You:**                           | **You:**                              |
| ``WHAT IS THE OFFICIAL LANGUAGE OF | ``WHAT IS THE BRAND OF THE WORLD'S MO |
|  JAPAN``                           | ST EXPENSIVE CAR``                    |
+------------------------------------+---------------------------------------+
| **Dragonfire:**                    | **Dragonfire:**                       |
| ``PLEASE WAIT... JAPANESE``        | ``PLEASE WAIT... MERCEDES-BENZ``      |
| :white\_check\_mark:               | :no\_entry:                           |
+------------------------------------+---------------------------------------+
| **You:**                           | **You:**                              |
| ``WHAT IS THE REAL NAME OF IRON MA | ``WHAT IS THE BLOODIEST WAR IN HUMAN  |
| N``                                | HISTORY``                             |
+------------------------------------+---------------------------------------+
| **Dragonfire:**                    | **Dragonfire:**                       |
| ``PLEASE WAIT... STARK``           | ``PLEASE WAIT... THE "EUROPEAN AGE"`` |
| :white\_check\_mark:               | :no\_entry:                           |
+------------------------------------+---------------------------------------+
| **You:**                           | **You:**                              |
| ``WHO IS THE CONQUEROR OF CONSTANT | ``WHAT IS THE NAME OF THE BEST SELLER |
| INOPLE``                           |  BOOK``                               |
+------------------------------------+---------------------------------------+
| **Dragonfire:**                    | **Dragonfire**                        |
| ``PLEASE WAIT... HAGIA SOPHIA``    | ``PLEASE WAIT... THE "CHILDREN'S BEST |
| :no\_entry:                        |  SELLERS``                            |
|                                    | :no\_entry:                           |
+------------------------------------+---------------------------------------+

**Supported Distributions:** KDE neon, elementary OS and Ubuntu. All
modern releases (Ubuntu 12.04 LTS and above) of these distributions are
fully supported. Any other Ubuntu based distributions are partially
supported.

Contribute
~~~~~~~~~~

If you want to contribute to Dragonfire then please read `this
guide <https://github.com/DragonComputer/Dragonfire/blob/master/CONTRIBUTING.md>`__.
