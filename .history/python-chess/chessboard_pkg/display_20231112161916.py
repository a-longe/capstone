import os
import sys
import pygame

import constants

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
    game_board.update_pieces(fen)

    pygame.display.update()
    fps_clock.tick(FPS)