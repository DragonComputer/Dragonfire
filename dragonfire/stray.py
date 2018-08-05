#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: stray
    :platform: Unix
    :synopsis: the top-level submodule of Dragonfire that contains the classes and methods related to Dragonfire's system tray icon.

.. moduleauthor:: Mehmet Mert Yıldıran <mert.yildiran@bil.omu.edu.tr>
"""

import os  # Miscellaneous operating system interfaces

TRAY_TOOLTIP = 'System Tray Icon'
TRAY_ICON = '/usr/share/icons/hicolor/48x48/apps/dragonfire_icon.png'
TRAY_ICON_ALT = 'debian/dragonfire_icon.png'
DEVELOPMENT_DIR = os.path.abspath(
    os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)) + '/'
global_event_holder = ''


class SystemTrayIcon:
    """Class to display a system tray icon.
    """

    def __init__(self):
        """Initialization method of :class:`dragonfire.stray.SystemTrayIcon` class.
        """

        import gi
        gi.require_version('Gtk', '3.0')
        from gi.repository import Gtk
        self.Gtk = Gtk

        self.icon = self.Gtk.StatusIcon()
        self.icon.set_title("Dragonfire")
        if os.path.isfile(TRAY_ICON):
            self.icon.set_from_file(TRAY_ICON)
        else:
            self.icon.set_from_file(DEVELOPMENT_DIR + TRAY_ICON_ALT)
        self.icon.connect('popup-menu', self.popup_menu)
        self.Gtk.main()

    def exit(self, data=None):
        """Method to exit the system tray icon.

        Keyword Args:
            data :  *Unknown*
        """

        self.Gtk.main_quit()
        global global_event_holder
        global_event_holder.set()

    def popup_menu(self, icon, button, time):
        """Method to display a popup menu whenever user clicked to the system tray icon.

        Args:
            icon:       Icon instance.
            button:     Button instance.
            time:       Timestamp.
        """

        self.menu = self.Gtk.Menu()

        menuitemDragonfire = self.Gtk.MenuItem(label="Dragonfire")
        self.menu.append(menuitemDragonfire)
        menuitemDragonfire.set_sensitive(False)

        menuitemSeperator = self.Gtk.SeparatorMenuItem()
        self.menu.append(menuitemSeperator)

        menuitemExit = self.Gtk.MenuItem(label="Exit")
        menuitemExit.connect_object("activate", self.exit, "Exit")
        self.menu.append(menuitemExit)
        self.menu.show_all()

        self.menu.popup(None, None, None, None, button, time)


def SystemTrayExitListenerSet(e):
    """Method to set an event listener for system tray icon exit.

    Args:
        e:  Event.
    """

    global global_event_holder
    global_event_holder = e


def SystemTrayInit():
    """Method to create a :class:`dragonfire.stray.SystemTrayIcon` instance with the purpose of displaying to system tray icon.
    """

    SystemTrayIcon()
