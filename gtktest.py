#!/usr/bin/env python

# stolen from http://askubuntu.com/questions/93088/making-gtk-window-transparent
# also using http://www.tortall.net/mu/wiki/CairoTutorial#cairos-drawing-model

import cairo
import gi
import time
import sys
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk


class MyWin (Gtk.Window):
    def __init__(self):
        super(MyWin, self).__init__(type = Gtk.WindowType.POPUP)
        self.set_accept_focus(False)
        self.set_resizable(False)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_border_width(30)
        self.screen = self.get_screen()
        self.visual = self.screen.get_rgba_visual()
        if self.visual is not None and self.screen.is_composited():
            print("yay")
            self.set_visual(self.visual)

        # box = Gtk.Box()
        # btn1 = Gtk.Button(label="foo")
        # box.add(btn1)
        # self.add(box)

        self.set_app_paintable(True)
        self.connect("draw", self.area_draw)
        self.connect("draw", self.button_draw)
        self.show_all()

    def area_draw(self, widget, cr):
        cr.set_source_rgba(.06, .16, .24, 0.25)
        cr.set_operator(cairo.OPERATOR_SOURCE)
        cr.paint()

    def button_draw(self, widget, cr):
        x, y, w, h, c = 10, 20, 30, 50, (0.15, 0.18, 0.49, 0.25)
        cr.set_source_rgba(c[0], c[1], c[2], c[3])
        cr.set_operator(cairo.OPERATOR_SOURCE)
        cr.rectangle(x, y, w, h)
        cr.fill()
        cr.set_source_rgba(1.0, 1.0, 1.0, 0.75)
        cr.select_font_face("Ubuntu", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        cr.set_font_size(16)
        x_bearing, y_bearing, width, height = cr.text_extents("Q")[:4]
        print(x_bearing, y_bearing, width, height)
        cr.move_to(x + w / 2 - width / 2 - x_bearing, y + h / 2 - height / 2 - y_bearing)
        cr.show_text("a")

MyWin()
Gtk.main()
