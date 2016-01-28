try:
    import clr
except:
    import sys
    import os
    libs = os.path.join(os.path.dirname(__file__), 'libs')
    sys.path.append(libs)
    import clr

# Add references to the need assemblies
clr.AddReference('Dwm')
clr.AddReference("System.Windows.Forms")

# Then we can import the .NET namespaces as if they were Python modules
# and we can use aliases.
from Dwm import ThumbnailEx as Thumb
from Dwm import DwmMessage as Msg
from Dwm import Win32
import System.Windows.Forms as WinForms
from System.Drawing import Rectangle, Size
import System

import MaxPlus

# We require the same trick as with Qt, or the Form will be GC'ed
class _GCProtector(object):
    widgets = []

class MainWindow(WinForms.Form):
    '''Our main window Form. We can inherit from any .NET class'''
    def __init__(self):
        ''' Constructor for the From '''
        self.TopMost = True  #  Access to class properties
        self.Height = 400
        # Adds to the static class to avoid garbage collection
        _GCProtector.widgets.append(self)
        # Registering for events is as easy as in normal C#
        self.Load += self.LoadEvent

    def LoadEvent(self, source, ev):
        ''' Here we start handling the DwmThumb for displaying on the form. '''
        vp = MaxPlus.ViewportManager.GetActiveViewportIndex() + 1
        self.Text = 'Viewport %s Clone' % vp
        
        self.thumb = Thumb(self.Handle, MaxPlus.Core.GetWindowHandle())
        print MaxPlus.Core.GetWindowHandle()
        self.thumb.SetSourceClientAreaOnly(True)

        # Register for active viewport changes
        MaxPlus.NotificationManager.Register(MaxPlus.NotificationCodes.ActiveViewportChanged, self.changedViewport)
        MaxPlus.NotificationManager.Register(MaxPlus.NotificationCodes.ViewportChange, self.updateViewport)
        self.menu = WinForms.ContextMenu()
        self.menuLock = WinForms.MenuItem("&Lock");
        self.menuLock.Checked = False
        self.menuLock.Click += self.lockViewport
        self.menu.MenuItems.Add(self.menuLock)
        self.ContextMenu = self.menu
        self.locked = False
        self.locked_id = 0
        # Register for resizing events
        self.Resize += self.resized
        self.resized(None, None)

    def lockViewport(self, source, evt):
        ''' Handle menu click. '''
        self.menuLock.Checked = self.locked = not self.menuLock.Checked
        self.locked_id = MaxPlus.ViewportManager.GetActiveViewportIndex()


    def changedViewport(self, code):
        ''' Handle active viewport changes. '''
        if self.locked:
            return
        vp = MaxPlus.ViewportManager.GetActiveViewportIndex() + 1
        self.Text = 'Viewport %s Clone' % vp
        self.updateThumb()

    def updateViewport(self, code):
        ''' Handle viewport changes. '''
        self.updateThumb()

    def updateThumb(self):
        hwnd = None
        if self.locked:
            hwnd = MaxPlus.ViewportManager.GetViewportByID(self.locked_id).GetHWnd()
        else:
            hwnd = MaxPlus.ViewportManager.GetActiveViewport().GetHWnd()
        r = Win32.GetWindowsRectangle(hwnd)
        r2 = Win32.GetWindowsRectangle(MaxPlus.Core.GetWindowHandle())
        r.X = r.X - r2.X
        r.Y = r.Y - r2.Y
        r.Width = r.Width - r2.X
        r.Height = r.Height - r2.Y
        self.thumb.SetDestinationRectangle(Rectangle(0, 0, self.Width-15, self.Height-20))
        self.thumb.SetSourceRectangle(r)

    def resized(self, source, ev):
        ''' Resized event. '''
        hwnd = MaxPlus.ViewportManager.GetActiveViewport().GetHWnd()
        r = Win32.GetWindowsRectangle(hwnd)
        ta = float(r.Width - r.X) / float(r.Height - r.Y)
        self.Size = Size(int(float(self.Height) * ta) - 30, self.Height)
        self.updateThumb()

    def OnClosing(self, event):
        ''' Override the OnClosing to handle cleanup. '''
        # Cleanup event handling, or things can get messy
        print 'Closing cloner'
        self.Load -= self.LoadEvent
        self.Resize -= self.resized
        MaxPlus.NotificationManager.Unregister(self.changedViewport)
        MaxPlus.NotificationManager.Unregister(self.updateViewport)
        self.thumb.Dispose()
        _GCProtector.widgets.remove(self)
        super(self).OnClose(event)

    def WndProc(self, m):
        ''' Override WndProc '''
        if Msg.DwmMessage(self.Handle, m):
            return
        super(MainWindow).WndProc(self, m)

# Creates main window
dialog = MainWindow()
dialog.Show()