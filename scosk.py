#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Steam Controller On-Screen Keyboard - Proof of Concept"""

import pygame
from steamcontroller import SteamController
import pykeyboard
import time
import os

pygame.init()
ssx, ssy = 640,320
screen = pygame.display.set_mode((ssx,ssy))
screen.fill((0x0f,0x28,0x3c))
state = 0

kb = pykeyboard.PyKeyboard()

def keybutton(txt,x,y,w,h, px,py):
    if px > x and px < x + w and py > y and py < y+h:
        pygame.draw.rect(screen,(0x25,0x5f,0x7e),(x+5,y+5,w-10,h-10))
        b = True
    else:
        pygame.draw.rect(screen,(0x19,0x3d,0x55),(x+5,y+5,w-10,h-10))
        b = False
        
    textSurf = pygame.font.SysFont("Lato",20).render(txt, True, (255,255,255))
    textRect = textSurf.get_rect(center=(x+(w//2),y+(h//2)))
    screen.blit(textSurf, textRect)
    return b

def rowofkeys(ls,x,y,w,h,px,py,press):
    n = len(ls)
    a = []
    for i,l in enumerate(ls):
        #print(l,x+i*w//n,y,w//n,h,px,py)
        if keybutton(l,x+i*w//n,y,w//n,h,px,py) and press:
            return(l)
    return ""
            
def rkeypad(px,py,press):
    n = 5
    tr = ""
    tr+=rowofkeys(['7','8','9','0','-'],ssx//2,0,ssx//2,ssy//n,px,py,press)
    tr+=rowofkeys(['y','u','i','o','p'],ssx//2,1*ssy//n,ssx//2,ssy//n,px,py,press)
    tr+=rowofkeys(['h','j','k','l',';','\''],ssx//2,2*ssy//n,ssx//2,ssy//n,px,py,press)
    tr+=rowofkeys(['n','m',',','.','/'],ssx//2,3*ssy//n,ssx//2,ssy//n,px,py,press)
    tr+=rowofkeys([' '],ssx//2,4*ssy//n,ssx//2,ssy//n,px,py,press)
    return tr

def lkeypad(px,py,press):
    n = 5
    tr = ""
    tr+=rowofkeys(['1','2','3','4','5','6'],0,0,ssx//2,ssy//n,px,py,press)
    tr+=rowofkeys(['q','w','e','r','t'],0,1*ssy//n,ssx//2,ssy//n,px,py,press)
    tr+=rowofkeys(['a','s','d','f','g'],0,2*ssy//n,ssx//2,ssy//n,px,py,press)
    tr+=rowofkeys(['z','x','c','v','b'],0,3*ssy//n,ssx//2,ssy//n,px,py,press)
    tr+=rowofkeys([' '],0,4*ssy//n,ssx//2,ssy//n,px,py,press)
    return tr

def update(_, sci):
    if sci.status != 15361:
        return
    global state
    newstate = sci.buttons
    lpx,lpy = (0x8000+sci.lpad_x*12//10)*ssx//(0x1fffe),(0x8000-sci.lpad_y*12//10)*ssy//(0xffff)
    rpx,rpy = (0x18000+sci.rpad_x*12//10)*ssx//(0x1fffe),(0x8000-sci.rpad_y*12//10)*ssy//(0xffff)
    lpadbuttons = sci.buttons & 0x0a000000
    rpadbuttons = sci.buttons & 0x14000000
    rr,rpress,lr,lpress = 10, False, 10, False
    if rpadbuttons == 0x10000000:
        rr = 10
    elif rpadbuttons == 0x14000000:
        rr,rpress = 7, (state & 0x14000000 != 0x14000000)
    else:
        rr = 100

    if lpadbuttons == 0x08000000:
        lr = 10
    elif lpadbuttons == 0x0a000000:
        lr,lpress = 7, (state & 0x0a000000 != 0x0a000000)
    else:
        lr = 100
    screen.fill((0x0f,0x28,0x3c))
    lk = lkeypad(lpx,lpy,lpress)
    if lpress and lk!='': kb.tap_key(lk)
    rk = rkeypad(rpx,rpy,rpress)
    if rpress and rk!='': kb.tap_key(rk)
    pygame.draw.circle(screen, (255,128,128), (lpx,lpy), lr, 2)
    pygame.draw.circle(screen, (128,255,128), (rpx,rpy), rr, 2)
    pygame.display.update()
    state = newstate

sc = SteamController(callback=update)
sc.run()
