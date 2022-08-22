# stolen shamelessly from https://stackoverflow.com/questions/6339057/draw-a-transparent-rectangles-and-polygons-in-pygame
from typing import Tuple, List
from dataclasses import dataclass
import pygame
from colors import Color
from _math import Vec2

@dataclass
class Shape:

    @staticmethod
    def line(surface: pygame.Surface, color: Color, p1: Vec2, p2: Vec2, width: int = 1, rot_angle: int = 0) -> None:
        horz = False
        diag = False
        diff_x = int(abs(p2.x-p1.x))
        diff_y = int(abs(p2.y-p1.y))
        if diff_x != 0 and diff_y != 0:
            diag = True
            rect = pygame.Rect(p1.x, p1.y, diff_x, diff_y)
            shape_surf = pygame.Surface((diff_x, diff_y), pygame.SRCALPHA)
        else:
            if diff_y > 0:
                horz = False
                rect_height = diff_y
                rect_width = width
            else:
                horz = True
                rect_height = width
                rect_width = diff_x
            rect = pygame.Rect(p1.x, p1.y, rect_width, rect_height)
            shape_surf = pygame.Surface((rect_width, rect_height), pygame.SRCALPHA)
        if rot_angle > 0:
            shape_surf = pygame.transform.rotate(shape_surf, rot_angle)
        if diag:
            if p1.y < p2.y:
                pygame.draw.line(shape_surf, color.get(), (0, 0), (diff_x, diff_y), width)
            else:
                pygame.draw.line(shape_surf, color.get(), (0, diff_y), (diff_x, 0), width)
        else:
            if horz:
                pygame.draw.line(shape_surf, color.get(), (0, 0), (rect.right, 0), width)
            else:
                pygame.draw.line(shape_surf, color.get(), (0, 0), (0, rect.bottom), width)
        surface.blit(shape_surf, rect)

    @staticmethod
    def rect(surface: pygame.Surface, color: Color, rect: pygame.Rect, width: int = 0, border_radius: int = -1, rot_angle: int = 0):
        shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
        if rot_angle > 0:
            shape_surf = pygame.transform.rotate(shape_surf, rot_angle)
        pygame.draw.rect(shape_surf, color.get(), shape_surf.get_rect(), width=width, border_radius=border_radius)
        surface.blit(shape_surf, rect)

    @staticmethod
    def circle(surface: pygame.Surface, color: Color, center: Tuple[int], radius: int, width: int = 0):
        target_rect = pygame.Rect(center, (0, 0)).inflate((radius * 2, radius * 2))
        shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
        pygame.draw.circle(shape_surf, color.get(), (radius, radius), radius, width=width)
        surface.blit(shape_surf, target_rect)

    @staticmethod
    def polygon(surface: pygame.Surface, color: Color, points: List[int], width: int = 0, rot_angle: int = 0):
        lx, ly = zip(*points)
        min_x, min_y, max_x, max_y = min(lx), min(ly), max(lx), max(ly)
        target_rect = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)
        shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
        if rot_angle > 0:
            shape_surf = pygame.transform.rotate(shape_surf, rot_angle)
        pygame.draw.polygon(shape_surf, color.get(), [(x - min_x, y - min_y) for x, y in points], width=width)
        surface.blit(shape_surf, target_rect)