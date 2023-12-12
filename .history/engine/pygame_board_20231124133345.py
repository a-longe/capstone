import pygame as pg
from my_utils import is_odd
from os import path, environ

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600

BOARD_SIZE = 4

BG_COLOR = (50, 50, 50)

a8, a7, a6, a5, a4, a3, a2, a1 = (100, 100), (100, 150), (100, 200), (100, 250), (100, 300), (100, 350), (100, 400), (100, 450)
b8, b7, b6, b5, b4, b3, b2, b1 = (150, 100), (150, 150), (150, 200), (150, 250), (150, 300), (150, 350), (150, 400), (150, 450)
c8, c7, c6, c5, c4, c3, c2, c1 = (200, 100), (200, 150), (200, 200), (200, 250), (200, 300), (200, 350), (200, 400), (200, 450)
d8, d7, d6, d5, d4, d3, d2, d1 = (250, 100), (250, 150), (250, 200), (250, 250), (250, 300), (250, 350), (250, 400), (250, 450)
e8, e7, e6, e5, e4, e3, e2, e1 = (300, 100), (300, 150), (300, 200), (300, 250), (300, 300), (300, 350), (300, 400), (300, 450)
f8, f7, f6, f5, f4, f3, f2, f1 = (350, 100), (350, 150), (350, 200), (350, 250), (350, 300), (350, 350), (350, 400), (350, 450)
g8, g7, g6, g5, g4, g3, g2, g1 = (400, 100), (400, 150), (400, 200), (400, 250), (400, 300), (400, 350), (400, 400), (400, 450)
h8, h7, h6, h5, h4, h3, h2, h1 = (450, 100), (450, 150), (450, 200), (450, 250), (450, 300), (450, 350), (450, 400), (450, 450)

BOARD_RECT = (
    (a8, b8, c8, d8, e8, f8, g8, h8),
    (a7, b7, c7, d7, e7, f7, g7, h7),
    (a6, b6, c6, d6, e6, f6, g6, h6),
    (a5, b5, c5, d5, e5, f5, g5, h5),
    (a4, b4, c4, d4, e4, f4, g4, h4),
    (a3, b3, c3, d3, e3, f3, g3, h3),
    (a2, b2, c2, d2, e2, f2, g2, h2),
    (a1, b1, c1, d1, e1, f1, g1, h1)
)


IMAGE_DIR = path.join(path.dirname(path.abspath(__file__)), 'images')

environ['SDL_VIDEO_CENTERED'] = '1'

w_tile_img = pg.image.load(path.join(IMAGE_DIR, 'wtile.png'))
b_tile_img = pg.image.load(path.join(IMAGE_DIR, 'btile.png'))

def create_checkerboard() -> pg.Surface:
    checkerboard = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    checkerboard.fill(BG_COLOR)
    for i in range(1, BOARD_SIZE + 1):
        for j in range(1, BOARD_SIZE + 1):
            if is_odd(i):
                if is_odd(j):
                    checkerboard.blit(w_tile_img, BOARD_RECT[i - 1][j - 1])
                else:
                    checkerboard.blit(b_tile_img, BOARD_RECT[i - 1][j - 1])
            elif not is_odd(i):
                if is_odd(j):
                    checkerboard.blit(b_tile_img, BOARD_RECT[i - 1][j - 1])
                else:
                    checkerboard.blit(w_tile_img, BOARD_RECT[i - 1][j - 1]) 
    return checkerboard

def display_piece(glyph:str, position:str) -> None:
    

pg.init()
checkerboard = create_checkerboard()
while True:
    pg.display.update()

