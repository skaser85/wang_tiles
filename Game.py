import os
from dataclasses import dataclass, field
from typing import Callable, List, Dict, Any, Literal
from json import loads
import pygame
from font import FontStore, FontUseType, _Font, _SysFont
from colors import Colors, Color
from Keyboard import Keyboard
from Mouse import Mouse
from _math import Vec2, clamp
from Shape import Shape
from random import choice

@dataclass
class Sides:
    n: int = 0
    e: int = 0
    w: int = 0
    s: int = 0

@dataclass
class Tile:
    surface: pygame.Surface
    sides: Sides
    filepath: str
    x: int = 0
    y: int = 0

@dataclass
class Game:
    screen_width: int
    screen_height: int
    screen: pygame.display = None

    font_store: FontStore = FontStore()

    game_started: bool = False
    running: bool = True
    paused: bool = True
    dragging: bool = False
    game_has_run_once: bool = False

    background_image: pygame.image = None
    background_color: Color = Colors.BLACK
    
    menus: dict = field(default_factory=dict)
    menu_actions: Dict[str, Callable] = field(default_factory=dict)
    
    keyboard: Keyboard = None
    mouse: Mouse = None

    hot_item: Any = None
    active_item: Any = None

    tile_w: int = 32
    tile_h: int = 32
    tile_count: int = 16
    tile_count_w: int = 0
    tile_count_h: int = 0
    tiles: List[Tile] = field(default_factory=list)
    
    grid_size_px: int = 32
    grid_tiles: List[pygame.Surface] = field(default_factory=list)

    color_1: Any = None

    placed: int = 0

    tile_index: int = 0

    candidate_tiles: List[Tile] = field(default_factory=list)

    check_tile_west: Tile = None
    check_tile_north: Tile = None

    def __post_init__(self):
        pygame.font.init()
        pygame.mixer.init()
        self.keyboard = Keyboard()
        self.mouse = Mouse()

        self.tile_count_h = self.screen_height // self.tile_h
        self.tile_count_w = self.screen_width // self.tile_w

    def __post_setup__(self):
        self.register_sys_font('Consolas', 16, FontUseType.DEFAULT)
        tile_sets_dir = './tile_sets'
        for i in range(self.tile_count):
            fp = os.path.join(tile_sets_dir, f'{i}.png')
            img = pygame.image.load(fp)
            n_color = img.get_at((self.tile_w//2, 1))
            e_color = img.get_at((self.tile_w-1, self.tile_h//2))
            s_color = img.get_at((self.tile_w//2, self.tile_h-1))
            w_color = img.get_at((1, self.tile_h//2))

            if self.color_1 is None:
                self.color_1 = n_color

            s = Sides()

            if n_color == self.color_1:
                s.n = 1
            if e_color == self.color_1:
                s.e = 1
            if s_color == self.color_1:
                s.s = 1
            if w_color == self.color_1:
                s.w = 1

            tile = Tile(img, s, fp)

            self.tiles.append(tile)

        self.grid_tiles = [None for _ in range(self.tile_count_w*self.tile_count_h)]
        self.create_wang_tiles()

    def create_wang_tiles(self) -> None:
        for ti in range(len(self.grid_tiles)):
            t = self.get_rand_tile(ti)
            self.grid_tiles[ti] = t

    def set_background_color(self, color: Color):
        self.background_color = color

    def register_background_image(self, path):        
        self.background_image = pygame.image.load(path)
        self.background_image = pygame.transform.scale(self.background_image, (self.screen.get_width(), self.screen.get_height()))

    def register_font(self, path: str, size: int, font_use_type: FontUseType) -> None:
        if font_use_type == FontUseType.DEFAULT:
            self.font_store.default = _Font(path, size)
        elif font_use_type == FontUseType.MENU:
            self.font_store.menu = _Font(path, size)
        elif font_use_type == FontUseType.UI:
            self.font_store.ui = _Font(path, size)
        else:
            raise ValueError(f'Unknown font_use_type: {font_use_type}')

    def register_sys_font(self, font_name: str, size: int, font_use_type: FontUseType) -> None:
        if font_use_type == FontUseType.DEFAULT:
            self.font_store.default = _SysFont(font_name, size)
        elif font_use_type == FontUseType.MENU:
            self.font_store.menu = _SysFont(font_name, size)
        elif font_use_type == FontUseType.UI:
            self.font_store.ui = _SysFont(font_name, size)
        else:
            raise ValueError(f'Unknown font_use_type: {font_use_type}')

    def draw(self):
        # clear the screen
        if self.background_image is None:
            self.screen.fill(self.background_color.get())
        else:
            self.screen.blit(self.background_image, (0, 0))

        for y in range(self.tile_count_h):
            for x in range(self.tile_count_w):
                index = y * self.tile_count_w + x
                tile = self.grid_tiles[index]
                if tile is not None:
                    tile.x = x * self.tile_w
                    tile.y = y * self.tile_h
                    self.screen.blit(tile.surface, (tile.x, tile.y))

        if self.check_tile_north is not None:
            Shape.rect(self.screen, Colors.PURPLE, pygame.Rect(self.check_tile_north.x, self.check_tile_north.y, self.tile_w, self.tile_h),5)

        if self.check_tile_west is not None:
            Shape.rect(self.screen, Colors.GREEN, pygame.Rect(self.check_tile_west.x, self.check_tile_west.y, self.tile_w, self.tile_h),5)

        # x = 64
        # y = 64
        # for t in self.candidate_tiles:
        #     self.screen.blit(t.surface, (x, y))
        #     text = self.font_store.default.font.render(t.filepath, True, Colors.WHITE.get())
        #     tw, th = text.get_size()
        #     self.screen.blit(text, (x + self.tile_w, y + th/2))
        #     y += self.tile_h


    def get_rand_tile(self, tile_index: int) -> Tile:
        if tile_index == 0:
            tile = choice(self.tiles)
            return tile

        s = Sides()

        check_west = False
        self.check_tile_west = None
        if tile_index % self.tile_count_w > 0:
            check_west = True
            self.check_tile_west = self.grid_tiles[tile_index - 1]
            west_tile_sides = self.check_tile_west.sides
            s.w = west_tile_sides.e

        check_north = False
        self.check_tile_north = None
        if tile_index >= self.tile_count_w:
            check_north = True
            self.check_tile_north = self.grid_tiles[tile_index - self.tile_count_w]
            north_tile_sides = self.check_tile_north.sides
            s.n = north_tile_sides.s

        self.candidate_tiles = []
        for t in self.tiles:
            if check_west and check_north:
                if t.sides.w == s.w and t.sides.n == s.n:
                    self.candidate_tiles.append(t)
            elif check_west and not check_north:
                if t.sides.w == s.w:
                    self.candidate_tiles.append(t)
            elif not check_west and check_north:
                if t.sides.n == s.n:
                    self.candidate_tiles.append(t)

        if len(self.candidate_tiles) == 0:
            raise ValueError(f'Could not find valid tile!')

        tile = choice(self.candidate_tiles)

        return tile

    def update(self):
        if self.mouse.left_released:
            if self.active_item is not None:
                if self.hot_item is not None:
                    if self.active_item == self.hot_item:
                        self.active_item.handle_keyboard(self.keyboard)
                        if self.active_item.dragging:
                            self.active_item.handle_end_drag()
                            self.active_item = None
                        else:
                            self.active_item.handle_click(self.mouse.pos)
                    else:
                        self.active_item.deactivate()
                        self.active_item = self.hot_item.handle_click(self.mouse.pos)
                else:
                    self.active_item.deactivate()
            elif self.hot_item is not None:
                self.active_item = self.hot_item.handle_click(self.mouse.pos)                
            else:
                self.create_wang_tiles()
                # if self.tile_index <= ((self.tile_count_h * self.tile_count_w)-1):
                #     self.grid_tiles[self.tile_index] = self.get_rand_tile(self.tile_index)
                #     self.tile_index += 1
            self.check_radio_groups()
        elif self.mouse.right_released:
            ...
            # if self.tile_index > 0:
            #     self.tile_index -= 1
            #     self.grid_tiles[self.tile_index] = None
        elif self.mouse.left_down:
            if self.active_item is not None:
                if not self.active_item.dragging:
                    self.active_item.handle_begin_drag()
        elif self.mouse.left_was_down and self.mouse.mouse_moved:
            if self.active_item is not None and self.active_item.dragging:
                self.active_item.handle_drag(self.mouse.offset_x, self.mouse.offset_y)
        
        self.keyboard = Keyboard.next_frame(self.keyboard)
        self.mouse = Mouse.next_frame(self.mouse)

    def load_setup(self, setup_file_path: str) -> None:
        # with open(setup_file_path) as f:
        #     data = loads(f.read())
        
        self.__post_setup__()

    def check_radio_groups(self):
        ...