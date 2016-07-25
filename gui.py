#!/usr/bin/env python3

from gi.repository import Gtk, GObject, GdkPixbuf, Gdk
import os
from gui_annotate.drawer import Drawer
from gui_annotate.constants import Constants
from gui_annotate.vec import Vec2D
from gui_annotate.toolbar import GuiToolbar


class Gui4Annotate(Gtk.Window):
    __gsignals__ = { 'folder_load' : (GObject.SIGNAL_RUN_FIRST, None, (str, ))}

    def __init__(self):
        Gtk.Window.__init__(self, title='Gui for annotation')
        self.connect('delete-event', Gtk.main_quit)

        self.current_im = '/home/otaj/files/blyskacci/StassenC_soubory-blI_sk_u_ek/1_21.4/21.4/IMG_3264.JPG'

        self.grid = Gtk.Grid()

        self.toolbar = GuiToolbar()
        self.area = Drawer()

        self.grid.attach(self.toolbar, 0,0,3,1)
        self.grid.attach(self.area, 1,1,2,2)
        self.add(self.grid)

        self.toolbar.connect('notify::state', lambda w, _: self.area.set_state(w.state))


if __name__ == '__main__':
    app = Gui4Annotate()
    app.show_all()
    Gtk.main()
