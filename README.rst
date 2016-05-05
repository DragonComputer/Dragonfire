Dragonfire
==========

Dragonfire is an open source virtual assistant project for Ubuntu based
Linux distributions

*Dragonfire will never leave your questions unanswered.*

Dragonfire does following tasks for each separate command, respectively:

-  Search across the built-in commands of Dragonfire
-  Explore A.L.I.C.E. AIML
-  Run Wikipedia Answering Machine

Version
~~~~~~~

0.7.4

Installation
~~~~~~~~~~~~

.. code:: Shell

	sudo pip install dragonfire

Usage
~~~~~

.. code:: Shell

	dragonfire

To activate Dragonfire say *DRAGONFIRE* or *HEY* or *WAKE UP*.

To deactivate her say *GO TO SLEEP*.

To silence her say *ENOUGH*.

To kill her say *GOODBYE* or *BYE BYE* or *SEE YOU LATER*.

Built-in Commands
^^^^^^^^^^^^^^^^^

::

	DRAGONFIRE / WAKE UP / HEY
	GO TO SLEEP
	ENOUGH
	WHO AM I / SAY MY NAME
	MY TITLE IS LADY / I'M A LADY / I'M A WOMAN / I'M A GIRL
	MY TITLE IS SIR / I'M A MAN / I'M A BOY
	WHAT IS YOUR NAME
	WHAT IS YOUR GENDER
	FILE MANAGER / OPEN FILES
	WEB BROWSER
	OPEN BLENDER
	PHOTOSHOP / PHOTO EDITOR
	INKSCAPE
	VIDEO EDITOR
	OPEN CAMERA
	OPEN CALENDAR
	OPEN CALCULATOR
	OPEN STEAM
	SOFTWARE CENTER
	OFFICE SUITE
	OPEN WRITER
	OPEN MATH
	OPEN IMPRESS
	OPEN DRAW
	SHUT DOWN THE COMPUTER
	GOODBYE / BYE BYE / SEE YOU LATER
	SEARCH * (IN/USING) WIKIPEDA
	SEARCH * (IN/USING) YOUTUBE

For generating .dict and .dfa files from .grammer and .voca files(for developers only), use:
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

.. code:: Shell

	cd Dragonfire/dragonfire/
	mkdfa sample
