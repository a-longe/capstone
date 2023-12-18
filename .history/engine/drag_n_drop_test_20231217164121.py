import os
import sys
import pygame as pg
import math
from pprint import pprint

Cord = tuple[int, int]
TOP_LEFT = 100
BOTTOM_RIGHT = 900
SQUARE_SIZE = 100
SCREEN_SIZE = 1000

RECT_DATA = 0
GLYPH = 1

def is_even(n):
    return 0 == n % 2

def is_odd(n):
    return 1 == n % 2

def black_square(surface, image, rect):
    image.fill((187,190,100))
    surface.blit(image, rect)

def white_square(surface, image, rect):
    image.fill((234,240,206))
    surface.blit(image, rect)

def get_snap_cords(x, y) -> Cord:
    return (math.floor(x / SQUARE_SIZE) * SQUARE_SIZE,
            math.floor(y / SQUARE_SIZE) * SQUARE_SIZE)

def fen_to_pieces(fen) -> list[tuple[tuple[int, int, int, int], str]]:
    lo_pieces = []
    pieces = fen.split(' ')[0]
    rows = pieces.split('/')
    r_i = 0
    for row in rows:
        c_i = 0
        for char in row:
            if char.isdigit():
                c_i += int(char) - 1
            else:
                # convert c_i and r_i into square
                lo_pieces.append(((c_i * SQUARE_SIZE + SQUARE_SIZE,
                                   r_i * SQUARE_SIZE + SQUARE_SIZE,
                                    SQUARE_SIZE, SQUARE_SIZE), char))
            c_i += 1
        r_i += 1
    return lo_pieces


IMAGE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images')

def get_piece_img(glyph:str) -> pg.Surface:
    if glyph.isupper():
        color = 'w'
    else:
        color = 'b'
    piece_type = glyph.upper()
    return pg.image.load(os.path.join(IMAGE_DIR, f"{color}{piece_type}.png"))


square_coords = [[i, j] for i in range(TOP_LEFT, BOTTOM_RIGHT, SQUARE_SIZE) \
                for j in range(TOP_LEFT, BOTTOM_RIGHT, SQUARE_SIZE)]


class Piece:
    # A Piece object needs to know about the Board because its behaviour
    # depends on the location of other Piece objects--only the Board knows
    # about them--that's why Board is an argument. It also needs to know its
    # dimensions, so we pass them in rect
    def __init__(self, Board, rect, glyph):
        self.board = Board
        self.rect = pg.Rect(rect)
        # self.cord = square_to_cords(square)
        self.previous_center = self.rect.center
        # a Piece object has a click attribute that is true if the
        # left mouse button is down and on top of the Piece
        self.click = False
        self.image = pg.transform.scale(get_piece_img(glyph), (SQUARE_SIZE, 
                                                               SQUARE_SIZE))
        self.is_white = glyph.isupper()

    # Check that the player has been selected and that the mouse will
    # not cause the player to bleed out of bounds.

    # To deal with collisions, save current position, and then move
    # the player to the mouse position. If there is a collision, then
    # move the rectangle back to the previous position.

    # Regardless, draw the player
    def update(self):
        if (self.click):
            self.rect.center = pg.mouse.get_pos()
        self.board.surface.blit(self.image, self.rect)

    def snap_to_square(self) -> None:
        if self.board.mouse_inside_bounds():
            player_cords = (self.rect.center[0], self.rect.center[1])
            self.rect.topleft = get_snap_cords(*player_cords)




class Board:
    # Each position corresponds to the arguments needed to instantiate
    # the PyGame.Rect class: (x, y, width, height) corresponding to a player

    # The Board class updates itself by asking the players to paint themselves.

    # It has a number of methods that exist so other parts of the program can
    # inquire about the current state of the board
    def __init__(self, positions):
        self.surface = pg.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
        self.piece_map = {}
        for piece_data in positions:
            rect = piece_data[RECT_DATA]
            glyph = piece_data[GLYPH]
            square:int = self.get_square_index(*rect[:2])
            self.piece_map[square] = Piece(self, rect, glyph)

    def clear_surface(self):
        self.surface.fill(0)

    def get_players(self):
        return self.piece_map.values()
    
    def set_piece(self, square:int, piece:Piece):
        self.piece_map[square] = piece

    def is_inside_bounds(self, x, y) -> bool:
        return (x >= TOP_LEFT and x <= BOTTOM_RIGHT and 
                y >= TOP_LEFT and y <= BOTTOM_RIGHT)

    def mouse_inside_bounds(self):
        return self.is_inside_bounds(*pg.mouse.get_pos())

    def get_square_index(self, x, y) -> int:
        """
        Precondition: x, y point must be inside board already
        """
        x -= 100
        y -= 100
        x //= 100
        y //= 100
        return (y * 8) + x
        
    def display_grid(self):
        for x, y in square_coords:
            row = x / 100
            column = y / 100
            rect = pg.Rect([x, y, 100, 100])
            image = pg.Surface(rect.size).convert()
            if not (is_odd(row) ^ is_odd(column)):
                black_square(self.surface, image, rect)
            else:
                white_square(self.surface, image, rect)

    def del_piece(self, piece:Piece):
        map_key = self.get_square_index(*piece.rect[:2])
        del self.piece_map[map_key]

    def on_mouse_down(self):
        for piece in self.get_players():
            # The event positions is the mouse coordinates
            if piece.rect.collidepoint(pg.mouse.get_pos()):
                if not piece.click:
                    # store current center
                    piece.previous_center = piece.rect.center
                piece.click = True

    def on_mouse_up(self) -> None: 
        pieces_to_be_deleted = []
        for piece in self.get_players():
                if piece.click:
                    # if valid location and is legal move()
                    if piece.board.mouse_inside_bounds() and True:
                        # does piece collide with another piece
                        colliding_piece = [piece_2 for piece_2 in self.get_players() if piece_2.rect.collidepoint(pg.mouse.get_pos())]
                        colliding_piece.remove(piece)
                        if not colliding_piece:
                            # if not colliding with any piece
                            piece.snap_to_square()
                        elif piece.is_white != colliding_piece[0].is_white:
                            # if colliding with piece with different colour
                            # delete piece from piece_list and then snap
                            pieces_to_be_deleted.append(colliding_piece[0])                      
                            piece.snap_to_square()
                        else:
                            piece.rect.center = piece.previous_center
                    # else set cords to last square
                    else:
                        piece.rect.center = piece.previous_center
                piece.click = False
        for piece_to_del in pieces_to_be_deleted:
            self.del_piece(piece_to_del)
        pprint(self.piece_map)

    def update_board(self):
        self.clear_surface()
        self.display_grid()
        for piece in self.get_players():
            piece.update()


def main(Board):
    # listen for events and update board in response to them
    game_event_loop(Board)
    Board.update_board()


# Notice that the event loop has been given its own function. This makes
# the program easier to understand.
def game_event_loop(Board):
    for event in pg.event.get():
        if event.type == pg.MOUSEBUTTONDOWN:
            Board.on_mouse_down()
        elif event.type == pg.MOUSEBUTTONUP:
            Board.on_mouse_up()
        elif event.type == pg.QUIT:
            pg.quit()
            sys.exit()


"""
Testing Fen Strings:
8/8/8/8/8/8/8/8 w - - 0 1
kK6/8/8/8/8/8/8/8 w - - 0 1
8/P3N3/2n1P3/2p4k/3Qp3/1qR3rp/3K3P/R5r1 w - - 0 1
"""

if __name__ == "__main__":
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pg.init()
    MyBoard = Board(fen_to_pieces('kK6/8/8/8/8/8/8/8 w - - 0 1'))
    MyClock = pg.time.Clock()
    while True:
        main(MyBoard)
        pg.display.update()
        MyClock.tick(60)
