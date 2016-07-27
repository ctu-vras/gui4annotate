#!/usr/bin/env python3
import functools
import math
import os
from abc import abstractmethod
from gi.repository import GdkPixbuf, Gtk
from gui_annotate.constants import Constants
from gui_annotate.vec import Vec2D


class SimpleTreeNode:
    def __init__(self, parent=None):
        if parent is not None:
            assert isinstance(parent, SimpleTreeNode)
            parent.children.append(self)
        self.parent = parent
        self.children = []
        self.type = -1
        self.changed = False
        self.storage_handle = None

    def any_unsaved(self):
        return any([child.changed for child in self.children])

    def set_changed(self, storage):
        self.changed = True
        storage.set_value(self.storage_handle, 2, Constants.UNSAVED_TEXT_COLOR)
        if self.parent is not None:
            self.parent.set_changed(storage)

    def set_saved(self, storage):
        self.changed = False
        storage.set_value(self.storage_handle, 2, Constants.DEFAULT_TEXT_COLOR)
        if self.parent is not None and not self.parent.any_unsaved():
            self.parent.set_saved(storage)

    @abstractmethod
    def save(self, storage):
        pass

    @abstractmethod
    def insert_to_storage(self, storage):
        pass


class FolderNode(SimpleTreeNode):

    @staticmethod
    def create_tree(path, storage, parent=None):
        node = FolderNode(path, storage, parent)
        all_files = sorted([os.path.join(path, f) for f in os.listdir(path)])
        dirs = [d for d in all_files if os.path.isdir(d)]
        files = [f for f in all_files if os.path.isfile(f) and os.path.splitext(f)[1].lower() in Constants.IMAGE_EXT]

        for d in dirs:
            FolderNode.create_tree(d, storage, node)
        for f in files:
            ImageNode.create_tree(f, storage, node)

        return node

    def __init__(self, full_path, storage, parent=None):
        if parent is not None:
            assert isinstance(parent, FolderNode)
        SimpleTreeNode.__init__(self, parent)
        self.type = Constants.FOLDER
        self.path = full_path
        self.insert_to_storage(storage)

    def insert_to_storage(self, storage):
        name = os.path.split(self.path)[1]
        data = (self, False, Constants.DEFAULT_TEXT_COLOR, Constants.FOLDER_ICON, name, '', '', '', '')
        self.storage_handle = storage.append(self.parent if self.parent is not None else None, data)

    def save(self, storage):
        if self.changed:
            for child in self.children:
                if child.changed:
                    child.save(storage)
            self.set_saved(storage)


class ImageNode(SimpleTreeNode):

    @staticmethod
    def create_tree(path, storage, parent):
        node = ImageNode(path, storage, parent)
        txt_file = os.path.splitext(path)[0] + '.txt'
        if os.path.isfile(txt_file):
            with open(txt_file, mode='r') as f:
                for line in f.readlines():
                    ROINode.create_tree(storage, node, line.strip())
        return node

    def __init__(self, full_path, storage, parent):
        assert isinstance(parent, FolderNode)
        SimpleTreeNode.__init__(self, parent)
        self.type = Constants.FILE
        self.path = full_path
        self.rois = 0
        self.size = None
        self.insert_to_storage(storage)

    def insert_to_storage(self, storage):
        name = os.path.split(self.path)[1]
        data = (self, False, Constants.DEFAULT_TEXT_COLOR, Constants.FILE_ICON, name,
                '<b>' + str(self.rois) + '</b>', '', '', '')
        self.storage_handle = storage.append(self.parent, data)

    def save(self, storage):
        if self.changed:
            data = functools.reduce(lambda x, y: x + str(y) + os.linesep, self.children, '')
            txt_path = os.path.splitext(self.path)[0] + '.txt'
            if data is not '':
                with open(txt_path, mode='w') as f:
                    f.write(data)
            else:
                os.remove(txt_path)
            self.set_saved(storage)
            for child in self.children:
                child.set_saved(storage)


class ROINode(SimpleTreeNode):

    @staticmethod
    def create_tree(storage, parent, roi_str):
        return ROINode(storage, parent, roi_str=roi_str)

    def __init__(self, storage, parent, cls=Constants.DEFAULT_ANNOTATION, lt=None, rb=None, roi_str=None, changed=False):
        assert isinstance(parent, ImageNode)
        assert (roi_str is not None) or (lt is not None and rb is not None)
        SimpleTreeNode.__init__(self, parent)
        self.type = Constants.ROI
        self.parent.rois += 1
        storage.set_value(self.parent.storage_handle, 5, '<b>' + str(self.parent.rois) + '</b>')
        if roi_str is None:
            self.cls = cls
            self.lt = lt
            self.rb = rb
        else:
            data = roi_str.split(',')
            self.cls = data[-1]
            roi_data = tuple(map(float, data[0:4]))
            self.lt = Vec2D(roi_data[0], roi_data[1])
            self.rb = Vec2D(roi_data[2], roi_data[3])
        self.insert_to_storage(storage)
        if changed:
            self.set_changed(storage)

    def insert_to_storage(self, storage):
        data = (self, True, Constants.DEFAULT_TEXT_COLOR, Constants.ROI_ICON, self.cls,
                '%.1f' % self.lt.x, '%.1f' % self.lt.y, '%.1f' % self.rb.x, '%.1f' % self.rb.y)
        self.storage_handle = (self.parent, data)

    def save(self, storage):
        pass

    def delete_node(self, storage):
        storage.remove(self.storage_handle)
        self.parent.rois -= 1
        storage.set_value(self.parent.storage_handle, 5, '<b>' + str(self.parent.rois) + '</b>')
        self.parent.set_changed(storage)
        storage.app.can_save_all = True
        if self.parent == storage.app.current_im_node:
            storage.app.can_save = True
        del self

    def update_cls(self, cls, storage):
        if cls == self.cls:
            return
        self.cls = cls
        storage.set_value(self.storage_handle, 4, self.cls)
        storage.app.can_save_all = True
        if self.parent == storage.app.current_im_node:
            storage.app.can_save = True
        self.set_changed(storage)

    def update_bbox(self, column, data, storage):
        try:
            data_f = float(data)
        except ValueError:
            return

        if math.isnan(data_f) or math.isinf(data_f):
            return
        if data_f < 0:
            data_f = 0

        if self.parent.size is None:
            pb = GdkPixbuf.Pixbuf.new_from_file(self.parent.path)
            self.parent.size = Vec2D(pb.get_width(), pb.get_height())

        if (column == Constants.ROI_LTX or column == Constants.ROI_RBX) and data_f > self.parent.size.x:
            data_f = self.parent.size.x
        if (column == Constants.ROI_LTY or column == Constants.ROI_RBY) and data_f > self.parent.size.y:
            data_f = self.parent.size.y

        if column == Constants.ROI_LTX:
            if self.lt.x == data_f:
                return
            self.lt.x = data_f
        if column == Constants.ROI_LTY:
            if self.lt.y == data_f:
                return
            self.lt.y = data_f
        if column == Constants.ROI_RBX:
            if self.rb.x == data_f:
                return
            self.rb.x = data_f
        if column == Constants.ROI_RBY:
            if self.rb.y == data_f:
                return
            self.rb.y = data_f

        nlt = Vec2D.allmin(self.lt, self.rb)
        nrb = Vec2D.allmax(self.lt, self.rb)

        self.lt = nlt
        self.rb = nrb

        roi_f = [nlt.x, nlt.y, nrb.x, nrb.y]
        roi_s = list(map(lambda x: '%.1f' % x, roi_f))

        storage.set(self.storage_handle, [5, 6, 7, 8], roi_s)
        storage.app.emit('change-areas', True)
        storage.app.can_save_all = True
        if self.parent == storage.app.current_im_node:
            storage.app.can_save = True
        self.set_changed(storage)

    def __str__(self):
        return str(self.lt) + ',' + str(self.rb) + ',' + self.cls


class TreeStorage(Gtk.TreeStore):
    def __init__(self, app, *args, **kwargs):
        Gtk.TreeStore.__init__(self, *args, **kwargs)

        self.app = app
        self.tree_node = None
        self.app.connect('notify::folder', lambda w, _: self.set_folder(w.folder))
        self.app.connect('save', lambda _, save_all: self.save_handler(save_all))

    def set_folder(self, folder):
        self.tree_node = FolderNode.create_tree(folder, self)

    def save_handler(self, save_all):
        if save_all:
            self.tree_node.save(self)
            self.app.can_save_all = False
        else:
            self.app.current_im_node.save(self)
            if not self.tree_node.any_unsaved():
                self.app.can_save_all = False
        self.app.can_save = False


class FolderView(Gtk.TreeView):
    def __init__(self, app, *args,**kwargs):
        Gtk.TreeView.__init__(self, *args, **kwargs)

        self.app = app
        self.storage = TreeStorage(self.app, *Constants.FOLDER_VIEW_ROW)
        self.set_model(self.storage)
        self.connect('row-activated', self.activated_row)
        self.set_property('activate-on-single-click', True)
        self.set_headers_visible(False)
        self.setup_columns()

    def setup_columns(self):
        icon_renderer = Gtk.CellRendererPixbuf.new()
        icon_column = Gtk.TreeViewColumn.new()
        icon_column.pack_start(icon_renderer, True)
        icon_column.add_attribute(icon_renderer, 'icon_name', 3)
        self.append_column(icon_column)

        name_renderer = Gtk.CellRendererText.new()
        name_column = Gtk.TreeViewColumn.new()
        name_column.pack_start(name_renderer, True)
        name_column.add_attribute(name_renderer, 'text', 4)
        name_column.add_attribute(name_renderer, 'editable', 1)
        name_column.add_attribute(name_renderer, 'foreground-rgba', 2)
        name_renderer.column = Constants.ROI_NAME
        name_renderer.connect('edited', self.edit_cell)
        self.append_column(name_column)

        for i in range(0, 4):
            roi_renderer = Gtk.CellRendererText.new()
            roi_column = Gtk.TreeViewColumn.new()
            roi_column.pack_start(roi_renderer, True)
            roi_column.add_attribute(roi_renderer, 'markup', i+5)
            roi_column.add_attribute(roi_renderer, 'edit   able', 1)
            roi_column.add_attribute(roi_renderer, 'foreground-rgba', 2)
            roi_renderer.column = Constants.ROI_POINTS[i]
            roi_renderer.connect('edited', self.edit_cell)
            self.append_column(roi_column)

    def activated_row(self, tree, path, _):
        node = self.storage[path][0]

        if node.type == Constants.FOLDER:
            if not self.row_expanded(path):
                self.expand_row(path, False)
            else:
                self.collapse_row(path, False)

        if node.type == Constants.FILE:
            self.app.current_im_node = node
            self.expand_row(path, False)

        if node.type == Constants.ROI:
            self.app.current_im_node = node.parent

    def edit_cell(self, cr, path, new_text):
        node = self.storage[path][0]

        if cr.column == Constants.ROI_NAME:
            node.update_cls(new_text, self.storage)
        else:
            node.update_bbox(cr.column, new_text, self.storage)


class FolderScrolledView(Gtk.ScrolledWindow):
    def __init__(self, app, *args, **kwargs):
        Gtk.ScrolledWindow.__init__(self, *args, **kwargs)

        self.app = app
        self.folder_view = FolderView(app)
        self.add(self.folder_view)
        self.set_size_request(500, 612)
        self.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
