#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Steam Controller On-Screen Keyboard - Proof of Concept"""

import pygame
from steamcontroller import SteamController
import steamcontroller.uinput as scui 
import time
import os

pygame.init()
ssx, ssy = 640,320
screen = pygame.display.set_mode((ssx,ssy))
screen.fill((0x0f,0x28,0x3c))
state = 0

kb = scui.Keyboard()

def tap_key(k):
    kb.pressEvent([k])
    kb.releaseEvent([k])

def keybutton(txt,x,y,w,h, px,py):
    if px > x and px < x + w and py > y and py < y+h:
        pygame.draw.rect(screen,(0x25,0x5f,0x7e),(x+5,y+5,w-10,h-10))
        b = True
    else:
        pygame.draw.rect(screen,(0x19,0x3d,0x55),(x+5,y+5,w-10,h-10))
        b = False
        
    textSurf = pygame.font.SysFont("Sans",20).render(txt, True, (255,255,255))
    textRect = textSurf.get_rect(center=(x+(w//2),y+(h//2)))
    screen.blit(textSurf, textRect)
    return b

def rowofkeys(ls,x,y,w,h,px,py,press):
    n = len(ls)
    a = []
    k = ""
    for i,l in enumerate(ls):
        if keybutton(l,x+i*w//n,y,w//n,h,px,py) and press:
            k = l
    return k

whatKey= {
    '0' : scui.Keys.KEY_0,
    '1' : scui.Keys.KEY_1,
    '2' : scui.Keys.KEY_2,
    '3' : scui.Keys.KEY_3,
    '4' : scui.Keys.KEY_4,
    '5' : scui.Keys.KEY_5,
    '6' : scui.Keys.KEY_6,
    '7' : scui.Keys.KEY_7,
    '8' : scui.Keys.KEY_8,
    '9' : scui.Keys.KEY_9,
    'a' : scui.Keys.KEY_A,
    'b' : scui.Keys.KEY_B,
    'c' : scui.Keys.KEY_C,
    'd' : scui.Keys.KEY_D,
    'e' : scui.Keys.KEY_E,
    'f' : scui.Keys.KEY_F,
    'g' : scui.Keys.KEY_G,
    'h' : scui.Keys.KEY_H,
    'i' : scui.Keys.KEY_I,
    'j' : scui.Keys.KEY_J,
    'k' : scui.Keys.KEY_K,
    'l' : scui.Keys.KEY_L,
    'm' : scui.Keys.KEY_M,
    'n' : scui.Keys.KEY_N,
    'o' : scui.Keys.KEY_O,
    'p' : scui.Keys.KEY_P,
    'q' : scui.Keys.KEY_Q,
    'r' : scui.Keys.KEY_R,
    's' : scui.Keys.KEY_S,
    't' : scui.Keys.KEY_T,
    'u' : scui.Keys.KEY_U,
    'v' : scui.Keys.KEY_V,
    'w' : scui.Keys.KEY_W,
    'x' : scui.Keys.KEY_X,
    'y' : scui.Keys.KEY_Y,
    'z' : scui.Keys.KEY_Z,
    ';' : scui.Keys.KEY_SEMICOLON,
    '\\' : scui.Keys.KEY_BACKSLASH,
    '\'' : scui.Keys.KEY_APOSTROPHE,
    ',' : scui.Keys.KEY_COMMA,
    '.' : scui.Keys.KEY_DOT,
    '/' : scui.Keys.KEY_SLASH,
    '-' : scui.Keys.KEY_MINUS,
    '?' : scui.Keys.KEY_QUESTION,
    ' ' : scui.Keys.KEY_SPACE,
    '←' : scui.Keys.KEY_BACKSPACE
        }
            
def rkeypad(px,py,press):
    n = 5
    tr = ""
    tr+=rowofkeys(['7','8','9','0','-','←'],ssx//2,0,ssx//2,ssy//n,px,py,press)
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
    if lpress and lk!='': tap_key(whatKey[lk])
    rk = rkeypad(rpx,rpy,rpress)
    if rpress and rk!='': tap_key(whatKey[rk])
    pygame.draw.circle(screen, (255,128,128), (lpx,lpy), lr, 2)
    pygame.draw.circle(screen, (128,255,128), (rpx,rpy), rr, 2)
    pygame.display.update()
    state = newstate

sc = SteamController(callback=update)
sc.run()
