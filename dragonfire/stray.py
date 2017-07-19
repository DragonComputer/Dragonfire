import wx
import os

TRAY_TOOLTIP = 'System Tray Demo'
TRAY_ICON = '/usr/share/icons/hicolor/48x48/apps/dragonfire_icon.png'
TRAY_ICON_ALT = 'debian/dragonfire_icon.png'
DEVELOPMENT_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)) + '/'
global_event_holder = ''


def create_menu_item(menu, label, func):
    item = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    menu.AppendItem(item)
    return item

class TaskBarIcon(wx.TaskBarIcon):
    def __init__(self, frame):
        self.frame = frame
        super(TaskBarIcon, self).__init__()
        try:
            self.set_icon(TRAY_ICON)
        except:
            self.set_icon(DEVELOPMENT_DIR + TRAY_ICON_ALT)
        self.Bind(wx.EVT_TASKBAR_LEFT_DOWN, self.on_left_down)

    def CreatePopupMenu(self):
        menu = wx.Menu()
        menu_title = wx.MenuItem(menu, 0, 'Dragonfire')
        menu.AppendItem(menu_title)
        menu.Enable(menu_title.Id, enable=False)
        #create_menu_item(menu, 'Say Hello', self.on_hello)
        menu.AppendSeparator()
        create_menu_item(menu, 'Exit', self.on_exit)
        return menu

    def set_icon(self, path):
        icon = wx.IconFromBitmap(wx.Bitmap(path))
        self.SetIcon(icon, TRAY_TOOLTIP)

    def on_left_down(self, event):
        print 'Tray icon was left-clicked.'

    def on_hello(self, event):
        print 'Hello, world!'

    def on_exit(self, event):
        wx.CallAfter(self.Destroy)
        self.frame.Close()
        global_event_holder.set()

class App(wx.App):
    def OnInit(self):
        frame=wx.Frame(None)
        self.SetTopWindow(frame)
        TaskBarIcon(frame)
        return True

def SystemTrayExitListenerSet(e):
    global global_event_holder
    global_event_holder = e

def SystemTrayInit():
    os.close(1) # close C's stdout stream
    os.close(2) # close C's stderr stream
    app = App(False)
    app.MainLoop()


if __name__ == '__main__':
    DEVELOPMENT_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)) + '/'
    from multiprocessing import Process, Event
    import time
    e = Event()
    SystemTrayExitListenerSet(e)
    Process(target=SystemTrayInit).start()
    while (1):
        time.sleep(1)
        print e.is_set()
        if (e.is_set()):
            break
