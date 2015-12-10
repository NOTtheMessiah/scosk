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

pygame.init()
ssx, ssy = 640, 320 # Screen Size <dim>
screen = pygame.display.set_mode((ssx, ssy))
screen.fill((0x0f, 0x28, 0x3c))
sci_p = SCI_NULL

kb = sui.Keyboard()

def tap_key(k):
    kb.pressEvent([k])
    kb.releaseEvent([k])

def virtualKeycap(txt, x, y, w, h, px, py):
    if px > x and px < x + w and py > y and py < y+h:
        pygame.draw.rect(screen, (0x25, 0x5f, 0x7e), (x+5, y+5, w-10, h-10))
        b = True
    else:
        pygame.draw.rect(screen, (0x19, 0x3d, 0x55), (x+5, y+5, w-10, h-10))
        b = False
        
    textSurf = pygame.font.SysFont("Sans", 20).render(txt, True, (255, 255, 255))
    textRect = textSurf.get_rect(center=(x+(w//2), y+(h//2)))
    screen.blit(textSurf, textRect)
    return b

def rowOfKeys(ls, x, y, w, h, px, py, press):
    n = len(ls)
    a = []
    k = ""
    for i, l in enumerate(ls):
        if virtualKeycap(l, x+i*w//n, y, w//n, h, px, py) and press:
            k = l
    return k

whatKey = {
    '0' : sui.Keys.KEY_0,
    '1' : sui.Keys.KEY_1,
    '2' : sui.Keys.KEY_2,
    '3' : sui.Keys.KEY_3,
    '4' : sui.Keys.KEY_4,
    '5' : sui.Keys.KEY_5,
    '6' : sui.Keys.KEY_6,
    '7' : sui.Keys.KEY_7,
    '8' : sui.Keys.KEY_8,
    '9' : sui.Keys.KEY_9,
    'a' : sui.Keys.KEY_A,
    'b' : sui.Keys.KEY_B,
    'c' : sui.Keys.KEY_C,
    'd' : sui.Keys.KEY_D,
    'e' : sui.Keys.KEY_E,
    'f' : sui.Keys.KEY_F,
    'g' : sui.Keys.KEY_G,
    'h' : sui.Keys.KEY_H,
    'i' : sui.Keys.KEY_I,
    'j' : sui.Keys.KEY_J,
    'k' : sui.Keys.KEY_K,
    'l' : sui.Keys.KEY_L,
    'm' : sui.Keys.KEY_M,
    'n' : sui.Keys.KEY_N,
    'o' : sui.Keys.KEY_O,
    'p' : sui.Keys.KEY_P,
    'q' : sui.Keys.KEY_Q,
    'r' : sui.Keys.KEY_R,
    's' : sui.Keys.KEY_S,
    't' : sui.Keys.KEY_T,
    'u' : sui.Keys.KEY_U,
    'v' : sui.Keys.KEY_V,
    'w' : sui.Keys.KEY_W,
    'x' : sui.Keys.KEY_X,
    'y' : sui.Keys.KEY_Y,
    'z' : sui.Keys.KEY_Z,
    ';' : sui.Keys.KEY_SEMICOLON,
    '\\' : sui.Keys.KEY_BACKSLASH,
    '\'' : sui.Keys.KEY_APOSTROPHE,
    ',' : sui.Keys.KEY_COMMA,
    '.' : sui.Keys.KEY_DOT,
    '/' : sui.Keys.KEY_SLASH,
    '-' : sui.Keys.KEY_MINUS,
    '?' : sui.Keys.KEY_QUESTION,
    ' ' : sui.Keys.KEY_SPACE,
    '←' : sui.Keys.KEY_BACKSPACE
}

def rkeypad(px, py, press):
    n = 5
    tr = ""
    tr += rowOfKeys(['7', '8', '9', '0', '-', '←'], ssx//2, 0, ssx//2, ssy//n, px, py, press)
    tr += rowOfKeys(['y', 'u', 'i', 'o', 'p'], ssx//2, 1*ssy//n, ssx//2, ssy//n, px, py, press)
    tr += rowOfKeys(['h', 'j', 'k', 'l', ';', '\''], ssx//2, 2*ssy//n, ssx//2, ssy//n, px, py, press)
    tr += rowOfKeys(['n', 'm', ',', '.', '/'], ssx//2, 3*ssy//n, ssx//2, ssy//n, px, py, press)
    tr += rowOfKeys([' '], ssx//2, 4*ssy//n, ssx//2, ssy//n, px, py, press)
    return tr

def lkeypad(px,py,press):
    n = 5
    tr = ""
    tr += rowOfKeys(['1', '2', '3', '4', '5', '6'], 0, 0, ssx//2, ssy//n, px, py, press)
    tr += rowOfKeys(['q', 'w', 'e', 'r', 't'], 0, 1*ssy//n, ssx//2, ssy//n, px, py, press)
    tr += rowOfKeys(['a', 's', 'd', 'f', 'g'], 0, 2*ssy//n, ssx//2, ssy//n, px, py, press)
    tr += rowOfKeys(['z', 'x', 'c', 'v', 'b'], 0, 3*ssy//n, ssx//2, ssy//n, px, py, press)
    tr += rowOfKeys([' '], 0, 4*ssy//n, ssx//2, ssy//n, px, py, press)
    return tr

def exitCallback(evm, btn, pressed):
    screen.fill((255, 0, 0))
    print("ABORT")
    if not pressed:
        sys.exit()

def evminit():
    evm = EventMapper()
    evm.setButtonAction(SCButtons.LGRIP, sui.Keys.KEY_LEFTSHIFT)
    evm.setButtonAction(SCButtons.LB, sui.Keys.KEY_BACKSPACE)
    evm.setButtonAction(SCButtons.RB, sui.Keys.KEY_SPACE)
    evm.setButtonAction(SCButtons.A, sui.Keys.KEY_ENTER)
    evm.setButtonCallback(SCButtons.B, exitCallback)
    #evm.setPadButtonCallback(Pos.RIGHT, _)
    #evm.setPadButtonCallback(Pos.LEFT, _)
    return evm

def update(sc, sci):
    if sci.status != 15361:
        return
    evm.process(sc, sci)
    global sci_p
    lpx, lpy = (0x8000+sci.lpad_x*12//10)*ssx//(0x1fffe), (0x8000-sci.lpad_y*12//10)*ssy//(0xffff)
    rpx, rpy = (0x18000+sci.rpad_x*12//10)*ssx//(0x1fffe), (0x8000-sci.rpad_y*12//10)*ssy//(0xffff)
    lpadbuttons = sci.buttons & 0x0a000000
    rpadbuttons = sci.buttons & 0x14000000
    rr, rpress, lr, lpress = 10, False, 10, False
    if rpadbuttons == 0x10000000:
        rr = 10
    elif rpadbuttons == 0x14000000:
        rr, rpress = 7, (sci_p.buttons & 0x14000000 != 0x14000000)
    else:
        rr = 100
    if lpadbuttons == 0x08000000:
        lr = 10
    elif lpadbuttons == 0x0a000000:
        lr, lpress = 7, (sci_p.buttons & 0x0a000000 != 0x0a000000)
    else:
        lr = 100
    screen.fill((0x0f, 0x28, 0x3c))
    lk = lkeypad(lpx, lpy, lpress)
    if lpress and lk != '': tap_key(whatKey[lk])
    rk = rkeypad(rpx, rpy, rpress)
    if rpress and rk != '': tap_key(whatKey[rk])
    pygame.draw.circle(screen, (255, 128, 128), (lpx, lpy), lr, 2)
    pygame.draw.circle(screen, (128, 255, 128), (rpx, rpy), rr, 2)
    pygame.display.update()
    sci_p = sci

if __name__ == '__main__':
    evm = evminit()
    sc = SteamController(callback=update)
    sc.run()
