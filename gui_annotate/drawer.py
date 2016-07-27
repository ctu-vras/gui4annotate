#!/usr/bin/env python3

from gi.repository import Gtk, Gdk, GdkPixbuf, GObject
from gui_annotate.vec import Vec2D
from gui_annotate.constants import Constants


class Drawer(Gtk.DrawingArea):
    def __init__(self, app, *args, **kwargs):
        Gtk.DrawingArea.__init__(self, *args, **kwargs)

        self.app = app

        self.current_im = None
        self.current_pb = None
        self.current_surface = None
        self.current_center = None
        self.current_lt = None

        self.pb_size = None
        self.visible_pb_area = None

        self.last_mouse = None
        self.draw_area = None

        self.vp_size = Constants.INIT_SIZE
        self.pad = Constants.PADDING

        self.win_size = self.vp_size + self.pad * 2
        self.over = False

        self.set_size_request(self.win_size.x, self.win_size.y)
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
        self.connect('draw', self.draw)
        self.app.connect('notify::zoom', lambda w, _: self.set_zoom(w.zoom))
        self.app.connect('notify::current-im-node', lambda w, _: self.set_image(w.current_im_node))
        self.app.connect('notify::state', lambda w, _: self.change_cursor(self.over))
        self.app.connect('change-areas', lambda _, change: self.queue_draw())
        self.app.connect('remove-roi', self.removed_roi)

    def draw(self, _, ctx):
        if self.current_surface:
            ctx.set_source_surface(self.current_surface, self.current_lt.x, self.current_lt.y)
        else:
            ctx.set_source_rgb(1, 1, 1)
        ctx.paint()

        ctx.set_source_rgb(1, 0, 0)
        ctx.set_line_width(1)
        if self.app.current_im_node is not None:
            for area in self.app.current_im_node.children:
                self.draw_roi(ctx, area.lt, area.rb)
        if self.draw_area:
            self.draw_roi(ctx, self.draw_area[0], self.draw_area[1])

        ctx.set_source_rgb(0, 0, 0)
        ctx.set_line_width(self.pad.x)
        ctx.rectangle(self.pad.x * 0.5, self.pad.y * 0.5, (self.vp_size + self.pad).x, (self.vp_size + self.pad).y)
        ctx.stroke()

    def draw_roi(self, ctx, lt, rb):
        a0 = self.transform_pb_to_vp(lt) + self.pad
        a1 = self.transform_pb_to_vp(rb) + self.pad - a0
        ctx.rectangle(a0.x, a0.y, a1.x, a1.y)
        ctx.stroke()

    def add_tmp_area(self, mouse):
        if mouse.x > self.pb_size.x:
            mouse.x = self.pb_size.x
        if mouse.y > self.pb_size.y:
            mouse.y = self.pb_size.y
        if mouse.x < 0:
            mouse.x = 0
        if mouse.y < 0:
            mouse.y = 0

        if self.last_mouse is None:
            self.last_mouse = mouse
            self.draw_area = (self.last_mouse, mouse)
        prev = self.draw_area[1]
        self.draw_area = (self.last_mouse, mouse)
        min_vec = self.transform_pb_to_vp(Vec2D.allmin(prev, mouse, self.last_mouse))
        max_vec = self.transform_pb_to_vp(Vec2D.allmax(prev, mouse, self.last_mouse)) + self.pad * 2 - min_vec
        self.queue_draw_area(min_vec.x, min_vec.y, max_vec.x, max_vec.y)

    def move(self, mouse):
        if self.last_mouse is None:
            self.last_mouse = mouse
        self.current_center += (self.last_mouse - mouse) * self.app.zoom
        self.calc_correct_lt()
        self.last_mouse = mouse
        self.queue_draw()

    def set_image(self, tree):
        if self.current_im == tree.path:
            return
        self.current_im = tree.path
        self.current_pb = GdkPixbuf.Pixbuf.new_from_file(tree.path)
        self.pb_size = Vec2D(self.current_pb.get_width(), self.current_pb.get_height())
        tree.size = self.pb_size
        self.set_zoom(None)
        self.app.can_save = tree.changed

    def calc_correct_lt(self):
        lt_check = self.current_center - self.visible_pb_area / 2
        rb_check = self.current_center + self.visible_pb_area / 2
        if lt_check.x < 0:
            self.current_center.x = self.visible_pb_area.x / 2
        if lt_check.y < 0:
            self.current_center.y = self.visible_pb_area.y / 2
        if rb_check.x > self.pb_size.x:
            self.current_center.x = (self.pb_size - self.visible_pb_area / 2).x
        if rb_check.y > self.pb_size.y:
            self.current_center.y = (self.pb_size - self.visible_pb_area / 2).y

        self.current_lt = -(self.transform_vp_to_pb(Vec2D(0, 0)) / self.app.zoom) + self.pad

    def transform_vp_to_pb(self, vec):
        return vec * (self.visible_pb_area / self.vp_size) + (self.current_center - self.visible_pb_area / 2)

    def transform_pb_to_vp(self, vec):
        return (vec - (self.current_center - self.visible_pb_area / 2)) * (self.vp_size / self.visible_pb_area)

    def set_zoom(self, zoom):
        if zoom is None:
            zoom = Constants.INIT_ZOOM
            self.current_center = self.pb_size / 2
            self.visible_pb_area = self.pb_size

        if zoom <= Constants.MIN_ZOOM:
            zoom = Constants.MIN_ZOOM

        elif zoom >= Constants.MAX_ZOOM:
            zoom = Constants.MAX_ZOOM

        if self.current_pb:
            self.current_surface = Gdk.cairo_surface_create_from_pixbuf(self.current_pb, zoom, None)
        else:
            self.current_surface = None

        self.visible_pb_area = self.vp_size * zoom
        if self.current_im:
            self.calc_correct_lt()
        if zoom is not self.app.zoom:
            self.app.zoom = zoom
        self.queue_draw()

    def button_press(self, _, event):
        if self.app.state == Constants.STATE_REMOVE and event.type == Gdk.EventType.BUTTON_PRESS and event.button == Constants.LEFT_BUTTON:
            mouse = self.transform_vp_to_pb(Vec2D(event.x, event.y) - self.pad)

            all_rois = self.app.current_im_node.children
            n_rois = [roi for roi in all_rois if not (roi.lt <= mouse <= roi.rb)]

            rm = list(set(all_rois) - set(n_rois))
            for rm_roi in rm:
                self.app.emit('remove-roi', rm_roi)

    def removed_roi(self, _, roi):
        lt = self.transform_pb_to_vp(roi.lt)
        rb = self.transform_pb_to_vp(roi.rb) - lt + self.pad * 2
        self.queue_draw_area(lt.x, lt.y, rb.x, rb.y)

    def button_motion(self, _, event):
        if self.app.current_im_node:
            mouse = Vec2D(event.x, event.y)
            if self.app.state == Constants.STATE_MOVE:
                if event.type == Gdk.EventType.MOTION_NOTIFY and event.state & Gdk.ModifierType.BUTTON1_MASK:
                    self.move(mouse)
            if self.app.state == Constants.STATE_ADD:
                if event.type == Gdk.EventType.MOTION_NOTIFY and event.state & Gdk.ModifierType.BUTTON1_MASK:
                    self.add_tmp_area(self.transform_vp_to_pb(mouse - self.pad))

    def button_release(self, _, event):
        if event.type == Gdk.EventType.BUTTON_RELEASE and event.state & Gdk.ModifierType.BUTTON1_MASK:
            self.last_mouse = None
            if self.app.state == Constants.STATE_ADD:
                rb_vec = Vec2D.allmax(*self.draw_area)
                lt_vec = Vec2D.allmin(*self.draw_area)
                self.app.emit('append-roi', str(lt_vec) + ',' + str(rb_vec) + ',' + Constants.DEFAULT_ANNOTATION)
                self.draw_area = None

    def change_cursor(self, enter):
        self.over = enter
        cursor = None
        if enter:
            if self.app.state == Constants.STATE_MOVE:
                cursor = Constants.CURSOR_MOVE
            if self.app.state == Constants.STATE_ADD:
                cursor = Constants.CURSOR_DRAW
            if self.app.state == Constants.STATE_REMOVE:
                cursor = Constants.CURSOR_DELETE
        self.get_window().set_cursor(cursor)
