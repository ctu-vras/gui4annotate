#!/usr/bin/env python3

from gi.repository import Gtk, GObject, GdkPixbuf, Gdk
from gui_annotate.drawer import Drawer
from gui_annotate.constants import Constants
from gui_annotate.toolbar import GuiToolbar
from gui_annotate.tree import FolderScrolledView


class Gui4Annotate(Gtk.Window):

    current_im_node = GObject.property(type=GObject.TYPE_PYOBJECT, flags=GObject.PARAM_READWRITE)
    zoom = GObject.property(type=int, default=Constants.INIT_ZOOM, flags=GObject.PARAM_READWRITE)
    can_save = GObject.property(type=bool, default=False, flags=GObject.PARAM_READWRITE)
    can_save_all = GObject.property(type=bool, default=False, flags=GObject.PARAM_READWRITE)
    can_prev = GObject.property(type=bool, default=False, flags=GObject.PARAM_READWRITE)
    can_next = GObject.property(type=bool, default=False, flags=GObject.PARAM_READWRITE)
    folder = GObject.property(type=str, default='', flags=GObject.PARAM_READWRITE)
    state = GObject.property(type=int, default=Constants.STATE_ADD, flags=GObject.PARAM_READWRITE)

    __gsignals__ = {'save': (GObject.SIGNAL_RUN_FIRST, None, (bool,)),
                    'change-areas': (GObject.SIGNAL_RUN_FIRST, None, (bool,)),
                    'append-roi': (GObject.SIGNAL_RUN_FIRST, None, (str,)),
                    'remove-roi': (GObject.SIGNAL_RUN_FIRST, None, (GObject.TYPE_PYOBJECT,)),
                    'prev-im': (GObject.SIGNAL_RUN_FIRST, None, (bool,)),
                    'next-im': (GObject.SIGNAL_RUN_FIRST, None, (bool,))
                    }

    def __init__(self):
        Gtk.Window.__init__(self, title='Gui for annotation')
        self.connect('delete-event', Gtk.main_quit)

        self.grid = Gtk.Grid()

        self.toolbar = GuiToolbar(self)
        self.area = Drawer(self)
        self.folder_view = FolderScrolledView(self)

        self.grid.attach(self.toolbar, 0,0,2,1)
        self.grid.attach(self.area, 1,1,1,1)
        self.grid.attach(self.folder_view, 0,1,1,1)
        self.add(self.grid)


if __name__ == '__main__':
    app = Gui4Annotate()
    app.show_all()
    Gtk.main()
