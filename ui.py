#!/usr/bin/env python

# stolen from http://askubuntu.com/questions/93088/making-gtk-window-transparent
# also using http://www.tortall.net/mu/wiki/CairoTutorial#cairos-drawing-model

import cairo
import gi
from math import pi

import os
import pygame
from Xlib import display
from state import PointerButton
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk


WSX, WSY = 640, 320  # Window Size <dim>


class Overlay:
    def __init__(self):
        pygame.init()
        mousePos = display.Display().screen().root.query_pointer()._data
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (mousePos["root_x"] - WSX // 2, mousePos["root_y"] + 64)
        pygame.display.set_caption("scosk")
        self.canvas = pygame.display.set_mode((WSX, WSY))
        self.canvas.fill((0x0f, 0x28, 0x3c))

    def drawKeycap(self, state, txt, x, y, w, h):
        if state:
            pygame.draw.rect(self.canvas, (0x25, 0x5f, 0x7e), (x + 5, y + 5, w - 10, h - 10))
        else:
            pygame.draw.rect(self.canvas, (0x19, 0x3d, 0x55), (x + 5, y + 5, w - 10, h - 10))
        textSurf = pygame.font.SysFont("Sans", 20).render(txt, True, (255, 255, 255))
        textRect = textSurf.get_rect(center=(x + (w // 2), y + (h // 2)))
        self.canvas.blit(textSurf, textRect)

    def drawPointer(self, right, px, py, pb):
        c = (255, 128, 128) if right else (128, 255, 128)
        if pb == PointerButton.PRESS:
            pygame.draw.circle(self.canvas, c, (px, py), 7, 2)
        elif pb == PointerButton.TOUCH:
            pygame.draw.circle(self.canvas, c, (px, py), 10, 2)
        else:
            pygame.draw.circle(self.canvas, c, (px, py), 100, 2)

    def update(self):
        pygame.display.update()

    def fill(self, c):
        self.canvas.fill(c)


class Overlay2:
    def __init__(self):
        # self.window = Gtk.Window(type=Gtk.WindowType.POPUP)
        # self.window.set_position(Gtk.WindowPosition.CENTER)
        # self.window.set_default_size(WSX, WSY)
        self.window = MyWin()
        # Gtk.main()

    def drawKeycap(self, state, txt, x, y, w, h):
        print("TODO")
        # self.window.connect("draw", self.window.key_draw, state, txt, x, y, w, h)

    def drawPointer(self, right, px, py, pb):
        print("TODO")
        # self.window.connect("draw", self.window.pointer_draw, right, px, py, pb)

    def update(self):
        # self.window.show_all()
        print("TODO")

    def fill(self, c):
        print("TODO")
        # self.window.connect("draw", self.window.bg_draw)


class MyWin (Gtk.Window):
    def __init__(self):
        super(MyWin, self).__init__(type=Gtk.WindowType.POPUP)
        # super(MyWin, self).__init__(type=Gtk.WindowType.TOPLEVEL)
        # self.set_accept_focus(False)
        # self.set_resizable(False)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_default_size(WSX, WSY)
        self.screen = self.get_screen()
        self.visual = self.screen.get_rgba_visual()
        if self.visual is not None and self.screen.is_composited():
            self.set_visual(self.visual)

        # box = Gtk.Box()
        # btn1 = Gtk.Button(label="foo")
        # box.add(btn1)
        # self.add(box)

        self.set_app_paintable(True)
        self.connect("destroy", self.destroy)
        self.connect("draw", self.bg_draw)
        self.connect("draw", self.key_draw, False, 'a', 10, 20, 30, 50)
        self.connect("draw", self.key_draw, True, 'b', 60, 30, 20, 20)
        self.connect("draw", self.pointer_draw, True, 65, 35, PointerButton.PRESS)
        self.show_all()

    def bg_draw(self, widget, cr):
        cr.set_source_rgba(.06, .16, .24, 0.25)
        cr.set_operator(cairo.OPERATOR_SOURCE)
        cr.paint()

    def destroy(self, widget, data=None):
        Gtk.main_quit()

    def key_draw(self, widget, cr, state, txt, x, y, w, h):
        if state:
            c = (0.30, 0.36, 0.98, 0.50)
        else:
            c = (0.15, 0.18, 0.49, 0.25)
        # Render Keycap
        cr.set_source_rgba(c[0], c[1], c[2], c[3])
        cr.set_operator(cairo.OPERATOR_SOURCE)
        cr.rectangle(x, y, w, h)
        cr.fill()
        # Render Text
        cr.set_source_rgba(1.0, 1.0, 1.0, 0.75)
        cr.select_font_face("Ubuntu", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        cr.set_font_size(16)
        x_bearing, y_bearing, width, height = cr.text_extents(txt)[:4]
        cr.move_to(x + w / 2 - width / 2 - x_bearing, y + h / 2 - height / 2 - y_bearing)
        cr.show_text(txt)

    def pointer_draw(self, widget, cr, right, x, y, pb):
        if pb == PointerButton.PRESS:
            r = 7
        elif pb == PointerButton.TOUCH:
            r = 10
        else:
            r = 100
        c = (1, 0, 0, 0.25) if right else (0, 1, 0, 0.25)
        cr.arc(x, y, r, 0, 2 * pi)
        cr.set_source_rgba(c[0], c[1], c[2], c[3])
        cr.stroke()

if __name__ == '__main__':
    MyWin()
    Gtk.main()
