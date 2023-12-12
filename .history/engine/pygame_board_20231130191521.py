import pygame as pg
from my_utils import row_index_to_legend
from my_utils import is_odd, column_letter_to_index
from os import path, environ
from sys import exit

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600

SQUARE_SIZE = 50

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

w_tile_img = pg.image.load(path.join(IMAGE_DIR, 'wtile.png'))
b_tile_img = pg.image.load(path.join(IMAGE_DIR, 'btile.png'))

fps = pg.time.Clock()

def get_piece_img(glyph:str) -> pg.Surface:
    if glyph.isupper():
        color = 'w'
    else:
        color = 'b'
    piece_type = glyph.upper()
    return pg.image.load(path.join(IMAGE_DIR, f"{color}{piece_type}.png"))

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

CHECKER_BASE = create_checkerboard()

def board_position_to_cords(position:str) -> tuple[int, int]:
    column, row = position[0], int(position[1])
    board_rect_row_index = 8 - row
    board_rect_column_index = column_letter_to_index[column]
    coordinates = BOARD_RECT[board_rect_row_index][board_rect_column_index]
    return coordinates

def cords_to_board_position(x, y) -> str:
    is_found = False
    board_cords = BOARD_RECT
    row_location:int = 0
    square_location:int = 0
    for row_index, row in enumerate(board_cords):
        if is_found: break
        for square_index, square in enumerate(row):
            x_min = square[0]
            y_min = square[1]
            x_max = x_min + SQUARE_SIZE
            y_max = y_min + SQUARE_SIZE
            # print(f"x: {x_min} <= {x} < {x_max}")
            # print(f"y: {y_min} <= {y} < {y_max}")
            # print(f"cords: {square}")
            if x >= x_min and x < x_max:
                if y >= y_min and y < y_max:
                    is_found = True
                    row_location = row_index
                    square_location = square_index
                    break
    if not is_found: return "OOB"
    # convert location_indecies into a string
    # print(row_location, square_location)
    return f'{row_index_to_legend[square_location]}{8 - (row_location)}'

def add_piece_to_surface(surface:pg.Surface, glyph:str, 
                      cords:tuple[int, int]) -> None:
    piece_img = get_piece_img(glyph)
    surface.blit(piece_img, cords)

def get_mouse_pos() -> tuple[int, int]:
    return pg.mouse.get_pos()

def terminate():
    pg.quit()
    exit()

def check_for_quit() -> None:
    for _ in pg.event.get(pg.QUIT): # rust am i right
        terminate()
    for event in pg.event.get(pg.KEYUP):
        if event.key == pg.K_ESCAPE:
            terminate()
        pg.event.post(event)

class Piece:
    def __init__(self, board, glyph, coords, is_dragging) -> None:
        # NOTE: might need to offset coords 0 and 1 because rect coords are the
        # top left and not the middle?
        self.board = board
        self.image = get_piece_img(glyph)
        self.colour = 'w' if glyph.is_upper() else 'b'
        self.rect = pg.Rect(coords[0], coords[1], SQUARE_SIZE, SQUARE_SIZE)
        self.is_dragging = is_dragging

    def update(self) -> None:
        if self.is_dragging and self.board.is_inside_board(pg.mouse.get_pos()):
            self.rect.center = pg.mouse.get_pos()
        self.board.display_surface.blit(self.image, self.rect)

class Board:
    def __init__(self, piece_matrix) -> None:
        self.piece_matrix = piece_matrix
        self.display_surface = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    def get_pieces(self) -> list[list[Piece]]:
        return self.piece_matrix

    def reset_board(self) -> None:
        self.display_surface.blit(CHECKER_BASE, (0, 0))

    def update_pieces(self) -> None:
        self.reset_board()
        for row in self.piece_matrix:
            for piece in row:
                piece.update()
    
    # TODO REMOVE MAGIC NUMBERS - make board rect dynamic,
    # use a8 and h1 as corners
    def is_inside_board(self, x, y) -> bool:
        return (100 <= x <= 450) and (100 <= y <= 450)

def fen_to_board(fen:str) -> Board:
    pass

def main(Board):
    # listen for events and update board in response to them
    game_event_loop(Board)
    Board.update_board()

# Notice that the event loop has been given its own function. This makes
# the program easier to understand.
def game_event_loop(Board):
    for event in pg.event.get():
        if event.type == pg.MOUSEBUTTONDOWN:
            for player in Board.get_players():
                # The event positions is the mouse coordinates
                if player.rect.collidepoint(event.pos):
                    player.click = True
        elif event.type == pg.MOUSEBUTTONUP:
            for player in Board.get_players():
                player.click = False
        elif event.type == pg.QUIT:
            pg.quit(); sys.exit()

if __name__ == "__main__":
    environ['SDL_VIDEO_CENTERED'] = '1'
    pg.init()
    MyBoard = Board([(50, 50, 100, 100),
                     (200, 200, 100, 100)])
    MyClock = pg.time.Clock()
    while True:
        main(MyBoard)
        pg.display.update()
        MyClock.tick(60)