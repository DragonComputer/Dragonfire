from __future__ import print_function
import sys
import os

if sys.version_info[0] < 3:
    import gtk
else:
    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk as gtk

TRAY_TOOLTIP = 'System Tray Icon'
TRAY_ICON = '/usr/share/icons/hicolor/48x48/apps/dragonfire_icon.png'
TRAY_ICON_ALT = 'debian/dragonfire_icon.png'
DEVELOPMENT_DIR = os.path.abspath(
    os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)) + '/'
global_event_holder = ''


def exit(data=None):
    gtk.main_quit()
    global_event_holder.set()

def make_menu(event_button, event_time, data=None):
    menu = gtk.Menu()
    dragon_item = gtk.MenuItem("Dragonfire")
    sep_item = gtk.SeparatorMenuItem()
    exit_item = gtk.MenuItem("Exit")

    #Append the menu items
    menu.append(dragon_item)
    menu.append(sep_item)
    menu.append(exit_item)
    #add callbacks
    exit_item.connect_object("activate", exit, "Exit")
    #Show the menu items
    dragon_item.show()
    dragon_item.set_sensitive(False)
    sep_item.show()
    exit_item.show()

    #Popup the menu
    menu.popup(None, None, None, event_button, event_time)

def on_right_click(data, event_button, event_time):
    make_menu(event_button, event_time)

def SystemTrayExitListenerSet(e):
    global global_event_holder
    global_event_holder = e


def SystemTrayInit():
    os.close(1)  # close C's stdout stream
    os.close(2)  # close C's stderr stream
    if os.path.isfile(TRAY_ICON):
        icon = gtk.status_icon_new_from_file(TRAY_ICON)
    else:
        icon = gtk.status_icon_new_from_file(DEVELOPMENT_DIR + TRAY_ICON_ALT)
    icon.connect('popup-menu', on_right_click)
    gtk.main()


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
