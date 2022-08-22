import pygame
from pygame.constants import RESIZABLE, VIDEORESIZE, MOUSEMOTION, MOUSEWHEEL, SRCALPHA, HWACCEL, MOUSEBUTTONDOWN, MOUSEBUTTONUP, K_RSHIFT, K_LSHIFT
from pygame.locals import KEYDOWN, KEYUP, QUIT
from Game import Game
from colors import Colors
from font import FontUseType

pygame.init()
clock = pygame.time.Clock()

gameWidth = 1920
gameHeight = 960
game = Game(gameWidth, gameHeight)
game.screen = pygame.display.set_mode((gameWidth, gameHeight),RESIZABLE|SRCALPHA|HWACCEL)
game.set_background_color(Colors.DARK_GREY)
game.register_sys_font('Courier', 12, FontUseType.DEFAULT)
game.load_setup("setup.json")

while game.running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            game.keyboard.update(event.key, event.unicode)
        elif event.type == KEYUP:
            if event.key in [K_RSHIFT, K_LSHIFT]:
                game.keyboard.shift_was_down = False
        elif event.type == MOUSEBUTTONDOWN:
            game.mouse.set_pressed(event.button)
        elif event.type == MOUSEBUTTONUP:
            game.mouse.set_released(event.button)
        elif event.type == MOUSEWHEEL:
            game.mouse.set_scroll(event.x, event.y)
        elif event.type == MOUSEMOTION:
            game.mouse.set_offset(event.rel)
        elif event.type == VIDEORESIZE:
            old = game.screen
            game.screen = pygame.display.set_mode((event.w,event.h),RESIZABLE|SRCALPHA|HWACCEL)
            game.screen.blit(old,(0,0))
            del old
        elif event.type == QUIT:
            game.running = False

    game.mouse.set_pos(pygame.mouse.get_pos())
    game.update()
    game.draw()

    pygame.display.flip()

    clock.tick(30)