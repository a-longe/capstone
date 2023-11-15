import os
import sys
import pygame

import constants

from pygame.locals import QUIT, KEYUP, K_ESCAPE

from board import Board, Color
from constants import FPS, STARTING_FEN, WINDOW_CAPTION, WINDOW_WIDTH, WINDOW_HEIGHT


screen = pygame.display.set_mode([constants.WINDOW_WIDTH,
                                  constants.WINDOW_HEIGHT])

os.environ['SDL_VIDEO_CENTERED'] = '1'  # Centre display window.

fps_clock = pygame.time.Clock()

def terminate():
    pygame.quit()
    sys.exit()


def check_for_quit():
    for _ in pygame.event.get(QUIT):
        terminate()
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            terminate()
        pygame.event.post(event)

def update(game_board):
    check_for_quit()

    pygame.display.update()
    fps_clock.tick(FPS)


def start(fen=STARTING_FEN, bg_color=Color.ASH, caption=WINDOW_CAPTION):
    pygame.init()

    display_surf = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(caption)

    display_surf.fill(bg_color)
    game_board = Board((50, 50, 50), display_surf)

    update(fen, game_board)

    return game_board