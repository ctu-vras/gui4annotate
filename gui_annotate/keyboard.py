#!/usr/bin/env python3

from gi.repository import Gdk

from gui_annotate.constants import Constants
from gui_annotate.tree import ImageNode, ROINode

class Keyboard:
    def __init__(self, app):
        self.app = app

        self.editing_row = None
        self.editable = None
        self.editing_col = -1

        self.folder_view = self.app.folder_view.folder_view
        self.app.connect('key-press-event', self.key_handler)

    def key_handler(self, _, event):
        keyname = Gdk.keyval_name(event.keyval)
        ctrl = bool(event.state & Gdk.ModifierType.CONTROL_MASK)
        shift = bool(event.state & Gdk.ModifierType.SHIFT_MASK)

        if self.editing_row is None:
            if ctrl and keyname == 's' and self.app.can_save and not shift:
                self.app.emit('save', False)
            if ctrl and shift and keyname == 'S' and self.app.can_save_all:
                self.app.emit('save', True)

            if keyname == 'Left' and self.app.can_prev:
                self.app.emit('prev-im', True)
            if keyname == 'Right' and self.app.can_next:
                self.app.emit('next-im', True)
            if keyname == 'Up':
                self.go_vertical(True)
            if keyname == 'Down':
                self.go_vertical(False)

            if keyname == 'plus' or keyname == 'KP_Add':
                self.try_zoom(True)
            if keyname == 'minus' or keyname == 'KP_Subtract':
                self.try_zoom(False)

            if keyname == 'm':
                self.app.state = Constants.STATE_MOVE
            if keyname == 'r':
                self.app.state = Constants.STATE_REMOVE
            if keyname == 'd':
                self.app.state = Constants.STATE_ADD

            if keyname == 'a' and self.app.current_im_node is not None:
                self.app.emit('append-roi', ('0,' * 4) + Constants.DEFAULT_ANNOTATION)
            if keyname == 'c':
                self.try_edit()

            if keyname == 'Delete':
                self.delete()
            return True
        else:
            if keyname == 'ISO_Left_Tab':
                self.change_edit(-1)
                return True
            if keyname == 'Tab':
                self.change_edit(1)
                return True

    def go_vertical(self, up):
        node = self.app.current_im_node
        if node is None:
            return
        path, column = self.folder_view.get_cursor()
        focus_node = self.folder_view.storage[path][0]
        if up and isinstance(focus_node, ImageNode):
            return
        if (not up) and isinstance(focus_node, ImageNode) and len(focus_node.children) == 0:
            return
        if up and isinstance(focus_node, ROINode):
            index = focus_node.parent.children.index(focus_node)
            if index > 0:
                nnode = focus_node.parent.children[index-1]
            else:
                nnode = focus_node.parent
            self.folder_view.set_focused_node(nnode)
            return
        if not up:
            if isinstance(focus_node, ImageNode):
                self.folder_view.set_focused_node(focus_node.children[0])
                return
            if isinstance(focus_node, ROINode):
                index = focus_node.parent.children.index(focus_node)
                if len(focus_node.parent.children) == index + 1:
                    return
                self.folder_view.set_focused_node(focus_node.parent.children[index+1])

    def try_zoom(self, zoom_in):
        zoom = self.app.zoom
        if zoom_in:
            if zoom - Constants.ZOOM_STEP >= self.app.area.min_zoom:
                self.app.zoom = zoom - Constants.ZOOM_STEP
        else:
            if zoom + Constants.ZOOM_STEP <= self.app.area.max_zoom:
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

    def change_edit(self, change):
        path = self.editing_row
        column = self.folder_view.get_column(self.editing_col + change)
        self.editable.editing_done()
        if column is not None:
            self.folder_view.set_cursor_on_cell(path, column, None, True)
        else:
            self.folder_view.set_cursor_on_cell(path, None, None, False)
