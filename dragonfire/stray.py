import wx
import os

TRAY_TOOLTIP = 'System Tray Demo'
TRAY_ICON = '/usr/share/icons/hicolor/48x48/apps/dragonfire_icon.png'
TRAY_ICON_ALT = 'debian/dragonfire_icon.png'

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
            self.set_icon(os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)) + '/' + TRAY_ICON_ALT)
        self.Bind(wx.EVT_TASKBAR_LEFT_DOWN, self.on_left_down)

    def CreatePopupMenu(self):
        menu = wx.Menu()
        create_menu_item(menu, 'Say Hello', self.on_hello)
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

class App(wx.App):
    def OnInit(self):
        frame=wx.Frame(None)
        self.SetTopWindow(frame)
        TaskBarIcon(frame)
        return True


def SystemTrayInit():
    app = App(False)
    app.MainLoop()
    print "ARE YOU NON-BLOCKING?"


if __name__ == '__main__':
    SystemTrayInit()
