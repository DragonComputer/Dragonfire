from __future__ import print_function
import sys
import os

TRAY_TOOLTIP = 'System Tray Icon'
TRAY_ICON = '/usr/share/icons/hicolor/48x48/apps/dragonfire_icon.png'
TRAY_ICON_ALT = 'debian/dragonfire_icon.png'
DEVELOPMENT_DIR = os.path.abspath(
    os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)) + '/'
global_event_holder = ''

class SystemTrayIcon:

    def __init__(self):
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
        self.Gtk.main_quit()
        global global_event_holder
        global_event_holder.set()

    def popup_menu(self, icon, button, time):
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
    global global_event_holder
    global_event_holder = e


def SystemTrayInit():
    SystemTrayIcon()


if __name__ == '__main__':
    DEVELOPMENT_DIR = os.path.abspath(
        os.path.join(os.path.dirname(os.path.realpath(__file__)),
                     os.pardir)) + '/'
    from multiprocessing import Process, Event
    import time
    e = Event()
    SystemTrayExitListenerSet(e)
    Process(target=SystemTrayInit).start()
    while (1):
        time.sleep(1)
        print(e.is_set())
        if (e.is_set()):
            break
