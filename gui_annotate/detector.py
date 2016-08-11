#!/usr/bin/env python3
import copy
import struct

import numpy as np
import scipy.ndimage
from gi.repository import Gtk

from gui_annotate.constants import Constants
from gui_annotate.vec import Vec2D


class DetectorSettings:
    def __init__(self, app, detector):
        self.app = app
        self.red = Constants.INIT_RED
        self.green = Constants.INIT_GREEN
        self.blue = Constants.INIT_BLUE

        self.min_color = Constants.INIT_MIN_COLOR
        self.max_color = Constants.INIT_MAX_COLOR

        self.min_area = Constants.INIT_MIN_AREA
        self.max_area = Constants.INIT_MAX_AREA

        self.parent = detector

    def show_dialog(self):
        def check_sensitivity():
            red = switch_red.get_active()
            green = switch_green.get_active()
            blue = switch_blue.get_active()
            red_sense = not(red and not (green or blue))
            green_sense = not(green and not(red or blue))
            blue_sense = not(blue and not(red or green))
            switch_red.set_sensitive(red_sense)
            switch_blue.set_sensitive(blue_sense)
            switch_green.set_sensitive(green_sense)
            min_red.set_sensitive(red)
            min_green.set_sensitive(green)
            min_blue.set_sensitive(blue)
            max_red.set_sensitive(red)
            max_green.set_sensitive(green)
            max_blue.set_sensitive(blue)

        def set_active_color(w, color):
            active = w.get_active()
            setattr(self, color, active)
            check_sensitivity()

        def change_color(button, mmtype, color, change):
            ind = ['red', 'green', 'blue'].index(color)
            value = button.get_value()
            arr = getattr(self, mmtype + '_color')
            arr[ind] = value
            if mmtype == 'min' and self.min_color[ind] > self.max_color[ind]:
                self.max_color[ind] = value
                change.set_value(value)
            if mmtype == 'max' and self.max_color[ind] < self.min_color[ind]:
                self.min_color[ind] = value
                change.set_value(value)

        names_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        label_red = Gtk.Label('Red')
        label_green = Gtk.Label('Green')
        label_blue = Gtk.Label('Blue')
        names_box.pack_start(label_red, True, True, 0)
        names_box.pack_start(label_green, True, True, 0)
        names_box.pack_start(label_blue, True, True, 0)

        switch_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        switch_red = Gtk.Switch()
        switch_red.connect_after('notify::active', lambda w, _: set_active_color(w, 'red'))

        switch_green = Gtk.Switch()
        switch_green.connect_after('notify::active', lambda w, _: set_active_color(w, 'green'))

        switch_blue = Gtk.Switch()
        switch_blue.connect_after('notify::active', lambda w, _: set_active_color(w, 'blue'))

        switch_box.pack_start(switch_red, True, True, 0)
        switch_box.pack_start(switch_green, True, True, 0)
        switch_box.pack_start(switch_blue, True, True, 0)

        min_color_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        max_color_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)

        min_red = Gtk.SpinButton.new_with_range(0, 255, 1)
        min_red.set_value(self.min_color[0])
        min_red.connect('value-changed', lambda w: change_color(w, 'min', 'red', max_red))
        min_color_box.pack_start(min_red, True, True, 0)

        min_green = Gtk.SpinButton.new_with_range(0, 255, 1)
        min_green.set_value(self.min_color[1])
        min_green.connect('value-changed', lambda w: change_color(w, 'min', 'green', max_green))
        min_color_box.pack_start(min_green, True, True, 0)

        min_blue = Gtk.SpinButton.new_with_range(0, 255, 1)
        min_blue.set_value(self.min_color[2])
        min_blue.connect('value-changed', lambda w: change_color(w, 'min', 'blue', max_blue))
        min_color_box.pack_start(min_blue, True, True, 0)

        max_red = Gtk.SpinButton.new_with_range(0, 255, 1)
        max_red.set_value(self.max_color[0])
        max_red.connect('value-changed', lambda w: change_color(w, 'max', 'red', min_red))
        max_color_box.pack_start(max_red, True, True, 0)

        max_green = Gtk.SpinButton.new_with_range(0, 255, 1)
        max_green.set_value(self.max_color[1])
        max_green.connect('value-changed', lambda w: change_color(w, 'max', 'green', min_green))
        max_color_box.pack_start(max_green, True, True, 0)

        max_blue = Gtk.SpinButton.new_with_range(0, 255, 1)
        max_blue.set_value(self.max_color[2])
        max_blue.connect('value-changed', lambda w: change_color(w, 'max', 'blue', min_blue))
        max_color_box.pack_start(max_blue, True, True, 0)

        switch_red.set_active(self.red)
        switch_green.set_active(self.green)
        switch_blue.set_active(self.blue)
        check_sensitivity()

        min_area_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        max_area_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)

        min_area_box.pack_start(Gtk.Label('Minimal detection size:'), True, True, 0)
        min_spin = Gtk.SpinButton.new_with_range(1, 49, 1)
        min_spin.set_value(self.min_area)
        min_spin.connect('value-changed', lambda w: setattr(self, 'min_area', w.get_value()))
        min_area_box.pack_start(min_spin, True, True, 0)

        max_area_box.pack_start(Gtk.Label('Maximal detection size:'), True, True, 0)
        max_spin = Gtk.SpinButton.new_with_range(50, 3000, 1)
        max_spin.set_value(self.max_area)
        max_spin.connect('value-changed', lambda w: setattr(self, 'max_area', w.get_value()))
        max_area_box.pack_start(max_spin, True, True, 0)

        listbox = Gtk.ListBox()
        listbox.set_selection_mode(Gtk.SelectionMode.NONE)

        listbox.add(names_box)
        listbox.add(switch_box)
        listbox.add(Gtk.Label('Minimal color values'))
        listbox.add(min_color_box)
        listbox.add(Gtk.Label('Maximal color values'))
        listbox.add(max_color_box)
        listbox.add(min_area_box)
        listbox.add(max_area_box)

        diag = Gtk.Dialog(parent=self.app)
        diag.get_content_area().add(listbox)
        diag.add_button('Save', Gtk.ResponseType.ACCEPT)
        diag.add_button('Cancel', Gtk.ResponseType.CANCEL)
        diag.set_modal(True)
        settings = copy.deepcopy(self)
        listbox.show_all()

        response = diag.run()
        if response != Gtk.ResponseType.ACCEPT:
            self.red = settings.red
            self.green = settings.green
            self.blue = settings.blue
            self.min_color = settings.min_color
            self.max_color = settings.max_color
            self.min_area = settings.min_area
            self.max_area = settings.max_area
        diag.destroy()

    def __deepcopy__(self, memo):
        settings = DetectorSettings(self.app, self.parent)
        copyable = ['red', 'green', 'blue', 'min_color', 'max_color', 'min_area', 'max_area']
        for attr in copyable:
            setattr(settings, attr, copy.deepcopy(getattr(self, attr), memo))
        return settings


class Detector():
    def __init__(self, app):
        self.app = app
        self.settings = DetectorSettings(app, self)
        self.app.connect('detect-settings', lambda w, e: self.settings.show_dialog())
        self.app.connect('detect', lambda w, e: self.detect())

    def detect(self):
        node = self.app.current_im_node
        if node is None:
            return
        if node.data is None:
            node.data = struct.unpack(str(3 * node.size.x * node.size.y) + 'B', node.pb.get_pixels())
        if node.pix_data is None:
            node.pix_data = np.array(node.data).reshape((node.size.y, node.size.x, 3))
        data = np.ones((node.size.y, node.size.x))
        if self.settings.red:
            data *= np.where((node.pix_data[:,:,0] >= self.settings.min_color[0]) & (node.pix_data[:,:,0] <= self.settings.max_color[0]), 1, 0)
        if self.settings.green:
            data *= np.where((node.pix_data[:,:,1] >= self.settings.min_color[1]) & (node.pix_data[:,:,1] <= self.settings.max_color[1]), 1, 0)
        if self.settings.blue:
            data *= np.where((node.pix_data[:,:,2] >= self.settings.min_color[2]) & (node.pix_data[:,:,2] <= self.settings.max_color[2]), 1, 0)
        labeled, num = scipy.ndimage.label(data, structure=np.ones((3, 3)))
        objects = scipy.ndimage.find_objects(labeled)
        for obj in objects:
            y, x = obj
            if not ((self.settings.min_area <= (x.stop - x.start) <= self.settings.max_area) and (self.settings.min_area <= (y.stop - y.start) <= self.settings.max_area)):
                continue
            lt = Vec2D(x.start, y.start)
            rb = Vec2D(x.stop, y.stop)
            if (lt, rb) not in node:
                self.app.emit('append-roi', str(lt) + ',' + str(rb) + ',' + Constants.DEFAULT_ANNOTATION)
        self.app.area.queue_draw()

