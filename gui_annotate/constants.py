#!/usr/bin/env python3

from gi.repository import Gdk, GObject
from gui_annotate.vec import Vec2D


class Constants:
    ZOOM_STEP = 1
    MIN_ZOOM = 1
    MAX_ZOOM = 5
    INIT_ZOOM = 5

    INIT_SIZE = Vec2D(800, 600)
    PADDING = Vec2D(6, 6)

    LEFT_BUTTON = 1
    RIGHT_BUTTON = 3

    STATE_MOVE = 0
    STATE_ADD = 1
    STATE_REMOVE = 2
    
    DEFAULT_STATE = STATE_ADD

    CURSOR_MOVE = Gdk.Cursor.new(Gdk.CursorType.FLEUR)
    CURSOR_DRAW = Gdk.Cursor.new(Gdk.CursorType.CROSSHAIR)
    CURSOR_DELETE = Gdk.Cursor.new(Gdk.CursorType.X_CURSOR)

    IMAGE_EXT = ['.png', '.jpg', '.jpeg', '.bmp']
    DEFAULT_ANNOTATION = 'Default bug'

    FILE = 0
    FILE_ICON = 'image-x-generic'
    FOLDER = 1
    FOLDER_ICON = 'folder'
    ROI = 2
    ROI_ICON = 'gtk-index'

    DEFAULT_TEXT_COLOR = Gdk.RGBA(0,0,0,0)
    UNSAVED_TEXT_COLOR = Gdk.RGBA(1,0,0,0)

#tree_inst, editable, color, icon_name, short_path/class_name, x-lt/#of ROIS, y-lt, x-rb, y-rb
    FOLDER_VIEW_ROW = (GObject.TYPE_PYOBJECT, bool, Gdk.RGBA, str, str, str, str, str, str)

    ROI_NAME = 0
    ROI_LTX = 1
    ROI_LTY = 2
    ROI_RBX = 3
    ROI_RBY = 4

    ROI_POINTS = [ROI_LTX, ROI_LTY, ROI_RBX, ROI_RBY]
