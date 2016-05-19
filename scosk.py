#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Steam Controller On-Screen Keyboard - Proof of Concept"""

from steamcontroller import SCButtons, SCI_NULL, SteamController
import steamcontroller.uinput as sui
from steamcontroller.events import EventMapper, Pos
import os
import sys
import pygame
from pygame.locals import QUIT
from Xlib import display
from enum import IntEnum

wsx, wsy = 640, 320  # Window Size <dim>

sci_p = SCI_NULL

kb = sui.Keyboard()

whatKey = {
    '0': sui.Keys.KEY_0,
    '1': sui.Keys.KEY_1,
    '2': sui.Keys.KEY_2,
    '3': sui.Keys.KEY_3,
    '4': sui.Keys.KEY_4,
    '5': sui.Keys.KEY_5,
    '6': sui.Keys.KEY_6,
    '7': sui.Keys.KEY_7,
    '8': sui.Keys.KEY_8,
    '9': sui.Keys.KEY_9,
    'a': sui.Keys.KEY_A,
    'b': sui.Keys.KEY_B,
    'c': sui.Keys.KEY_C,
    'd': sui.Keys.KEY_D,
    'e': sui.Keys.KEY_E,
    'f': sui.Keys.KEY_F,
    'g': sui.Keys.KEY_G,
    'h': sui.Keys.KEY_H,
    'i': sui.Keys.KEY_I,
    'j': sui.Keys.KEY_J,
    'k': sui.Keys.KEY_K,
    'l': sui.Keys.KEY_L,
    'm': sui.Keys.KEY_M,
    'n': sui.Keys.KEY_N,
    'o': sui.Keys.KEY_O,
    'p': sui.Keys.KEY_P,
    'q': sui.Keys.KEY_Q,
    'r': sui.Keys.KEY_R,
    's': sui.Keys.KEY_S,
    't': sui.Keys.KEY_T,
    'u': sui.Keys.KEY_U,
    'v': sui.Keys.KEY_V,
    'w': sui.Keys.KEY_W,
    'x': sui.Keys.KEY_X,
    'y': sui.Keys.KEY_Y,
    'z': sui.Keys.KEY_Z,
    ';': sui.Keys.KEY_SEMICOLON,
    '\\': sui.Keys.KEY_BACKSLASH,
    '\'': sui.Keys.KEY_APOSTROPHE,
    ',': sui.Keys.KEY_COMMA,
    '.': sui.Keys.KEY_DOT,
    '/': sui.Keys.KEY_SLASH,
    '-': sui.Keys.KEY_MINUS,
    '?': sui.Keys.KEY_QUESTION,
    ' ': sui.Keys.KEY_SPACE,
    '←': sui.Keys.KEY_BACKSPACE
}

kp_left  = [['1', '2', '3', '4', '5', '6'], ['q', 'w', 'e', 'r', 't'],
            ['a', 's', 'd', 'f', 'g'], ['z', 'x', 'c', 'v', 'b'], [' ']]
kp_right = [['7', '8', '9', '0', '-', '←'], ['y', 'u', 'i', 'o', 'p'],
            ['h', 'j', 'k', 'l', ';', '\''], ['n', 'm', ',', '.', '/'], [' ']]


class Overlay:
    def __init__(self):
        pygame.init()
        mousePos = display.Display().screen().root.query_pointer()._data
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (mousePos["root_x"]-wsx//2, mousePos["root_y"]+64)
        pygame.display.set_caption("scosk")
        self.canvas = pygame.display.set_mode((wsx, wsy))
        self.canvas.fill((0x0f, 0x28, 0x3c))

    def drawKeycap(self, state, txt, x, y, w, h):
        if state:
            pygame.draw.rect(self.canvas, (0x25, 0x5f, 0x7e), (x+5, y+5, w-10, h-10))
        else:
            pygame.draw.rect(self.canvas, (0x19, 0x3d, 0x55), (x+5, y+5, w-10, h-10))
        textSurf = pygame.font.SysFont("Sans", 20).render(txt, True, (255, 255, 255))
        textRect = textSurf.get_rect(center=(x+(w//2), y+(h//2)))
        self.canvas.blit(textSurf, textRect)

    def drawPointer(self, c, px, py, pb):
        if pb == PointerButton.PRESS:
            pygame.draw.circle(self.canvas, c, (px, py), 7, 2)
        elif pb == PointerButton.TOUCH:
            pygame.draw.circle(self.canvas, c, (px, py), 10, 2)
        else:
            pygame.draw.circle(self.canvas, c, (px, py), 100, 2)

    def update(self):
        pygame.display.update()


class PointerButton(IntEnum):
    NONE = 0
    TOUCH = 1
    PRESS = 2


class Pointer():
    def __init__(self, right):
        self.right = right
        if self.right:
            self.px, self.py = 0x18000*wsx//0x1fffe, 0x8000*wsy//0xffff
        else:
            self.px, self.py = 0x8000*wsx//0x1fffe, 0x8000*wsy//0xffff
        self.pb = PointerButton.NONE
        self.k = ''

    def updateState(self, sci, sci_p):
        pad = SCButtons.RPAD if self.right else SCButtons.LPAD
        padt = SCButtons.RPADTOUCH if self.right else SCButtons.LPADTOUCH
        padbuttons = sci.buttons & (pad.value | padt.value)
        if padbuttons == padt.value:
            self.pb = PointerButton.TOUCH
        elif padbuttons == padt.value + pad.value:
            self.pb = PointerButton.PRESS
        else:
            self.pb = PointerButton.NONE


class VirtualKeypad():
    def __init__(self):
        self.l = Pointer(False)
        self.r = Pointer(True)

    def updateState(self, sci, sci_p):
        self.l.px = (0x8000+sci.lpad_x*12//10)*wsx//(0x1fffe)
        self.l.py = (0x8000-sci.lpad_y*12//10)*wsy//(0xffff)
        self.r.px = (0x18000+sci.rpad_x*12//10)*wsx//(0x1fffe)
        self.r.py = (0x8000-sci.rpad_y*12//10)*wsy//(0xffff)
        self.l.updateState(sci, sci_p)
        self.r.updateState(sci, sci_p)


    def renderKeyboards(self):
        ovr.canvas.fill((0x0f, 0x28, 0x3c))
        self.l.k = _keypad(self.l.px, self.l.py, False)
        self.r.k = _keypad(self.r.px, self.r.py, True)


def tapKey(k):
    kb.pressEvent([k])
    kb.releaseEvent([k])


def isInBox(x, y, w, h, px, py):
    return px > x and px < x + w and py > y and py < y+h


def _rowOfKeys(ls, x, y, w, h, px, py):
    n = len(ls)
    k = ""
    for i, l in enumerate(ls):
        b = isInBox(x+i*w//n, y, w//n, h, px, py)
        ovr.drawKeycap(b, l, x+i*w//n, y, w//n, h)
        if b:
            k = l
    return k


def _keypad(px, py, right):
    n = 5
    tr = ""
    offset = wsx//2 if right else 0
    kp = kp_right if right else kp_left
    for row, krow in enumerate(kp):
        tr += _rowOfKeys(krow, offset, row*wsy//n, wsx//2, wsy//n, px, py)
    return tr


class OSKEventMapper(EventMapper):
    def __init__(self):
        super(OSKEventMapper, self).__init__()
        self.set_overlay_buttons()

    @staticmethod
    def exitCallback(self, btn, pressed):
        if not pressed:
            ovr.canvas.fill((255, 0, 0))
            ovr.update()
            sys.exit()

    def set_overlay_buttons(self):
        self.setButtonAction(SCButtons.LGRIP, sui.Keys.KEY_LEFTSHIFT)
        self.setButtonAction(SCButtons.LB, sui.Keys.KEY_BACKSPACE)
        self.setButtonAction(SCButtons.RB, sui.Keys.KEY_SPACE)
        self.setButtonAction(SCButtons.A, sui.Keys.KEY_ENTER)
        self.setButtonCallback(SCButtons.B, self.exitCallback)
        self.setPadButtonCallback(Pos.LEFT, self.clickLeftCallback, clicked=True)
        self.setPadButtonCallback(Pos.RIGHT, self.clickRightCallback, clicked=True)

    @staticmethod
    def clickRightCallback(self, btn, pressed):
        if pressed:
            if vkp.r.k != '':
                tapKey(whatKey[vkp.r.k])

    @staticmethod
    def clickLeftCallback(self, btn, pressed):
        if pressed:
            if vkp.l.k != '':
                tapKey(whatKey[vkp.l.k])


ovr = Overlay()
vkp = VirtualKeypad()


# Assumes existence of evm, vkp, and sci_p
def update(sc, sci):
    if QUIT in [p.type for p in pygame.event.get()]:
        sys.exit()
    if sci.status != 15361:
        return
    evm.process(sc, sci)
    global sci_p
    vkp.updateState(sci, sci_p)
    vkp.renderKeyboards()

    ovr.drawPointer((255, 128, 128), vkp.l.px, vkp.l.py, vkp.l.pb)
    ovr.drawPointer((255, 128, 128), vkp.r.px, vkp.r.py, vkp.r.pb)
    ovr.update()
    sci_p = sci

if __name__ == '__main__':
    ovr.drawKeycap(False, "PLEASE INSERT CONTROLLER", wsx//4, wsy//4, wsx//2, wsy//2)
    ovr.update()
    evm = OSKEventMapper()
    sc = SteamController(callback=update)
    sc.run()
