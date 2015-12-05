#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Steam Controller On-Screen Keyboard - Proof of Concept"""

import pygame
from steamcontroller import SteamController
import pykeyboard
import time

pygame.init()
ssx, ssy = 640,320
screen = pygame.display.set_mode((ssx,ssy))
pygame.display.set_caption("scosk")
state = 0 # remember last button state
time.sleep(1)

kb = pykeyboard.PyKeyboard()

def renderYesNo(x,y,r):
    pygame.draw.rect(screen,(0x0,0x5b,0x10),(0,0,ssx,ssy//2))
    pygame.draw.rect(screen,(0x60,0x12,0x15),(0,ssy//2,ssx,ssy//2))
    pygame.draw.circle(screen, (128,128,128), (x,y), r, 2)
    pygame.display.update()

def update(_, sci):
    if sci.status != 15361:
        return
    global state
    newstate = sci.buttons
    px,py = (0x8000+sci.rpad_x)*ssx//0xffff,(0x8000-sci.rpad_y)*ssy//0xffff
    rpadbuttons = sci.buttons & 0x14000000
    if rpadbuttons == 0x10000000:
        renderYesNo(px,py,10)
    elif rpadbuttons == 0x14000000:
        renderYesNo(px,py,7)
        # key presses (check prev state)
        if state & 0x14000000 != 0x14000000:
            if sci.rpad_y > 0:
                kb.tap_key('y')
            else:
                kb.tap_key('n')
    state = newstate

sc = SteamController(callback=update)
sc.run()
