#!/usr/bin/env python3

from gi.repository import Gtk, GObject
from gui_annotate.constants import Constants


class GuiToolbar(Gtk.Toolbar):

    __gsignals__ = {'prev-im' : (GObject.SIGNAL_RUN_FIRST, None, (bool,)), 'next-im': (GObject.SIGNAL_RUN_FIRST, None, (bool,)), 'save': (GObject.SIGNAL_RUN_FIRST, None, (bool,))}
    can_save = GObject.property(type = bool, default = False, flags = GObject.PARAM_READWRITE)
    can_save_all = GObject.property(type=bool, default=False, flags=GObject.PARAM_READWRITE)
    can_next = GObject.property(type=bool, default=False, flags=GObject.PARAM_READWRITE)
    can_prev = GObject.property(type=bool, default=False, flags=GObject.PARAM_READWRITE)
    folder = GObject.property(type = str, default = None, flags = GObject.PARAM_READWRITE)
    zoom = GObject.property(type = int, default = Constants.INIT_ZOOM, flags = GObject.PARAM_READWRITE)
    state = GObject.property(type = int, default = Constants.DEFAULT_STATE, flags = GObject.PARAM_READWRITE)

    def __init__(self, *args, **kwargs):
        Gtk.Toolbar.__init__(self, *args, **kwargs)

        self.filechooser = Gtk.FileChooserButton.new("Please choose a folder", Gtk.FileChooserAction.SELECT_FOLDER)
        self.filechooser.connect('file-set', lambda widget: self.set_property('folder', widget.get_filename()))
        self.filechooser_button = Gtk.ToolItem.new()
        self.filechooser_button.add(self.filechooser)

        self.save_button = Gtk.ToolButton.new(Gtk.Image.new_from_icon_name('gtk-save', Gtk.IconSize.LARGE_TOOLBAR), 'Save')
        self.save_button.connect('clicked', lambda _: self.emit('save', False))
        self.save_button.set_sensitive(False)
        self.connect('notify::can-save', lambda w, _: self.save_button.set_sensitive(w.can_save))

        self.save_all_button = Gtk.ToolButton.new(Gtk.Image.new_from_icon_name('gtk-save-as', Gtk.IconSize.LARGE_TOOLBAR), 'Save all')
        self.save_all_button.connect('clicked', lambda _:self.emit('save', True))
        self.save_all_button.set_sensitive(False)
        self.connect('notify::can-save-all', lambda w, _: self.save_all_button.set_sensitive(w.can_save_all))

        self.prev_button = Gtk.ToolButton.new(Gtk.Image.new_from_icon_name('go-previous', Gtk.IconSize.LARGE_TOOLBAR), None)
        self.prev_button.connect('clicked', lambda _: self.emit('prev-im', True))
        self.prev_button.set_sensitive(False)
        self.connect('notify::can-prev', lambda w, _: self.prev_button.set_sensitive(w.can_prev))

        self.next_button = Gtk.ToolButton.new(Gtk.Image.new_from_icon_name('go-next', Gtk.IconSize.LARGE_TOOLBAR), None)
        self.next_button.connect('clicked', lambda _: self.emit('next-im', True))
        self.next_button.set_sensitive(False)
        self.connect('notify::can-next', lambda w, _: self.next_button.set_sensitive(w.can_next))

        self.zoom_out_button = Gtk.ToolButton.new(Gtk.Image.new_from_icon_name('zoom-out', Gtk.IconSize.LARGE_TOOLBAR), None)
        self.zoom_out_button.connect('clicked', lambda _: self.set_zoom(self.zoom + Constants.ZOOM_STEP) if self.zoom + Constants.ZOOM_STEP <= Constants.MAX_ZOOM else None)

        self.scale = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, Constants.MIN_ZOOM, Constants.MAX_ZOOM, Constants.ZOOM_STEP)
        self.scale.set_inverted(True)
        self.scale.add_mark(1, Gtk.PositionType.TOP, None)
        self.scale.add_mark(2, Gtk.PositionType.TOP, None)
        self.scale.add_mark(3, Gtk.PositionType.TOP, None)
        self.scale.add_mark(4, Gtk.PositionType.TOP, None)
        self.scale.add_mark(5, Gtk.PositionType.TOP, None)
        self.scale.set_size_request(150, 24)
        self.scale.set_draw_value(False)
        self.scale.connect('value-changed', lambda scale: self.set_zoom(int(round(scale.get_value()))))
        self.scale_button = Gtk.ToolItem.new()
        self.scale_button.add(self.scale)

        self.zoom_in_button = Gtk.ToolButton.new(Gtk.Image.new_from_icon_name('zoom-in', Gtk.IconSize.LARGE_TOOLBAR), None)
        self.zoom_in_button.connect('clicked', lambda _: self.set_zoom(self.zoom - Constants.ZOOM_STEP) if self.zoom - Constants.ZOOM_STEP >= Constants.MIN_ZOOM else None)

        self.move_button = Gtk.RadioButton.new()
        self.move_button.add(Gtk.Image.new_from_stock('gtk-missing-image', Gtk.IconSize.LARGE_TOOLBAR))
        self.move_button.connect('toggled', lambda _: self.set_state(Constants.STATE_MOVE))
        self.move_button.set_property('draw-indicator', False)
        self.move_item = Gtk.ToolItem.new()
        self.move_item.add(self.move_button)

        self.add_button = Gtk.RadioButton.new_from_widget(self.move_button)
        self.add_button.add(Gtk.Image.new_from_stock('gtk-add', Gtk.IconSize.LARGE_TOOLBAR))
        self.add_button.connect('toggled', lambda _: self.set_state(Constants.STATE_ADD))
        self.add_button.set_property('draw-indicator', False)
        self.add_item = Gtk.ToolItem.new()
        self.add_item.add(self.add_button)

        self.delete_button = Gtk.RadioButton.new_from_widget(self.move_button)
        self.delete_button.add(Gtk.Image.new_from_stock('gtk-delete', Gtk.IconSize.LARGE_TOOLBAR))
        self.delete_button.connect('toggled', lambda _: self.set_state(Constants.STATE_REMOVE))
        self.delete_button.set_property('draw-indicator', False)
        self.delete_item = Gtk.ToolItem.new()
        self.delete_item.add(self.delete_button)

        self.insert(self.delete_item, 0)
        self.insert(self.add_item, 0)
        self.insert(self.move_item, 0)
        self.insert(Gtk.SeparatorToolItem.new(), 0)

        self.insert(self.zoom_in_button, 0)
        self.insert(self.scale_button, 0)
        self.insert(self.zoom_out_button, 0)
        self.insert(Gtk.SeparatorToolItem.new(), 0)

        self.insert(self.next_button, 0)
        self.insert(self.prev_button, 0)
        self.insert(Gtk.SeparatorToolItem.new(), 0)

        self.insert(self.save_all_button, 0)
        self.insert(self.save_button, 0)
        self.insert(self.filechooser_button, 0)

        self.set_zoom(Constants.INIT_ZOOM)
        self.add_button.set_active(True)

    def set_zoom(self, zoom):
        self.set_property('zoom', zoom)
        self.scale.set_value(zoom)
        if zoom <= Constants.MIN_ZOOM:
            self.zoom_in_button.set_sensitive(False)
            if zoom < Constants.MIN_ZOOM:
                self.set_zoom(Constants.MIN_ZOOM)
        else:
            self.zoom_in_button.set_sensitive(True)

        if zoom >= Constants.MAX_ZOOM:
            self.zoom_out_button.set_sensitive(False)
            if zoom > Constants.MAX_ZOOM:
                self.set_zoom(Constants.MAX_ZOOM)
        else:
            self.zoom_out_button.set_sensitive(True)

    def set_state(self, state):
        self.set_property('state', state)
