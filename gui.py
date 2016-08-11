#!/usr/bin/env python3

from gi.repository import Gtk, GObject, Gdk

import gui_annotate.dialogs as dialogs
from gui_annotate.constants import Constants
from gui_annotate.detector import Detector
from gui_annotate.drawer import Drawer
from gui_annotate.keyboard import Keyboard
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
                    'next-im': (GObject.SIGNAL_RUN_FIRST, None, (bool,)),
                    'set-editing': (GObject.SIGNAL_RUN_FIRST, None, (GObject.TYPE_PYOBJECT, GObject.TYPE_PYOBJECT)),
                    'help-dialog': (GObject.SIGNAL_RUN_FIRST, None, (bool,)),
                    'about-dialog': (GObject.SIGNAL_RUN_FIRST, None, (bool,)),
                    'draw-change-size': (GObject.SIGNAL_RUN_FIRST, None, (int, int)),
                    'change-zoom-range': (GObject.SIGNAL_RUN_FIRST, None, (int, int)),
                    'detect-settings': (GObject.SIGNAL_RUN_FIRST, None, (bool,)),
                    'detect': (GObject.SIGNAL_RUN_FIRST, None, (bool,))
                    }

    def __init__(self):
        Gtk.Window.__init__(self, title='Gui for annotation')
        self.connect('delete-event', self.quit)
        self.connect('realize', self.setup)
        self.connect('help-dialog', lambda w, e: dialogs.help_dialog(self))
        self.connect('about-dialog', lambda w, e: dialogs.about_dialog(self))
        self.connect('size-allocate', self.allocate)

        self.keyboard = None
        self.grid = Gtk.Grid()
        self.width = 0
        self.height = 0

        self.area = Drawer(self)
        self.detector = Detector(self)
        self.toolbar = GuiToolbar(self)
        self.folder_view = FolderScrolledView(self)
        self.grid.attach(self.toolbar, 0,0,2,1)
        self.grid.attach(self.area, 1,1,1,1)
        self.grid.attach(self.folder_view, 0,1,1,1)
        self.add(self.grid)

    def setup(self, _):
        display = Gdk.Display.get_default()
        try:
            Constants.CURSOR_DELETE = Gdk.Cursor.new_from_name(display, 'not-allowed')
        except TypeError:
            Constants.CURSOR_DELETE = Gdk.Cursor.new_for_display(display, Gdk.CursorType.X_CURSOR)
        Constants.CURSOR_DRAW = Gdk.Cursor.new_for_display(display, Gdk.CursorType.CROSSHAIR)
        Constants.CURSOR_MOVE = Gdk.Cursor.new_for_display(display, Gdk.CursorType.FLEUR)
        self.keyboard = Keyboard(self)

    def allocate(self, _, allocation):
        change = False
        if allocation.width != self.width:
            self.width = allocation.width
            change = True
        if allocation.height != self.height:
            self.height = allocation.height
            change = True
        if change:
            self.change_sizes()

    def change_sizes(self):
        tool_height = self.toolbar.get_allocation().height
        cur_draw_height = self.height - tool_height
        cur_draw_width = int((cur_draw_height - Constants.PADDING.y * 2) * 4/3 + Constants.PADDING.y * 2)
        folder_width = self.width - cur_draw_width
        self.folder_view.set_size_request(folder_width, cur_draw_height)
        self.emit('draw-change-size', cur_draw_width, cur_draw_height)

    def quit(self, w, e):
        if not self.can_save_all:
            Gtk.main_quit(w, e)
            return False
        dialog = Gtk.MessageDialog(parent=self, type=Constants.QUIT_DIALOG_TYPE, buttons=Gtk.ButtonsType.YES_NO, message_format=Constants.QUIT_DIALOG_TEXT)
        response = dialog.run()
        if response == Gtk.ResponseType.YES:
            dialog.destroy()
            Gtk.main_quit(w, e)
            return False
        else:
            dialog.destroy()
            return True


if __name__ == '__main__':
    app = Gui4Annotate()
    app.show_all()
    Gtk.main()
