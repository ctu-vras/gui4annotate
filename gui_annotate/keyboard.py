#!/usr/bin/env python3

from gi.repository import Gdk

from gui_annotate.constants import Constants
from gui_annotate.tree import FolderNode, ImageNode, ROINode

class Keyboard:
    def __init__(self, app):
        self.app = app

        self.folder_view = self.app.folder_view.folder_view
        self.app.connect('key-press-event', self.key_handler)

    def key_handler(self, _, event):
        keyname = Gdk.keyval_name(event.keyval)
        print(keyname)
        ctrl = event.state & Gdk.ModifierType.CONTROL_MASK
        shift = event.state & Gdk.ModifierType.SHIFT_MASK

        if self.app.editing_row is None:
            if ctrl and keyname == 's' and self.app.can_save:
                self.app.emit('save', False)
                return True
            if ctrl and shift and keyname == 's' and self.app.can_save_all:
                self.app.emit('save', True)
                return True

            if keyname == 'Left' and self.app.can_prev:
                self.app.emit('prev-im', True)
                return True
            if keyname == 'Right' and self.app.can_next:
                self.app.emit('next-im', True)
                return True
            if keyname == 'Up':
                self.go_vertical(True)
                return True
            if keyname == 'Down':
                self.go_vertical(False)
                return True

            if keyname == 'plus' or keyname == 'KP_Add':
                self.try_zoom(True)
                return True
            if keyname == 'minus' or keyname == 'KP_Subtract':
                self.try_zoom(False)
                return True

            if keyname == 'm':
                self.app.state = Constants.STATE_MOVE
                return True
            if keyname == 'r':
                self.app.state = Constants.STATE_REMOVE
                return True
            if keyname == 'd':
                self.app.state = Constants.STATE_ADD
                return True

            if keyname == 'a' and self.app.current_im_node is not None:
                self.app.emit('append-roi', ('0,' * 4) + Constants.DEFAULT_ANNOTATION)
                return True
            if keyname == 'c':
                self.try_edit()
                return True

            if keyname == 'Delete':
                self.delete()
                return True
        else:
            if keyname == 'Tab':
                self.next_edit()
                #return True

    def next_edit(self):
        pass

    def go_vertical(self, up):
        pass

    def try_zoom(self, zoom_in):
        zoom = self.app.zoom
        if zoom_in:
            if zoom - Constants.ZOOM_STEP >= Constants.MIN_ZOOM:
                self.app.zoom = zoom - Constants.ZOOM_STEP
        else:
            if zoom + Constants.ZOOM_STEP <= Constants.MAX_ZOOM:
                self.app.zoom = zoom + Constants.ZOOM_STEP

    def delete(self):
        node = self.app.current_im_node
        if node is None:
            return
        if len(node.children) == 0:
            return

        path, column = self.folder_view.get_cursor()
        focus_node = self.folder_view.storage[path][0]

        if isinstance(focus_node, ROINode):
            self.app.emit('remove-roi', focus_node)
            return
        if isinstance(focus_node, ImageNode):
            for child in reversed(focus_node.children):
                self.app.emit('remove-roi', child)

    def try_edit(self):
        node = self.app.current_im_node
        if node is None:
            return
        if len(node.children) == 0:
            return

        path, _ = self.folder_view.get_cursor()
        focus_node = self.folder_view.storage[path][0]
        column = self.folder_view.get_column(1)
        if isinstance(focus_node, ROINode):
            self.folder_view.set_cursor_on_cell(path, column, None, True)
        if isinstance(focus_node, ImageNode):
            child_path = self.folder_view.storage.get_path(focus_node.children[0].storage_handle)
            self.folder_view.set_cursor_on_cell(child_path, column, None, True)
