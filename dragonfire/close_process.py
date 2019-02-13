#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: close_process
    :platform: Unix
    :synopsis: the top-level submodule of dragonfire that contains the functions related to Dragonfire's simple if-else struct of command line ability.

.. moduleauthors:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""


def close(h, userin):
    """Method to dragonfire's command structure for close the open programs on command line ability

    Args:
        h:                         doc helper from __init__.py
        userin:                    :class:`ava.utilities.TextToAction` instance.
    """

    if h.check_verb_lemma("close") or h.check_adj_lemma("close") or h.check_verb_lemma("stop"):
        if h.check_text("blender"):
            """
            blender:                 For All
            """
            cmds = [["blender"]]
            return executes(cmds, "Blender", userin)
        if h.check_text("draw") or h.check_text("impress") or h.check_text("math") or h.check_text("writer") or (h.check_noun_lemma("office") and h.check_noun_lemma("suite")):
            """
            soffice.bin:                   For All LibreOffice Process
            """
            cmds = [["soffice.bin"]]
            return executes(cmds, "LibreOffice", userin)
        if h.check_text("gimp") or (h.check_noun_lemma("photo") and (h.check_noun_lemma("editor") or h.check_noun_lemma("shop"))):
            """
            gimp:                   For All
            """
            cmds = [["gimp"]]
            return executes(cmds, "Gimp", userin)
        if h.check_text("inkscape") or (h.check_noun_lemma("vector") and h.check_noun_lemma("graphic")) or (h.check_text("vectorial") and h.check_text("drawing")):
            """
            gimp:                   For All
            """
            cmds = [["inkscape"]]
            return executes(cmds, "Inkscape", userin)
        if h.check_text("kdenlive") or (h.check_noun_lemma("video") and h.check_noun_lemma("editor")):
            """
            kdenlive:               For All
            """
            cmds = [["kdenlive"]]
            return executes(cmds, "Kdenlive", userin)
        if h.check_noun_lemma("browser") or h.check_text("chrome") or h.check_text("firefox"):
            """ All of them for all OS
            firefox:
            chromium:
            chrome:
            opera:
            safari:
            """
            cmds = [["firefox"], ["chromium-browse"], ["chrome"], ["opera"], ["safari"]]
            return executes(cmds, "Browser", userin)
        if h.check_text("steam"):
            """
            steam:                  For All
            """
            cmds = [["steam"]]
            return executes(cmds, "Steam", userin)
        if h.check_text("files") or (h.check_noun_lemma("file") and h.check_noun_lemma("manager")):
            """
            dolphin:                For KDE neon
            pantheon-files  :       For elementary OS
            nautilus:               For ubuntu
            nemo:                   For Linux Mint
            """
            cmds = [["dolphin"], ["pantheon-files"], ["nautilus"], ["nemo"]]
            return executes(cmds, "File Manager", userin)
        if h.check_noun_lemma("camera"):
            """
            kamoso:                 For KDE neon
            snap-photobooth:        For elementary OS
            cheese:                 For ubuntu
            """
            cmds = [["kamoso"], ["snap-photobooth"], ["cheese"]]
            return executes(cmds, "Camera", userin)
        if h.check_noun_lemma("calendar"):
            """
            korganizer:             For KDE neon
            maya-calendar:          For elementary OS
            orage:                  For ubuntu
            gnome-calendar:         For ubuntu & Linux Mint
            """
            cmds = [["korganizer"], ["maya-calendar"], ["orage"], ["gnome-calendar"]]
            return executes(cmds, "Calendar", userin)
        if h.check_noun_lemma("calculator"):
            """
            kcalc:                  For KDE neon
            pantheon-calculator:    For elementary OS
            gnome-calculator:       For Ubuntu
            """
            cmds = [["kcalc"], ["pantheon-calculator"], ["gnome-calculator"]]
            return executes(cmds, "Calculator", userin)
        if h.check_noun_lemma("software") and (h.check_text("center") or h.check_text("manager")):
            """
            plasma-discover:        For KDE neon
            software-center:        For elementary OS & Ubuntu
            mintinstall:            For Linux Mint
            """
            cmds = [["plasma-discover"], ["software-center"], ["mintinstall"]]
            return executes(cmds, "Software Center", userin)
        if h.check_noun_lemma("console"):  # for openin terminal.
            """
            konsole:               For KDE neon
            gnome-terminal:        For elementary OS & Ubuntu
            """
            cmds = [["konsole"], ["gnome-terminal"]]
            return executes(cmds, "Console", userin)
    return None


def executes(cmds, msg, userin):
    closed_msg = msg + " is not open"  # if there is more than one program exist for the same job in local, this will keep.
    for a in cmds:
        response = userin.execute(a, msg, False, 0, True)  # KDE neon
        if response == msg + " closed":
            closed_msg = response
    return userin.say(closed_msg)
