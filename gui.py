#!/usr/bin/env python3

from gi.repository import Gtk, GObject, GdkPixbuf, Gdk
from gui_annotate.drawer import Drawer
from gui_annotate.constants import Constants
from gui_annotate.vec import Vec2D
from gui_annotate.toolbar import GuiToolbar
from gui_annotate.folder_view import FolderView


class Gui4Annotate(Gtk.Window):

    current_node = GObject.property(type=GObject.TYPE_PYOBJECT, flags=GObject.PARAM_READWRITE)
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
        self.toolbar.connect('notify::zoom', lambda w, _: self.area.set_zoom(w.zoom))
        self.toolbar.connect('save', lambda w, save_all: self.folder_view.data.save_handler(w, save_all, self))

        self.folder_view.connect('notify::current-im-node', lambda w, _: [None, self.area.set_image(w.current_im_node), self.set_property('current_node', w.current_im_node)][0])
        self.area.connect('append-roi', lambda _, parent, roi_data: self.append_roi(parent, roi_data))
        self.area.connect('remove-roi', lambda _, roi: self.folder_view.data.delete_roi(roi))
        self.area.connect('notify::can-save', lambda w, _: [None, self.toolbar.set_property('can_save', w.can_save), self.toolbar.set_property('can_save_all', True) if w.can_save else None][0])

    def append_roi(self, parent, roi_data):
        self.folder_view.data.append_custom(Constants.ROI, parent=parent, roi_data=roi_data, change=True)
        self.area.update_areas()
        self.folder_view.tree_view.expand_row(self.folder_view.data.get_path(parent.data['iter']), False)


if __name__ == '__main__':
    app = Gui4Annotate()
    app.show_all()
    Gtk.main()
