from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

from pygame.locals import (
    K_BACKSPACE,
    K_DELETE,
    K_END,
    K_ESCAPE,
    K_DOWN,
    K_HOME,
    K_KP_ENTER,
    K_LALT,
    K_LCTRL,
    K_LEFT,
    K_LSHIFT,
    K_PAGEUP,
    K_PAGEDOWN,
    K_RALT,
    K_RCTRL,
    K_RETURN,
    K_RIGHT,
    K_RSHIFT,
    K_SPACE,
    K_TAB,
    K_UP,

    K_0,
    K_KP_0,
    K_1,
    K_KP_1,
    K_2,
    K_KP_2,
    K_3,
    K_KP_3,
    K_4,
    K_KP_4,
    K_5,
    K_KP_5,
    K_6,
    K_KP_6,
    K_7,
    K_KP_7,
    K_8,
    K_KP_8,
    K_9,
    K_KP_9
)

@dataclass
class Arrow:
    up: bool = False
    right: bool = False
    down: bool = False
    left: bool = False

@dataclass
class Keyboard:
    key: Any = None
    alt: bool = False
    backspace: bool = False
    ctrl: bool = False
    delete: bool = False
    end: bool = False
    enter: bool = False
    escape: bool = False
    home: bool = False
    pagedown: bool = False
    pageup: bool = False
    shift: bool = False
    space: bool = False
    tab: bool = False
    arrow: Arrow = field(init=False)
    
    shift_was_down: bool = False

    def __post_init__(self):
        self.arrow = Arrow()

    @staticmethod
    def next_frame(kb: Keyboard = None) -> Keyboard:
        k = Keyboard()
        if kb is not None:
            k.shift_was_down = kb.shift_was_down
        return k

    def update(self, key: Any, key_unicode: str) -> None:
        if key == K_BACKSPACE:
            self.backspace = True
        elif key in [K_LALT, K_RALT]:
            self.alt = True
        elif key in [K_LCTRL, K_RCTRL]:
            self.ctrl = True
        elif key in [K_LSHIFT, K_RSHIFT]:
            self.shift = True
        elif key in [K_KP_ENTER, K_RETURN]:
            self.enter = True
        elif key == K_SPACE:
            self.space = True
        elif key == K_ESCAPE:
            self.escape = True
        elif key == K_TAB:
            self.tab = True
        elif key == K_UP:
            self.arrow.up = True
        elif key == K_RIGHT:
            self.arrow.right = True
        elif key == K_DOWN:
            self.arrow.down = True
        elif key == K_LEFT:
            self.arrow.left = True
        elif key == K_DELETE:
            self.delete = True
        elif key == K_HOME:
            self.home = True
        elif key == K_END:
            self.end = True
        elif key == K_PAGEDOWN:
            self.pagedown = True
        elif key == K_PAGEUP:
            self.pageup = True
        elif key in [K_0, K_KP_0, K_1, K_KP_1, K_2, K_KP_2,
                     K_3, K_KP_3, K_4, K_KP_4, K_5, K_KP_5,
                     K_6, K_KP_6, K_7, K_KP_7, K_8, K_KP_8, K_9, K_KP_9]:
            self.key = key_unicode
        else:
            if (key > 64 and key < 91) or (key > 96 and key < 123):
                self.key = key_unicode