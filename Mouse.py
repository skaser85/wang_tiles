from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple
from _math import Vec2

@dataclass
class Mouse:
    pos: Vec2 = Vec2(0, 0)
    left_down: bool = False
    left_released: bool = False
    left_was_down: bool = False
    right_down: bool = False
    right_released: bool = False
    middle_down: bool = False
    middle_released: bool = False
    scrolled_up: bool = False
    scrolled_down: bool = False
    scrolled_amt_x: int = 0
    scrolled_amt_y: int = 0
    last_pos: Vec2 = Vec2(0, 0)
    mouse_moved: bool = False
    offset_x: int = 0
    offset_y: int = 0

    @staticmethod
    def next_frame(pm: Mouse = None) -> Mouse:
        m = Mouse()
        if pm:
            m.last_pos = pm.pos
            m.left_was_down = pm.left_was_down
        return m

    def set_offset(self, offset: Tuple[int]) -> None:
        self.mouse_moved = True
        self.offset_x = offset[0]
        self.offset_y = offset[1]

    def get_offset_from_last_frame(self) -> Vec2:
        p = self.pos.copy()
        p.sub(self.last_pos)
        return p

    def set_pos(self, pos: Tuple[int]) -> None:
        self.pos = Vec2(pos[0], pos[1])

    def set_pressed(self, button: int) -> None:
        if button == 1:
            self.left_down = True
            self.left_was_down = True
        elif button == 2:
            self.middle_down = True
        elif button == 3:
            self.right_down = True
        elif button == 4:
            # scroll down
            # ignored here because this will be handled with the MOUSEWHEEL event in the set_scroll function
            ...
        elif button == 5:
            # scroll up
            # ignored here because this will be handled with the MOUSEWHEEL event in the set_scroll function
            ...

    def set_released(self, button: int) -> None:
        if button == 1:
            self.left_released = True
            self.left_was_down = False
        elif button == 2:
            self.middle_released = True
        elif button == 3:
            self.right_released = True
            self.right_down = False

    def set_scroll(self, x: int, y: int) -> None:
        self.scrolled_amt_x = x
        self.scrolled_amt_y = y