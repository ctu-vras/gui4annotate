#!/usr/bin/env python3

from gi.repository import Gtk, GObject
from gui_annotate.constants import Constants


class GuiToolbar(Gtk.Toolbar):

    def __init__(self, app, *args, **kwargs):
        Gtk.Toolbar.__init__(self, *args, **kwargs)

        self.app = app

        self.setup_stateop()
        self.setup_scaleop()
        self.setup_fileop()

    def setup_stateop(self):
        move_button = Gtk.RadioButton.new()
        move_button.add(Gtk.Image.new_from_stock('gtk-missing-image', Gtk.IconSize.LARGE_TOOLBAR))
        move_button.connect('toggled', lambda _: self.app.set_property('state', Constants.STATE_MOVE))
        move_button.set_property('draw-indicator', False)
        move_item = Gtk.ToolItem.new()
        move_item.add(move_button)

        add_button = Gtk.RadioButton.new_from_widget(move_button)
        add_button.add(Gtk.Image.new_from_stock('gtk-add', Gtk.IconSize.LARGE_TOOLBAR))
        add_button.connect('toggled', lambda _: self.app.set_property('state', Constants.STATE_ADD))
        add_button.set_property('draw-indicator', False)
        add_button.set_active(True)
        add_item = Gtk.ToolItem.new()
        add_item.add(add_button)

        delete_button = Gtk.RadioButton.new_from_widget(move_button)
        delete_button.add(Gtk.Image.new_from_stock('gtk-delete', Gtk.IconSize.LARGE_TOOLBAR))
        delete_button.connect('toggled', lambda _: self.app.set_property('state', Constants.STATE_REMOVE))
        delete_button.set_property('draw-indicator', False)
        delete_item = Gtk.ToolItem.new()
        delete_item.add(delete_button)

        self.insert(delete_item, 0)
        self.insert(add_item, 0)
        self.insert(move_item, 0)
        self.insert(Gtk.SeparatorToolItem.new(), 0)

    def setup_scaleop(self):
        zoom_out_button = Gtk.ToolButton.new(Gtk.Image.new_from_icon_name('zoom-out', Gtk.IconSize.LARGE_TOOLBAR), None)
        zoom_out_button.connect('clicked', lambda _: self.app.set_property('zoom', self.app.zoom + Constants.ZOOM_STEP) if self.app.zoom + Constants.ZOOM_STEP <= Constants.MAX_ZOOM else None)
        self.app.connect('notify::zoom', lambda w, _: zoom_out_button.set_sensitive(False) if w.zoom >= Constants.MAX_ZOOM else zoom_out_button.set_sensitive(True))
        zoom_out_button.set_sensitive(False)

        scale = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, Constants.MIN_ZOOM, Constants.MAX_ZOOM, Constants.ZOOM_STEP)
        scale.set_inverted(True)
        scale.add_mark(1, Gtk.PositionType.TOP, None)
        scale.add_mark(2, Gtk.PositionType.TOP, None)
        scale.add_mark(3, Gtk.PositionType.TOP, None)
        scale.add_mark(4, Gtk.PositionType.TOP, None)
        scale.add_mark(5, Gtk.PositionType.TOP, None)
        scale.set_size_request(150, 24)
        scale.set_draw_value(False)
        scale.set_value(Constants.INIT_ZOOM)
        scale.connect('value-changed', lambda s: self.app.set_property('zoom', int(round(s.get_value()))))
        self.app.connect('notify::zoom', lambda w, _: scale.set_value(w.zoom))
        scale_button = Gtk.ToolItem.new()
        scale_button.add(scale)

        zoom_in_button = Gtk.ToolButton.new(Gtk.Image.new_from_icon_name('zoom-in', Gtk.IconSize.LARGE_TOOLBAR), None)
        zoom_in_button.connect('clicked', lambda _: self.app.set_property('zoom', self.app.zoom - Constants.ZOOM_STEP) if self.app.zoom - Constants.ZOOM_STEP >= Constants.MIN_ZOOM else None)
        self.app.connect('notify::zoom', lambda w, _: zoom_in_button.set_sensitive(False) if w.zoom <= Constants.MIN_ZOOM else zoom_in_button.set_sensitive(True))

        self.insert(zoom_in_button, 0)
        self.insert(scale_button, 0)
        self.insert(zoom_out_button, 0)
        self.insert(Gtk.SeparatorToolItem.new(), 0)

    def setup_fileop(self):
        filechooser = Gtk.FileChooserButton.new("Please choose a folder", Gtk.FileChooserAction.SELECT_FOLDER)
        filechooser.connect('file-set', lambda w: self.app.set_property('folder', w.get_filename()))
        filechooser_button = Gtk.ToolItem.new()
        filechooser_button.add(filechooser)

        save_button = Gtk.ToolButton.new(Gtk.Image.new_from_icon_name('gtk-save', Gtk.IconSize.LARGE_TOOLBAR), 'Save')
        save_button.connect('clicked', lambda _: self.app.emit('save', False))
        save_button.set_sensitive(False)
        self.app.connect('notify::can-save', lambda w, _: save_button.set_sensitive(w.can_save))

        save_all_button = Gtk.ToolButton.new(Gtk.Image.new_from_icon_name('gtk-save-as', Gtk.IconSize.LARGE_TOOLBAR), 'Save all')
        save_all_button.connect('clicked', lambda _: self.app.emit('save', True))
        save_all_button.set_sensitive(False)
        self.app.connect('notify::can-save-all', lambda w, _: save_all_button.set_sensitive(w.can_save_all))

        prev_button = Gtk.ToolButton.new(Gtk.Image.new_from_icon_name('go-previous', Gtk.IconSize.LARGE_TOOLBAR), None)
        prev_button.connect('clicked', lambda _: self.app.emit('prev-im', True))
        prev_button.set_sensitive(False)
        self.app.connect('notify::can-prev', lambda w, _: prev_button.set_sensitive(w.can_prev))

        next_button = Gtk.ToolButton.new(Gtk.Image.new_from_icon_name('go-next', Gtk.IconSize.LARGE_TOOLBAR), None)
        next_button.connect('clicked', lambda _: self.app.emit('next-im', True))
        next_button.set_sensitive(False)
        self.app.connect('notify::can-next', lambda w, _: next_button.set_sensitive(w.can_next))

        self.insert(next_button, 0)
        self.insert(prev_button, 0)
        self.insert(Gtk.SeparatorToolItem.new(), 0)

        self.insert(save_all_button, 0)
        self.insert(save_button, 0)
        self.insert(filechooser_button, 0)