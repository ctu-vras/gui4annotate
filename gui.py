#!/usr/bin/env python3

from gi.repository import Gtk, GObject, GdkPixbuf, Gdk
from gui_annotate.drawer import Drawer
from gui_annotate.constants import Constants
from gui_annotate.vec import Vec2D
from gui_annotate.toolbar import GuiToolbar
from gui_annotate.folder_view import FolderView


class Gui4Annotate(Gtk.Window):
    __gsignals__ = { 'folder_load' : (GObject.SIGNAL_RUN_FIRST, None, (str, ))}

    def __init__(self):
        Gtk.Window.__init__(self, title='Gui for annotation')
        self.connect('delete-event', Gtk.main_quit)

        self.grid = Gtk.Grid()

        self.toolbar = GuiToolbar()
        self.area = Drawer()
        self.folder_view = FolderView()

        self.grid.attach(self.toolbar, 0,0,2,1)
        self.grid.attach(self.area, 1,1,1,1)
        self.grid.attach(self.folder_view, 0,1,1,1)
        self.add(self.grid)

        self.toolbar.connect('notify::state', lambda w, _: self.area.set_state(w.state))
        self.toolbar.connect('notify::folder', lambda w, _: self.folder_view.set_property('folder', w.folder))

if __name__ == '__main__':
    app = Gui4Annotate()
    app.show_all()
    Gtk.main()
