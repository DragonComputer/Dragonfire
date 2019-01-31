#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: directCliExecute
    :platform: Unix
    :synopsis: the top-level submodule of Dragonfire.commands that contains the classes related to Dragonfire's simple if-else struct of directly executed command on command line ability.

.. moduleauthors:: Mehmet Mert Yıldıran <mert.yildiran@bil.omu.edu.tr>
                   Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

from dragonfire.nlplib import Classifier, Helper  # Submodule of Dragonfire to handle extra NLP tasks

import spacy  # Industrial-strength Natural Language Processing in Python

nlp = spacy.load('en')  # Load en_core_web_sm, English, 50 MB, default model


class CliExecuteCommands():
    """Class to contains taking notes process with simply if-else struct.
    """

    def compare(self, com, userin, user_prefix):
        """Method to dragonfire's command structures of directly executed command on command line ability.

        Args:
            com (str):                 User's command.
            userin:                    :class:`dragonfire.utilities.TextToAction` instance.
            user_prefix:               user's preferred titles.
        """

        doc = nlp(com)
        h = Helper(doc)
        if h.check_verb_lemma("open") or h.check_adj_lemma("open") or h.check_verb_lemma("run") or h.check_verb_lemma(
                "start") or h.check_verb_lemma("show"):
            if h.check_text("blender"):
                userin.execute(["blender"], "Blender")
                return userin.say("Blender 3D computer graphics software")
            if h.check_text("draw"):
                userin.execute(["libreoffice", "--draw"], "LibreOffice Draw")
                return userin.say("Opening LibreOffice Draw")
            if h.check_text("impress"):
                userin.execute(["libreoffice", "--impress"], "LibreOffice Impress")
                return userin.say("Opening LibreOffice Impress")
            if h.check_text("math"):
                userin.execute(["libreoffice", "--math"], "LibreOffice Math")
                return userin.say("Opening LibreOffice Math")
            if h.check_text("writer"):
                userin.execute(["libreoffice", "--writer"], "LibreOffice Writer")
                return userin.say("Opening LibreOffice Writer")
            if h.check_text("gimp") or (
                    h.check_noun_lemma("photo") and (h.check_noun_lemma("editor") or h.check_noun_lemma("shop"))):
                userin.execute(["gimp"], "GIMP")
                return userin.say("Opening the photo editor software.")
            if h.check_text("inkscape") or (h.check_noun_lemma("vector") and h.check_noun_lemma("graphic")) or (
                    h.check_text("vectorial") and h.check_text("drawing")):
                userin.execute(["inkscape"], "Inkscape")
                return userin.say("Opening the vectorial drawing software.")
            if h.check_noun_lemma("office") and h.check_noun_lemma("suite"):
                userin.execute(["libreoffice"], "LibreOffice")
                return userin.say("Opening LibreOffice")
            if h.check_text("kdenlive") or (h.check_noun_lemma("video") and h.check_noun_lemma("editor")):
                userin.execute(["kdenlive"], "Kdenlive")
                return userin.say("Opening the video editor software.")
            if h.check_noun_lemma("browser") or h.check_text("chrome") or h.check_text("firefox"):
                userin.execute(["sensible-browser"], "Web Browser")
                return userin.say("Web browser")
            if h.check_text("steam"):
                userin.execute(["steam"], "Steam")
                return userin.say("Opening Steam Game Store")
            if h.check_text("files") or (h.check_noun_lemma("file") and h.check_noun_lemma("manager")):
                userin.execute(["dolphin"], "File Manager")  # KDE neon
                userin.execute(["pantheon-files"], "File Manager")  # elementary OS
                userin.execute(["nautilus", "--browser"], "File Manager")  # Ubuntu
                return userin.say("File Manager")
            if h.check_noun_lemma("camera"):
                userin.execute(["kamoso"], "Camera")  # KDE neon
                userin.execute(["snap-photobooth"], "Camera")  # elementary OS
                userin.execute(["cheese"], "Camera")  # Ubuntu
                return userin.say("Camera")
            if h.check_noun_lemma("calendar"):
                userin.execute(["korganizer"], "Calendar")  # KDE neon
                userin.execute(["maya-calendar"], "Calendar")  # elementary OS
                userin.execute(["orage"], "Calendar")  # Ubuntu
                return userin.say("Calendar")
            if h.check_noun_lemma("calculator"):
                userin.execute(["kcalc"], "Calculator")  # KDE neon
                userin.execute(["pantheon-calculator"], "Calculator")  # elementary OS
                userin.execute(["gnome-calculator"], "Calculator")  # Ubuntu
                return userin.say("Calculator")
            if h.check_noun_lemma("software") and h.check_text("center"):
                userin.execute(["plasma-discover"], "Software Center")  # KDE neon
                userin.execute(["software-center"], "Software Center")  # elementary OS & Ubuntu
                return userin.say("Software Center")
            if h.check_noun_lemma("console"):  # for openin terminal.
                userin.execute(["konsole"], "Terminal")  # KDE neon
                userin.execute(["gnome-terminal"], "Terminal")  # elementary OS & Ubuntu
                return userin.say("console")
        return None
