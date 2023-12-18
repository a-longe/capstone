import os
import sys
import pygame as pg
import math

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

    def get_map_key(self):
        board_rel_cords = (self.rect[0] - 100,
                           self.rect[1] - 100)
        map_key = sum([int(board_rel_cords[0] / SQUARE_SIZE),
                        int(board_rel_cords[1] / SQUARE_SIZE) * 8])
        return map_key

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
            board_rel_cords = (piece_data[RECT_DATA][0] - 100,
                               piece_data[RECT_DATA][1] - 100)
            map_key = sum([int(board_rel_cords[0] / SQUARE_SIZE),
                          int(board_rel_cords[1] / SQUARE_SIZE) * 8])
            self.piece_map[map_key] = Piece(self, piece_data[RECT_DATA],
                                      piece_data[GLYPH])

    def clear_surface(self):
        self.surface.fill(0)

    def get_players(self):
        return self.piece_map.values()

    def mouse_inside_bounds(self):
        # hard-coded numbers should be fixed
        x, y = pg.mouse.get_pos()
        return (x > TOP_LEFT and x < BOTTOM_RIGHT and 
                y > TOP_LEFT and y < BOTTOM_RIGHT)

    def display_grid(self):
        # print("I should be displaying...")
        for x, y in square_coords:
            row = x / 100
            column = y / 100
            rect = pg.Rect([x, y, 100, 100])
            image = pg.Surface(rect.size).convert()
            if not (is_odd(row) ^ is_odd(column)):
                black_square(self.surface, image, rect)
            else:
                white_square(self.surface, image, rect)

    def del_piece(self, map_key):
        del self.piece_map[map_key]

    def on_mouse_down(self):
        for player in self.get_players():
            # The event positions is the mouse coordinates
            if player.rect.collidepoint(pg.mouse.get_pos()):
                if not player.click:
                    # store current center
                    player.previous_center = player.rect.center
                player.click = True

    def on_mouse_up(self):
        for player in self.get_players():
                if player.click:
                    # if valid location and is legal move()
                    if player.board.mouse_inside_bounds() and True:
                        # does player collide with another player
                        colliding_piece = [piece_2 for piece_2 in self.get_players() if piece_2.rect.collidepoint(pg.mouse.get_pos())]
                        colliding_piece.remove(player)
                        if not colliding_piece:
                            # if not colliding with any piece
                            player.snap_to_square()
                        elif player.is_white != colliding_piece[0].is_white:
                            # if colliding with piece with different colour
                            # delete player from player_list and then snap
                            self.del_piece(colliding_piece[0].get_map_key())                      
                            player.snap_to_square()
                        else:
                            player.rect.center = player.previous_center
                    # else set cords to last square
                    else:
                        player.rect.center = player.previous_center
                player.click = False

    def update_board(self):
        self.clear_surface()
        self.display_grid()
        for player in self.get_players():
            player.update()


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


if __name__ == "__main__":
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pg.init()
    MyBoard = Board(fen_to_pieces('8/5k2/3p4/1p1Pp2p/pP2Pp1P/P4P1K/8/8 b - - 99 50'))
    MyClock = pg.time.Clock()
    while True:
        print('\r', MyBoard.piece_map)
        main(MyBoard)
        pg.display.update()
        MyClock.tick(60)
