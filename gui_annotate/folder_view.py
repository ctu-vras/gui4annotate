#!/usr/bin/env python3

from gi.repository import Gtk, GObject, Gdk
import os
from gui_annotate.vec import Vec2D
from gui_annotate.constants import Constants


class FolderStore(Gtk.TreeStore):
    def __init__(self, *args, **kwargs):
        Gtk.TreeStore.__init__(self, *args, **kwargs)

        self.roi_data = dict()

    def append_custom(self, type, full_path = None, parent = None, roi_data = None):
        if type is Constants.FOLDER:
            if full_path is None:
                raise ValueError('You need to specify path for folder')
            small_path = os.path.split(full_path)[1]
            return self.append(parent, (full_path, small_path, Constants.FOLDER_ICON, '', False, Constants.DEFAULT_TEXT_COLOR))
        if type is Constants.FILE:
            if full_path is None:
                raise ValueError('You need to specify path for file')
            if os.path.splitext(full_path)[1].lower() not in Constants.IMAGE_EXT:
                return None
            small_path = os.path.split(full_path)[1]
            self.roi_data[full_path] = list()
            file_append = self.append(parent, (full_path, small_path, Constants.FILE_ICON, '<b>'+str(len(self.roi_data[full_path]))+'</b>', False, Constants.DEFAULT_TEXT_COLOR))
            txt_file = os.path.splitext(full_path)[0] + '.txt'
            if os.path.isfile(txt_file):
                with open(txt_file, mode='r') as f:
                    for line in f.readlines():
                        self.append_custom(Constants.ROI, full_path=full_path, parent=file_append, roi_data=line.strip())
                self.set(file_append, [3], ['<b>'+str(len(self.roi_data[full_path]))+'</b>'])
            return file_append
        if type is Constants.ROI:
            data = roi_data.split(',')
            roi = tuple(map(float, data[0:4]))
            name = data[-1]
            print(name)
            self.roi_data[full_path].append((roi, name))
            roi = '(%.1f, %.1f, %.1f, %.1f)' % roi
            return self.append(parent, ('', name, Constants.ROI_ICON, roi, True, Constants.DEFAULT_TEXT_COLOR))


class FolderView(Gtk.ScrolledWindow):
    folder = GObject.property(type=str, default=None, flags=GObject.PARAM_READWRITE)

    def __init__(self, *args, **kwargs):
        Gtk.ScrolledWindow.__init__(self, *args, **kwargs)
        self.tree = Gtk.TreeView()
        # full_name, name/roi_type, folder/file/ROI, num_of_rois/roi, editable(only rois), foreground
        self.data = FolderStore(str, str, str, str, bool, Gdk.RGBA)
        self.tree.set_model(self.data)

        self.connect('notify::folder', lambda view, _: [None, self.data.clear(), self.set_folder(self.folder, self.data.append_custom(Constants.FOLDER, full_path=self.folder))][0])

        icon = Gtk.CellRendererPixbuf.new()
        icon_column = Gtk.TreeViewColumn.new()
        icon_column.pack_start(icon, True)
        icon_column.add_attribute(icon, 'icon_name', 2)
        self.tree.append_column(icon_column)

        name = Gtk.CellRendererText.new()
        name_column = Gtk.TreeViewColumn.new()
        name_column.pack_start(name, True)
        name_column.add_attribute(name, 'text', 1)
        name_column.add_attribute(name, 'editable', 4)
        name_column.add_attribute(name, 'foreground-rgba', 5)
        self.tree.append_column(name_column)

        roi_data = Gtk.CellRendererText.new()
        roi_data_column = Gtk.TreeViewColumn.new()
        roi_data_column.pack_start(roi_data, True)
        roi_data_column.add_attribute(roi_data, 'markup', 3)
        roi_data_column.add_attribute(roi_data, 'editable', 4)
        roi_data_column.add_attribute(roi_data, 'foreground-rgba', 5)
        self.tree.append_column(roi_data_column)

        self.tree.set_headers_visible(False)

        self.add(self.tree)
        self.set_size_request(500, 612)
        self.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)


    def set_folder(self, path, parent):
        all_files = sorted([os.path.join(path, f) for f in os.listdir(path)])
        dirs = [d for d in all_files if os.path.isdir(d)]
        files = [f for f in all_files if os.path.isfile(f)]

        for d in dirs:
            self.set_folder(d, self.data.append_custom(Constants.FOLDER, full_path=d, parent=parent))

        for f in files:
            self.data.append_custom(Constants.FILE, full_path=f, parent=parent)


def print_tree_store(store):
    rootiter = store.get_iter_first()
    print_rows(store, rootiter, "")

def print_rows(store, treeiter, indent):
    while treeiter != None:
        print(indent + str(store[treeiter][:]))
        if store.iter_has_child(treeiter):
            childiter = store.iter_children(treeiter)
            print_rows(store, childiter, indent + "\t")
        treeiter = store.iter_next(treeiter)