from enum import IntEnum
# from ui import wsx, wsy


WSX, WSY = 640, 320  # Window Size <dim>


class PointerButton(IntEnum):
    NONE = 0
    TOUCH = 1
    PRESS = 2


class Pointer():
    def __init__(self, right):
        self.right = right
        if self.right:
            self.px, self.py = 0x18000 * WSX // 0x1fffe, 0x8000 * WSY // 0xffff
        else:
            self.px, self.py = 0x8000 * WSX // 0x1fffe, 0x8000 * WSY // 0xffff
        self.pb = PointerButton.NONE
        self.k = ''
