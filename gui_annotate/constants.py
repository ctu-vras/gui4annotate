#!/usr/bin/env python3

from gi.repository import Gdk, GObject, Gtk

from gui_annotate.vec import Vec2D


class Constants:
    INIT_MIN_AREA = 10
    INIT_MAX_AREA = 100
    INIT_RED = False
    INIT_GREEN = True
    INIT_BLUE = False

    INIT_MIN_COLOR = [0, 0, 0]
    INIT_MAX_COLOR = [255, 100, 255]

    ZOOM_STEP = 1
    MIN_ZOOM = 1
    INIT_MAX_ZOOM = 5
    INIT_ZOOM = 5

    INIT_SIZE = Vec2D(800, 600)
    PADDING = Vec2D(6, 6)

    LEFT_BUTTON = 1
    RIGHT_BUTTON = 3

    STATE_MOVE = 0
    STATE_ADD = 1
    STATE_REMOVE = 2
    STATE_ANNO = 3
    
    DEFAULT_STATE = STATE_ADD

    CURSOR_MOVE = None
    CURSOR_DRAW = None
    CURSOR_DELETE = None
    CURSOR_RESIZE = None

    RESIZE_TOLERATION = 10
    CORNER_PART = 0.25

    TOP = 0
    TOP_RIGHT = 1
    RIGHT = 2
    BOTTOM_RIGHT = 3
    BOTTOM = 4
    BOTTOM_LEFT = 5
    LEFT = 6
    TOP_LEFT = 7
    CENTER = 8

    IMAGE_EXT = ['.png', '.jpg', '.jpeg', '.bmp']
    DEFAULT_ANNOTATION = 'Blyskacek'

    IMAGE = 0
    FILE_ICON = 'image-x-generic'
    FOLDER = 1
    FOLDER_ICON = 'folder'
    ROI = 2
    ROI_ICON = 'gtk-index'

    ZOOM_OUT_ICON = Gtk.Image.new_from_icon_name('zoom-out', Gtk.IconSize.LARGE_TOOLBAR)
    ZOOM_IN_ICON = Gtk.Image.new_from_icon_name('zoom-in', Gtk.IconSize.LARGE_TOOLBAR)
    DELETE_ICON = Gtk.Image.new_from_stock('gtk-delete', Gtk.IconSize.LARGE_TOOLBAR)
    ADD_ICON = Gtk.Image.new_from_stock('gtk-add', Gtk.IconSize.LARGE_TOOLBAR)
    MOVE_ICON = Gtk.Image.new_from_icon_name('view-fullscreen', Gtk.IconSize.LARGE_TOOLBAR)
    ANNO_ICON = Gtk.Image.new_from_stock('gtk-zoom-fit', Gtk.IconSize.LARGE_TOOLBAR)
    SAVE_ICON = Gtk.Image.new_from_icon_name('gtk-save', Gtk.IconSize.LARGE_TOOLBAR)
    SAVE_ALL_ICON = Gtk.Image.new_from_icon_name('gtk-save-as', Gtk.IconSize.LARGE_TOOLBAR)
    PREV_ICON = Gtk.Image.new_from_icon_name('go-previous', Gtk.IconSize.LARGE_TOOLBAR)
    NEXT_ICON = Gtk.Image.new_from_icon_name('go-next', Gtk.IconSize.LARGE_TOOLBAR)
    ABOUT_DIALOG_ICON = Gtk.Image.new_from_stock('gtk-info', Gtk.IconSize.LARGE_TOOLBAR)
    HELP_DIALOG_ICON = Gtk.Image.new_from_stock('gtk-dialog-question', Gtk.IconSize.LARGE_TOOLBAR)
    DETECTOR_SETTINGS_ICON = Gtk.Image.new_from_stock('gtk-preferences', Gtk.IconSize.LARGE_TOOLBAR)
    DETECT_ICON = Gtk.Image.new_from_stock('gtk-new', Gtk.IconSize.LARGE_TOOLBAR)

    DEFAULT_TEXT_COLOR = Gdk.RGBA(0,0,0,0)
    UNSAVED_TEXT_COLOR = Gdk.RGBA(1,0,0,0)

    UNSELECTED_ROI_COLOR = (0, 0, 1)
    SELECTED_ROI_COLOR = (1, 0, 0)

#tree_inst, editable, color, icon_name, short_path/class_name, x-lt/#of ROIS, y-lt, x-rb, y-rb
    FOLDER_VIEW_ROW = (GObject.TYPE_PYOBJECT, bool, Gdk.RGBA, str, str, str, str, str, str)

    ROI_NAME = 0
    ROI_LTX = 1
    ROI_LTY = 2
    ROI_RBX = 3
    ROI_RBY = 4

    ROI_POINTS = [ROI_LTX, ROI_LTY, ROI_RBX, ROI_RBY]

    QUIT_DIALOG_TEXT = "Are you sure you want to quit? You still have some unsaved work."
    QUIT_DIALOG_TYPE = Gtk.MessageType.WARNING

    WEBSITE = "https://github.com/svobodat/gui4annotate"
    AUTHORS = ["Otakar Jašek - jasek.ota@gmail.com", None]
    PROG_NAME = "Gui4Annotate"
    COMMENTS = "Simple GUI tool for easy annotation of data"
    COPYRIGHT = "© Otakar Jašek, 2016"

    HELP_DIALOG_MSG = "Help and Keyboard shortcuts for " + PROG_NAME
    HELP_DIALOG_SECONDARY = """Workflow: Load a folder with images, add, modify or delete annotations and save them

<b>Toolbar buttons:</b>
    Load folder
    Save current image
    Save all annotations
    Previous image
    Next image
    Scale buttons plus scale
    Image manipulation modes
    Detector settings
    Detect
    Help
    About

<b>Keyboard shortcuts</b>
    <b>Ctrl + s</b> - Save current image
    <b>Ctrl + Shift + s</b> - Save all annotations
    <b>&#8592;</b> - Previous image
    <b>&#8594;</b> - Next image
    <b>&#8593;</b> - Previous annotation for image
    <b>&#8595;</b> - Next annotation for image
    <b>+</b> - Zoom in
    <b>-</b> - Zoom out
    <b>m</b> - Mode MOVE
    <b>a</b> - Mode ADD
    <b>r</b> - Mode REMOVE
    <b>i</b> - Create new default annotation for image
    <b>c</b> - Edit annotation
    <b>d</b> - Automatically detect ROIs
    <b>Ctrl + d</b> - Detector settings
    <b>Del</b> - Delete annotation
    <b>Tab</b> - Next field in editing mode
    <b>Ctrl + Tab</b> - Previous field in editing mode

More extensive guide can be found at https://github.com/svobodat/gui4annotate/blob/master/USAGE.md"""
