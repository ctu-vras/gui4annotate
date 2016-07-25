#!/usr/bin/env python3

from gi.repository import Gdk
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
