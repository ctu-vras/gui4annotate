#!/usr/bin/env python3

import enum

from gui_annotate.constants import Constants
from gui_annotate.vec import Vec2D
from abc import abstractmethod
from gi.repository import Gdk


class Direction:
    def __init__(self):
        self.cursor = None
        self.drawer = None

    @property
    @abstractmethod
    def cursor_name(self):
        pass

    def set_cursor(self, cursor):
        self.cursor = cursor

    def set_drawer(self, drawer):
        self.drawer = drawer

    @staticmethod
    @abstractmethod
    def inside_check(norm_vec):
        pass

    @staticmethod
    @abstractmethod
    def get_dist(mouse, roi):
        pass

    @abstractmethod
    def move_roi(self, mouse, roi):
        pass


class DirTop(Direction):
    @property
    def cursor_name(self):
        return Gdk.CursorType.TOP_SIDE

    @staticmethod
    def inside_check(norm_vec):
        return norm_vec.y < Constants.CORNER_PART and (Constants.CORNER_PART < norm_vec.x < 1 - Constants.CORNER_PART)

    def move_roi(self, mouse, roi):
        roi.update_bbox(Constants.ROI_LTY, mouse.y, self.drawer.app.folder_view.folder_view.storage)


    @staticmethod
    def get_dist(mouse, roi):
        return Vec2D.dist(mouse, Vec2D(mouse.x, roi.lt.y))


class DirLeft(Direction):
    @property
    def cursor_name(self):
        return Gdk.CursorType.LEFT_SIDE

    @staticmethod
    def inside_check(norm_vec):
        return norm_vec.x < Constants.CORNER_PART and (Constants.CORNER_PART < norm_vec.y < 1 - Constants.CORNER_PART)

    def move_roi(self, mouse, roi):
        pass

    @staticmethod
    def get_dist(mouse, roi):
        return Vec2D.dist(mouse, Vec2D(roi.lt.x, mouse.y))


class DirRight(Direction):
    @property
    def cursor_name(self):
        return Gdk.CursorType.RIGHT_SIDE

    @staticmethod
    def inside_check(norm_vec):
        return norm_vec.x > 1 - Constants.CORNER_PART and (Constants.CORNER_PART < norm_vec.y < 1 - Constants.CORNER_PART)

    def move_roi(self, mouse, roi):
        pass

    @staticmethod
    def get_dist(mouse, roi):
        return Vec2D.dist(mouse, Vec2D(roi.rb.x, mouse.y))


class DirBottom(Direction):
    @property
    def cursor_name(self):
        return Gdk.CursorType.BOTTOM_SIDE

    @staticmethod
    def inside_check(norm_vec):
        return norm_vec.y > 1 - Constants.CORNER_PART and (Constants.CORNER_PART < norm_vec.x < 1 - Constants.CORNER_PART)

    def move_roi(self, mouse, roi):
        pass

    @staticmethod
    def get_dist(mouse, roi):
        return Vec2D.dist(mouse, Vec2D(mouse.x, roi.rb.y))


class DirCenter(Direction):
    @property
    def cursor_name(self):
        return Gdk.CursorType.FLEUR

    @staticmethod
    def inside_check(norm_vec):
        return Constants.CORNER_PART < norm_vec < 1 - Constants.CORNER_PART

    def move_roi(self, mouse, roi):
        pass

    @staticmethod
    def get_dist(mouse, roi):
        return Vec2D.dist(mouse, (roi.lt + roi.rb)/2)


class DirBottomRight(Direction):
    @property
    def cursor_name(self):
        return Gdk.CursorType.BOTTOM_RIGHT_CORNER

    @staticmethod
    def inside_check(norm_vec):
        return norm_vec > 1 - Constants.CORNER_PART

    def move_roi(self, mouse, roi):
        pass

    @staticmethod
    def get_dist(mouse, roi):
        return Vec2D.dist(mouse, roi.rb)


class DirBottomLeft(Direction):
    @property
    def cursor_name(self):
        return Gdk.CursorType.BOTTOM_LEFT_CORNER

    @staticmethod
    def inside_check(norm_vec):
        return norm_vec.x < Constants.CORNER_PART and norm_vec.y > 1 - Constants.CORNER_PART

    def move_roi(self, mouse, roi):
        pass

    @staticmethod
    def get_dist(mouse, roi):
        return Vec2D.dist(mouse, Vec2D(roi.lt.x, roi.rb.y))


class DirTopRight(Direction):
    @property
    def cursor_name(self):
        return Gdk.CursorType.TOP_RIGHT_CORNER

    @staticmethod
    def inside_check(norm_vec):
        return norm_vec.x > 1 - Constants.CORNER_PART and norm_vec.y < Constants.CORNER_PART

    def move_roi(self, mouse, roi):
        pass

    @staticmethod
    def get_dist(mouse, roi):
        return Vec2D.dist(mouse, Vec2D(roi.rb.x, roi.lt.x))


class DirTopLeft(Direction):
    @property
    def cursor_name(self):
        return Gdk.CursorType.TOP_LEFT_CORNER

    @staticmethod
    def inside_check(norm_vec):
        return norm_vec < Constants.CORNER_PART

    def move_roi(self, mouse, roi):
        pass

    @staticmethod
    def get_dist(mouse, roi):
        return Vec2D.dist(mouse, roi.lt)


class DirEnum(enum.Enum):
    top_left = DirTopLeft()
    top_right = DirTopRight()
    bottom_left = DirBottomLeft()
    bottom_right = DirBottomRight()
    left = DirLeft()
    right = DirRight()
    top = DirTop()
    bottom = DirBottom()
    center = DirCenter()

