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
        # dispInfo = pygame.display.Info()
        # ssx, ssy = dispInfo.current_w, dispInfo.current_h
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


class VirtualKeypad():
    def __init__(self):
        # self.kp = kp_right if right else kp_left
        # self.offset = wsx//2 if right else 0
        self.lpx, self.lpy = 0x8000*wsx//0x1fffe, 0x8000*wsy//0xffff
        self.rpx, self.rpy = 0x18000*wsx//0x1fffe, 0x8000*wsy//0xffff
        self.lpb, self.rpb = PointerButton.NONE, PointerButton.NONE
        self.lk, self.rk = '', ''
        self.lpress, self.rpress = False, False

    def updatePointers(self, sci):
        self.lpx = (0x8000+sci.lpad_x*12//10)*wsx//(0x1fffe)
        self.lpy = (0x8000-sci.lpad_y*12//10)*wsy//(0xffff)
        self.rpx = (0x18000+sci.rpad_x*12//10)*wsx//(0x1fffe)
        self.rpy = (0x8000-sci.rpad_y*12//10)*wsy//(0xffff)

    def renderKeyboards(self):
        ovr.canvas.fill((0x0f, 0x28, 0x3c))
        self.lk = _keypad(self.lpx, self.lpy, self.lpress, False)
        # if self.lpress and self.lk != '':
        #     tapKey(whatKey[self.lk])
        self.rk = _keypad(self.rpx, self.rpy, self.rpress, True)
        # if self.rpress and self.rk != '':
        #     tapKey(whatKey[self.rk])

    def getButtonState(self, sci, sci_p):
        lpadbuttons = sci.buttons & (SCButtons.LPAD.value + SCButtons.LPADTOUCH.value)
        rpadbuttons = sci.buttons & (SCButtons.RPAD.value + SCButtons.RPADTOUCH.value)
        self.rpress, self.lpress = False, False
        if rpadbuttons == SCButtons.RPADTOUCH.value:
            self.rpb, self.rpress = PointerButton.TOUCH, bool(sci_p.buttons & SCButtons.RPAD.value)
        elif rpadbuttons == SCButtons.RPADTOUCH.value + SCButtons.RPAD.value:
            self.rpb = PointerButton.PRESS
        else:
            self.rpb = PointerButton.NONE
        if lpadbuttons == SCButtons.LPADTOUCH.value:
            self.lpb, self.lpress = PointerButton.TOUCH, bool(sci_p.buttons & SCButtons.LPAD.value)
        elif lpadbuttons == SCButtons.LPADTOUCH.value + SCButtons.LPAD.value:
            self.lpb = PointerButton.PRESS
        else:
            self.lpb = PointerButton.NONE


def tapKey(k):
    kb.pressEvent([k])
    kb.releaseEvent([k])


def virtualKeycap(txt, x, y, w, h, px, py):
    b = px > x and px < x + w and py > y and py < y+h
    ovr.drawKeycap(b, txt, x, y, w, h)
    return b


def _rowOfKeys(ls, x, y, w, h, px, py, press):
    n = len(ls)
    k = ""
    for i, l in enumerate(ls):
        if virtualKeycap(l, x+i*w//n, y, w//n, h, px, py):  # and press:
            k = l
    return k


def _keypad(px, py, press, right):
    n = 5
    tr = ""
    offset = wsx//2 if right else 0
    kp = kp_right if right else kp_left
    for row, krow in enumerate(kp):
        tr += _rowOfKeys(krow, offset, row*wsy//n, wsx//2, wsy//n, px, py, press)
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
        else:
            print("ABORT")

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
            if vkp.rk != '':
                tapKey(whatKey[vkp.rk])

    @staticmethod
    def clickLeftCallback(self, btn, pressed):
        if pressed:
            if vkp.lk != '':
                tapKey(whatKey[vkp.lk])


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
    vkp.updatePointers(sci)
    vkp.getButtonState(sci, sci_p)
    vkp.renderKeyboards()

    ovr.drawPointer((255, 128, 128), vkp.lpx, vkp.lpy, vkp.lpb)
    ovr.drawPointer((255, 128, 128), vkp.rpx, vkp.rpy, vkp.rpb)
    ovr.update()
    sci_p = sci

if __name__ == '__main__':
    virtualKeycap("PLEASE INSERT CONTROLLER", wsx//4, wsy//4, wsx//2, wsy//2, 0, 0)
    ovr.update()
    evm = OSKEventMapper()
    sc = SteamController(callback=update)
    sc.run()
