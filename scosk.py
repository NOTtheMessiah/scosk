#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Steam Controller On-Screen Keyboard - Proof of Concept"""

from steamcontroller import *
import steamcontroller.uinput as sui
from steamcontroller.events import EventMapper, Pos
import time
import os
import sys
import pygame
from pygame.locals import QUIT
from Xlib import display

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

kp_left = [['1', '2', '3', '4', '5', '6'], ['q', 'w', 'e', 'r', 't'], ['a', 's', 'd', 'f', 'g'], ['z', 'x', 'c', 'v', 'b'], [' ']]
kp_right = [['7', '8', '9', '0', '-', '←'], ['y', 'u', 'i', 'o', 'p'], ['h', 'j', 'k', 'l', ';', '\''], ['n', 'm', ',', '.', '/'], [' ']]

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

    def drawPointer(self, c, px, py, r):
        pygame.draw.circle(self.canvas, c, (px, py), r, 2)

    def update(self):
        pygame.display.update()

ovr = Overlay()


def tapKey(k):
    kb.pressEvent([k])
    kb.releaseEvent([k])


def virtualKeycap(txt, x, y, w, h, px, py):
    b = px > x and px < x + w and py > y and py < y+h
    ovr.drawKeycap(b, txt, x, y, w, h)
    return b


def rowOfKeys(ls, x, y, w, h, px, py, press):
    n = len(ls)
    k = ""
    for i, l in enumerate(ls):
        if virtualKeycap(l, x+i*w//n, y, w//n, h, px, py) and press:
            k = l
    return k


def keypad(px, py, press, right):
    n = 5
    tr = ""
    offset = wsx//2 if right else 0
    kp = kp_right if right else kp_left
    for row, krow in enumerate(kp):
        tr += rowOfKeys(krow, offset, row*wsy//n, wsx//2, wsy//n, px, py, press)
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
        # self.setPadButtonCallback(Pos.RIGHT, _)
        # self.setPadButtonCallback(Pos.LEFT, _)

def update(sc, sci):
    if QUIT in [p.type for p in pygame.event.get()]:
        sys.exit()
    if sci.status != 15361:
        return
    evm.process(sc, sci)
    global sci_p
    lpx, lpy = (0x8000+sci.lpad_x*12//10)*wsx//(0x1fffe), (0x8000-sci.lpad_y*12//10)*wsy//(0xffff)
    rpx, rpy = (0x18000+sci.rpad_x*12//10)*wsx//(0x1fffe), (0x8000-sci.rpad_y*12//10)*wsy//(0xffff)
    lpadbuttons = sci.buttons & 0x0a000000
    rpadbuttons = sci.buttons & 0x14000000
    rr, rpress, lr, lpress = 10, False, 10, False
    if rpadbuttons == 0x10000000:
        rr, rpress = 10, (sci_p.buttons & 0x14000000 == 0x14000000)
    elif rpadbuttons == 0x14000000:
        rr = 7
    else:
        rr = 100
    if lpadbuttons == 0x08000000:
        lr, lpress = 10, (sci_p.buttons & 0x0a000000 == 0x0a000000)
    elif lpadbuttons == 0x0a000000:
        lr = 7
    else:
        lr = 100
    ovr.canvas.fill((0x0f, 0x28, 0x3c))
    lk = keypad(lpx, lpy, lpress, False)
    if lpress and lk != '':
        tapKey(whatKey[lk])
    rk = keypad(rpx, rpy, rpress, True)
    if rpress and rk != '':
        tapKey(whatKey[rk])
    ovr.drawPointer((255, 128, 128), lpx, lpy, lr)
    ovr.drawPointer((255, 128, 128), rpx, rpy, rr)
    ovr.update()
    sci_p = sci

if __name__ == '__main__':

    virtualKeycap("PLEASE INSERT CONTROLLER", wsx//4, wsy//4, wsx//2, wsy//2, 0, 0)
    ovr.update()
    evm = OSKEventMapper()
    sc = SteamController(callback=update)
    sc.run()
