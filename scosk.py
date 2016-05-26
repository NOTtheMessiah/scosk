#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Steam Controller On-Screen Keyboard - Proof of Concept"""

from steamcontroller import SCButtons, SCI_NULL, SteamController
import steamcontroller.uinput as sui
from steamcontroller.events import EventMapper, Pos
import pygame
from pygame.locals import QUIT
from ui import WSX, WSY, Overlay, Overlay2
from state import Pointer, PointerButton
import sys

USE_GTK = False

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

kp_left = [['1', '2', '3', '4', '5', '6'], ['q', 'w', 'e', 'r', 't'],
            ['a', 's', 'd', 'f', 'g'], ['z', 'x', 'c', 'v', 'b'], [' ']]
kp_right = [['7', '8', '9', '0', '-', '←'], ['y', 'u', 'i', 'o', 'p'],
            ['h', 'j', 'k', 'l', ';', '\''], ['n', 'm', ',', '.', '/'], [' ']]


class VirtualKeypad():
    def __init__(self):
        self.l = Pointer(False)
        self.r = Pointer(True)

    def renderKeyboards(self):
        ovr.fill((0x0f, 0x28, 0x3c))
        self.l.k = _keypad(self.l.px, self.l.py, False)
        self.r.k = _keypad(self.r.px, self.r.py, True)


def tapKey(k):
    kb.pressEvent([k])
    kb.releaseEvent([k])


def isInBox(x, y, w, h, px, py):
    return px > x and px < x + w and py > y and py < y + h


def _rowOfKeys(ls, x, y, w, h, px, py):
    n = len(ls)
    k = ""
    for i, l in enumerate(ls):
        b = isInBox(x + i * w // n, y, w // n, h, px, py)
        ovr.drawKeycap(b, l, x + i * w // n, y, w // n, h)
        if b:
            k = l
    return k


def _keypad(px, py, right):
    n = 5
    tr = ""
    offset = WSX // 2 if right else 0
    kp = kp_right if right else kp_left
    for row, krow in enumerate(kp):
        tr += _rowOfKeys(krow, offset, row * WSY // n, WSX // 2, WSY // n, px, py)
    return tr


class OSKEventMapper(EventMapper):
    def __init__(self):
        super(OSKEventMapper, self).__init__()
        self.set_overlay_buttons()

    @staticmethod
    def exitCallback(self, btn, pressed):
        if not pressed:
            ovr.fill((255, 0, 0))
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
        self.setPadButtonCallback(Pos.LEFT, self.touchLeftCallback, clicked=False)
        self.setPadButtonCallback(Pos.RIGHT, self.touchRightCallback, clicked=False)

    @staticmethod
    def clickRightCallback(self, btn, pressed):
        vkp.r.pb = PointerButton.PRESS
        if pressed:
            if vkp.r.k != '':
                tapKey(whatKey[vkp.r.k])
        else:
            vkp.r.pb = PointerButton.TOUCH

    @staticmethod
    def clickLeftCallback(self, btn, pressed):
        vkp.l.pb = PointerButton.PRESS
        if pressed:
            if vkp.l.k != '':
                tapKey(whatKey[vkp.l.k])
        else:
            vkp.l.pb = PointerButton.TOUCH

    @staticmethod
    def touchRightCallback(self, pad, x, y):
        if not pad:
            vkp.r.px = (0x18000 + x * 12 // 10) * WSX // (0x1fffe)
            vkp.r.py = (0x8000 - y * 12 // 10) * WSY // (0xffff)

    @staticmethod
    def touchLeftCallback(self, pad, x, y):
        if pad:
            vkp.l.px = (0x8000 + x * 12 // 10) * WSX // (0x1fffe)
            vkp.l.py = (0x8000 - y * 12 // 10) * WSY // (0xffff)

ovr = Overlay() if not USE_GTK else Overlay2()
vkp = VirtualKeypad()


# Assumes existence of evm, vkp
def update(sc, sci):
    if not USE_GTK:
        if QUIT in [p.type for p in pygame.event.get()]:
             sys.exit()
    if sci.status != 15361:
        return
    evm.process(sc, sci)
    vkp.renderKeyboards()

    ovr.drawPointer(False, vkp.l.px, vkp.l.py, vkp.l.pb)
    ovr.drawPointer(True, vkp.r.px, vkp.r.py, vkp.r.pb)
    ovr.update()

if __name__ == '__main__':
    ovr.drawKeycap(False, "PLEASE INSERT CONTROLLER", WSX // 4, WSY // 4, WSX // 2, WSY // 2)
    ovr.update()
    evm = OSKEventMapper()
    sc = SteamController(callback=update)
    sc.run()
