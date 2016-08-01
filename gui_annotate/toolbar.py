#!/usr/bin/env python3

from gi.repository import Gtk

from gui_annotate.constants import Constants


class GuiToolbar(Gtk.Toolbar):

    def __init__(self, app, *args, **kwargs):
        Gtk.Toolbar.__init__(self, *args, **kwargs)

        self.app = app

        self.setup_dialogs()
        self.setup_stateop()
        self.setup_scaleop()
        self.setup_fileop()

    def setup_dialogs(self):
        help_button = Gtk.ToolButton.new(Constants.HELP_DIALOG_ICON, None)
        help_button.connect('clicked', lambda _: self.app.emit('help-dialog', True))
        help_button.set_tooltip_text('Help')

        about_button = Gtk.ToolButton.new(Constants.ABOUT_DIALOG_ICON, None)
        about_button.connect('clicked', lambda _: self.app.emit('about-dialog', True))
        about_button.set_tooltip_text('About')

        self.insert(help_button, 0)
        self.insert(about_button, 0)
        self.insert(Gtk.SeparatorToolItem.new(), 0)

    def setup_stateop(self):

        def set_state(state, button):
            if state != button.state:
                return
            if button.get_active():
                return
            button.set_active(True)

        move_button = Gtk.RadioButton.new()
        move_button.state = Constants.STATE_MOVE
        move_button.add(Constants.MOVE_ICON)
        move_button.connect('toggled', lambda _: self.app.set_property('state', Constants.STATE_MOVE))
        move_button.set_property('draw-indicator', False)
        self.app.connect('notify::state', lambda w, _: set_state(w.state, move_button))
        move_item = Gtk.ToolItem.new()
        move_item.add(move_button)
        move_item.set_tooltip_text('Mode MOVING')

        add_button = Gtk.RadioButton.new_from_widget(move_button)
        add_button.state = Constants.STATE_ADD
        add_button.add(Constants.ADD_ICON)
        add_button.connect('toggled', lambda _: self.app.set_property('state', Constants.STATE_ADD))
        add_button.set_property('draw-indicator', False)
        self.app.connect('notify::state', lambda w, _: set_state(w.state, add_button))
        add_button.set_active(True)
        add_item = Gtk.ToolItem.new()
        add_item.add(add_button)
        add_item.set_tooltip_text('Mode DRAWING')

        delete_button = Gtk.RadioButton.new_from_widget(move_button)
        delete_button.state = Constants.STATE_REMOVE
        delete_button.add(Constants.DELETE_ICON)
        delete_button.connect('toggled', lambda _: self.app.set_property('state', Constants.STATE_REMOVE))
        delete_button.set_property('draw-indicator', False)
        self.app.connect('notify::state', lambda w, _: set_state(w.state, delete_button))
        delete_item = Gtk.ToolItem.new()
        delete_item.add(delete_button)
        delete_item.set_tooltip_text('Mode REMOVING')

        self.insert(delete_item, 0)
        self.insert(add_item, 0)
        self.insert(move_item, 0)
        self.insert(Gtk.SeparatorToolItem.new(), 0)

    def setup_scaleop(self):
        zoom_out_button = Gtk.ToolButton.new(Constants.ZOOM_OUT_ICON, None)
        zoom_out_button.connect('clicked', lambda _: self.app.set_property('zoom', self.app.zoom + Constants.ZOOM_STEP) if self.app.zoom + Constants.ZOOM_STEP <= Constants.MAX_ZOOM else None)
        self.app.connect('notify::zoom', lambda w, _: zoom_out_button.set_sensitive(False) if w.zoom >= Constants.MAX_ZOOM else zoom_out_button.set_sensitive(True))
        zoom_out_button.set_sensitive(False)
        zoom_out_button.set_tooltip_text('Zoom out')

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

        zoom_in_button = Gtk.ToolButton.new(Constants.ZOOM_IN_ICON, None)
        zoom_in_button.connect('clicked', lambda _: self.app.set_property('zoom', self.app.zoom - Constants.ZOOM_STEP) if self.app.zoom - Constants.ZOOM_STEP >= Constants.MIN_ZOOM else None)
        self.app.connect('notify::zoom', lambda w, _: zoom_in_button.set_sensitive(False) if w.zoom <= Constants.MIN_ZOOM else zoom_in_button.set_sensitive(True))
        zoom_in_button.set_tooltip_text('Zoom in')

        self.insert(zoom_in_button, 0)
        self.insert(scale_button, 0)
        self.insert(zoom_out_button, 0)
        self.insert(Gtk.SeparatorToolItem.new(), 0)

    def setup_fileop(self):
        filechooser = Gtk.FileChooserButton.new("Please choose a folder", Gtk.FileChooserAction.SELECT_FOLDER)
        filechooser.connect('file-set', lambda w: self.app.set_property('folder', w.get_filename()) if self.app.folder is not w.get_filename() else None)
        filechooser_button = Gtk.ToolItem.new()
        filechooser_button.add(filechooser)
        filechooser_button.set_tooltip_text('Choose a folder')

        save_button = Gtk.ToolButton.new(Constants.SAVE_ICON, None)
        save_button.connect('clicked', lambda _: self.app.emit('save', False))
        save_button.set_sensitive(False)
        self.app.connect('notify::can-save', lambda w, _: save_button.set_sensitive(w.can_save))
        save_button.set_tooltip_text('Save current file')

        save_all_button = Gtk.ToolButton.new(Constants.SAVE_ALL_ICON, None)
        save_all_button.connect('clicked', lambda _: self.app.emit('save', True))
        save_all_button.set_sensitive(False)
        self.app.connect('notify::can-save-all', lambda w, _: save_all_button.set_sensitive(w.can_save_all))
        save_all_button.set_tooltip_text('Save all changes')

        prev_button = Gtk.ToolButton.new(Constants.PREV_ICON, None)
        prev_button.connect('clicked', lambda _: self.app.emit('prev-im', True))
        prev_button.set_sensitive(False)
        self.app.connect('notify::can-prev', lambda w, _: prev_button.set_sensitive(w.can_prev))
        prev_button.set_tooltip_text('Previous image')

        next_button = Gtk.ToolButton.new(Constants.NEXT_ICON, None)
        next_button.connect('clicked', lambda _: self.app.emit('next-im', True))
        next_button.set_sensitive(False)
        self.app.connect('notify::can-next', lambda w, _: next_button.set_sensitive(w.can_next))
        next_button.set_tooltip_text('Next image')

        self.insert(next_button, 0)
        self.insert(prev_button, 0)
        self.insert(Gtk.SeparatorToolItem.new(), 0)

        self.insert(save_all_button, 0)
        self.insert(save_button, 0)
        self.insert(filechooser_button, 0)