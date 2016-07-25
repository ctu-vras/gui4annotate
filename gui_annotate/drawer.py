#!/usr/bin/env python3

from gi.repository import Gtk, Gdk, GdkPixbuf
from gui_annotate.vec import Vec2D
from gui_annotate.constants import Constants


class Drawer(Gtk.DrawingArea):

    def __init__(self):
        Gtk.DrawingArea.__init__(self)

        self.state = Constants.DEFAULT_STATE

        self.current_im = None
        self.current_pb = None
        self.current_surface = None

        self.pb_size = None

        self.current_areas = []

        self.current_zoom = Constants.INIT_ZOOM

        self.current_center = None
        self.current_lt = None
        self.im_area = None

        self.vp_size = Constants.INIT_SIZE
        self.pad = Constants.PADDING

        self.win_size = self.vp_size + self.pad * 2

        self.last_mouse = None

        self.set_size_request(self.win_size.x, self.win_size.y)
        self.connect('draw', self.draw)
        self.add_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        self.add_events(Gdk.EventMask.BUTTON_MOTION_MASK)
        self.add_events(Gdk.EventMask.BUTTON_RELEASE_MASK)
        self.add_events(Gdk.EventMask.ENTER_NOTIFY_MASK)
        self.add_events(Gdk.EventMask.LEAVE_NOTIFY_MASK)
        self.connect('button-press-event', self.button_press)
        self.connect('motion-notify-event', self.button_motion)
        self.connect('button-release-event', self.button_release)
        self.connect('enter-notify-event', lambda w, e: self.change_cursor(True))
        self.connect('leave-notify-event', lambda w, e: self.change_cursor(False))

    def change_cursor(self, enter):
        cursor = None
        if enter:
            if self.state == Constants.STATE_MOVE:
                cursor = Constants.CURSOR_MOVE
            if self.state == Constants.STATE_ADD:
                cursor = Constants.CURSOR_DRAW
            if self.state == Constants.STATE_REMOVE:
                cursor = Constants.CURSOR_DELETE
        self.get_window().set_cursor(cursor)

    def button_release(self, _, event):
        if event.type == Gdk.EventType.BUTTON_RELEASE and event.state & Gdk.ModifierType.BUTTON1_MASK:
            self.last_mouse = None

    def draw(self, _, ctx):
        if self.current_surface:
            ctx.set_source_surface(self.current_surface, self.current_lt.x, self.current_lt.y)
        else:
            ctx.set_source_rgb(1, 1, 1)

        ctx.paint()

        ctx.set_source_rgb(1,0,0)
        ctx.set_line_width(1)
        for area in self.current_areas:
            a0 = self.transform_pb_to_vp(area[0]) + self.pad
            a1 = self.transform_pb_to_vp(area[1]) + self.pad - a0
            ctx.rectangle(a0.x, a0.y, a1.x, a1.y)
            ctx.stroke()

        ctx.set_source_rgb(0, 0, 0)
        ctx.set_line_width(self.pad.x)
        ctx.rectangle(self.pad.x * 0.5, self.pad.y * 0.5, (self.vp_size + self.pad).x, (self.vp_size + self.pad).y)
        ctx.stroke()

    def set_state(self, val):
        self.state = val

    def button_press(self, _, event):
        if self.state == Constants.STATE_REMOVE and event.type == Gdk.EventType.BUTTON_PRESS and event.button == Constants.LEFT_BUTTON:
            mouse = self.transform_vp_to_pb(Vec2D(event.x, event.y) - self.pad)

            all_areas = self.current_areas
            self.current_areas = [area for area in self.current_areas if not (Vec2D.allmin(*area) <= mouse <= Vec2D.allmax(*area))]

            rm = list(set(all_areas) - set(self.current_areas))

            if len(rm):
                rm[:] = [vec for area in rm for vec in area]
                min_vec = self.transform_pb_to_vp(Vec2D.allmin(*rm))
                max_vec = self.transform_pb_to_vp(Vec2D.allmax(*rm)) - min_vec + self.pad * 2

                self.queue_draw_area(min_vec.x, min_vec.y, max_vec.x, max_vec.y)

    def button_motion(self, widget, event):
        if self.state == Constants.STATE_MOVE:
            if event.type == Gdk.EventType.MOTION_NOTIFY and event.state & Gdk.ModifierType.BUTTON1_MASK:
                mouse = Vec2D(event.x, event.y)
                self.move(mouse)
        if self.state == Constants.STATE_ADD:
            if event.type == Gdk.EventType.MOTION_NOTIFY and event.state & Gdk.ModifierType.BUTTON1_MASK:
                self.add_area(self.transform_vp_to_pb(Vec2D(event.x, event.y)-self.pad))

    def add_area(self, mouse):
        if self.last_mouse is None:
            self.last_mouse = mouse
            self.current_areas.append((self.last_mouse, mouse))
        prev = self.current_areas[-1][1]
        self.current_areas[-1] = (self.last_mouse, mouse)
        min_vec = self.transform_pb_to_vp(Vec2D.allmin(prev, mouse, self.last_mouse))
        max_vec = self.transform_pb_to_vp(Vec2D.allmax(prev, mouse, self.last_mouse)) + self.pad * 2 - min_vec
        self.queue_draw_area(min_vec.x, min_vec.y, max_vec.x, max_vec.y)

    def move(self, mouse):
        if self.last_mouse is None:
            self.last_mouse = mouse
        self.current_center += (self.last_mouse - mouse) * self.current_zoom
        self.inside_check()
        self.last_mouse = mouse
        self.queue_draw()

    def set_image(self, im_path, areas):
        if self.current_im == im_path:
            self.set_zoom(None)
            return
        self.current_im = im_path
        self.current_pb = GdkPixbuf.Pixbuf.new_from_file(self.current_im)
        self.pb_size = Vec2D(self.current_pb.get_width(), self.current_pb.get_height())
        self.current_areas = areas

    def inside_check(self):
        lt_check = self.current_center - self.im_area/2
        rb_check = self.current_center + self.im_area/2
        if lt_check.x < 0:
            self.current_center.x = self.im_area.x/2
        if lt_check.y < 0:
            self.current_center.y = self.im_area.y/2
        if rb_check.x > self.pb_size.x:
            self.current_center.x = (self.pb_size - self.im_area/2).x
        if rb_check.y > self.pb_size.y:
            self.current_center.y = (self.pb_size - self.im_area / 2).y

        self.current_lt = -(self.transform_vp_to_pb(Vec2D(0, 0))/self.current_zoom) + self.pad

    def transform_vp_to_pb(self, vec):
        return vec * (self.im_area / self.vp_size) + (self.current_center - self.im_area/2)

    def transform_pb_to_vp(self, vec):
        return (vec - (self.current_center - self.im_area/2)) * (self.vp_size / self.im_area)

    def set_zoom(self, zoom):
        if zoom is None:
            zoom = Constants.INIT_ZOOM
            self.current_center = self.pb_size / 2
            self.im_area = self.pb_size

        if zoom <= Constants.MIN_ZOOM:
            zoom = Constants.MIN_ZOOM

        elif zoom >= Constants.MAX_ZOOM:
            zoom = Constants.MAX_ZOOM

        if self.current_pb:
            self.current_surface = Gdk.cairo_surface_create_from_pixbuf(self.current_pb, zoom, None)
        else:
            self.current_surface = None

        self.im_area = self.vp_size * zoom
        if self.current_im:
            self.inside_check()
        self.current_zoom = zoom

        self.queue_draw()
        return zoom
