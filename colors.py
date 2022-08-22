from __future__ import annotations
from dataclasses import dataclass, fields
from typing import List, Tuple
from _math import clamp, lerp

@dataclass
class Color:
    """
    Color works between 0.0 and 1.0 to make the math easier. Static methods available
    to return a tuple of ints in the range 0-255 as well as hex strings.
    """
    r: float = 0.0
    g: float = 0.0
    b: float = 0.0
    a: float = 1.0

    def get(self, return_format: str = '255') -> Tuple[int|float]|str:
        """
        Available formats (always returned in RGBA):

            '255'   => Tuple[int]   = (255, 255, 255, 255)

            'float' => Tuple[float] = (1.0, 1.0, 1.0, 1.0)

            'hex'   => str          = '#ffffffff'

        """
        if return_format == '255':
            return Color.to_255_values(self)
        elif return_format == 'float':
            return Color.to_float(self)
        elif return_format == 'hex':
            return Color.to_hex_str(self)
        else:
            raise ValueError(f'Invalid return_format: {return_format}. Available formats: "255", "float", "hex"')

    @staticmethod
    def to_float(color: Color) -> Tuple[float]:
        return color.r, color.g, color.b, color.a

    @staticmethod
    def to_hex_str(color: Color) -> str:
        c = Color.to_255_values(color)
        r = hex(c[0])[2:].zfill(2)
        g = hex(c[1])[2:].zfill(2)
        b = hex(c[2])[2:].zfill(2)
        a = hex(c[3])[2:].zfill(2)
        return f'#{r}{g}{b}{a}'

    @staticmethod
    def from_hex_str(hex_str: str) -> Color:
        if hex_str.startswith('#'):
            hex_str = hex_str[1:]
        if not len(hex_str) in [3, 6, 8]:
            raise ValueError(f'hex_str argument must be 3, 6, or 8 characters long (e.g., fff (rgb), ffffff (rrggbb), ffffffff (rrggbbaa)).  Invalid: {hex_str}')
        if len(hex_str) == 3:
            hex_str = f'{hex_str[0] + hex_str[0]}{hex_str[1] + hex_str[1]}{hex_str[2] + hex_str[2]}ff'
        elif len(hex_str) == 6:
            hex_str = f'{hex_str}ff'
        r = int(hex_str[:2], 16)
        g = int(hex_str[2:4], 16)
        b = int(hex_str[4:6], 16)
        a = int(hex_str[6:], 16)
        return Color.from_255_values(r, g, b, a)

    @staticmethod
    def from_255_values(r: int, g: int, b: int, a: int = 255) -> Color:
        return Color(r/255, g/255, b/255, a/255)

    @staticmethod
    def to_255_values(color: Color) -> Tuple[int]:
        return (int(color.r*255),int(color.g*255),int(color.b*255),int(color.a*255))

    @staticmethod
    def copy(color: Color) -> Color:
        return Color(color.r, color.g, color.b, color.a)

    @staticmethod
    def brighten(color: Color, amount: float = 0.1) -> Color:
        r = clamp(color.r + amount, 0.0, 1.0)
        g = clamp(color.g + amount, 0.0, 1.0)
        b = clamp(color.b + amount, 0.0, 1.0)
        return Color(r, g, b, color.a)

    @staticmethod
    def darken(color: Color, amount: float = 0.1) -> Color:
        r = clamp(color.r - amount, 0.0, 1.0)
        g = clamp(color.g - amount, 0.0, 1.0)
        b = clamp(color.b - amount, 0.0, 1.0)
        return Color(r, g, b, color.a)

    @staticmethod
    def invert(color: Color) -> Color:
        r = abs(1.0 - color.r)
        g = abs(1.0 - color.g)
        b = abs(1.0 - color.b)
        return Color(r, g, b, color.a)

    @staticmethod
    def lerp(c1: Color, c2: Color, t: float) -> Tuple[int]:
        r = clamp(abs(lerp(c1.r, c2.r, t)), 0.0, 1.0)
        g = clamp(abs(lerp(c1.g, c2.g, t)), 0.0, 1.0)
        b = clamp(abs(lerp(c1.b, c2.b, t)), 0.0, 1.0)
        return Color(r, g, b, 1.0) # is hard-coding the alpha ok?

@dataclass
class Colors:
    BLACK:      Color = Color(  0/255,   0/255,   0/255, 255/255)
    BLUE:       Color = Color(  0/255,   0/255, 255/255, 255/255)
    BLUE2:      Color = Color( 29/255, 145/255, 191/255, 255/255)
    DARK_GREY:  Color = Color( 50/255,  50/255,  50/255, 255/255)
    DARK_GREEN: Color = Color(  5/255, 163/255,  63/255, 255/255)
    WHITE:      Color = Color(255/255, 255/255, 255/255, 255/255)
    GREEN:      Color = Color(  0/255, 255/255,   0/255, 255/255)
    GREY:       Color = Color(128/255, 128/255, 128/255, 255/255)
    RED:        Color = Color(255/255,   0/255,   0/255, 255/255)
    RED2:       Color = Color(235/255, 110/255, 110/255, 255/255)
    MAGENTA:    Color = Color(255/255,   0/255, 255/255, 255/255)
    PINK:       Color = Color(255/255, 112/255, 200/255, 255/255)
    PURPLE:     Color = Color(208/255, 105/255, 240/255, 255/255)
    CYAN:       Color = Color(  0/255, 255/255, 255/255, 255/255)
    YELLOW:     Color = Color(255/255, 255/255,   0/255, 255/255)

    @classmethod
    def get_color_names(cls) -> List[str]:
        return [c.name for c in fields(cls)]
    
    @classmethod
    def get_colors(cls) -> List[Color]:
        return [c.default for c in fields(cls)]

    @classmethod
    def get_color_by_name(cls, name: str) -> Color:
        c = [c.default for c in fields(cls) if c.name == name.upper()]
        if len(c) > 0:
            return c[0] 

if __name__ == '__main__':
    print(Colors.get_color_by_name('green'))