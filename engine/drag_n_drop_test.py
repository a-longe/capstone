import os
import sys
import pygame as pg
import math
from random import randint
from copy import deepcopy
from pprint import pprint

Cord = tuple[int, int]
BoardInput = list[tuple[tuple[int, int, int, int], str]]
FEN_ACTIVE_COLOUR = 1
FEN_MOVE_COUNT = 5
STARTING_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
LEN_ROW = 8
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

def my_divmod(num, divisor)->tuple[int, int]:
    if num < 0:
        is_neg = -1
    else:
        is_neg = 1

    num = abs(num)
    return is_neg*(num//divisor), is_neg*(num%divisor)

def convert_piece(piece:'Piece') -> None:
    pass

def add_tuples(t1:tuple, t2:tuple) -> tuple:
    """Precondition: tuples must both be len(2)"""
    return (t1[0] + t2[0], t1[1] + t2[1])

def multiply_in_tuple(t1:tuple[int, int], multiplier:int) -> tuple[int, int]:
    return (t1[0] * multiplier, t1[1] * multiplier)

def black_square(surface, image, rect):
    image.fill((187,190,100))
    surface.blit(image, rect)

def white_square(surface, image, rect):
    image.fill((234,240,206))
    surface.blit(image, rect)

def blue_square(surface, image, rect):
    image.fill((100, 100, 250))
    surface.blit(image, rect)

def make_squares_blue(surface, squares:list[int]) -> None:
    for square in squares:
        x, y = my_divmod(square, 8)[1] * SQUARE_SIZE + 100, my_divmod(square, 8)[0] * SQUARE_SIZE + 100
        rect = pg.Rect([x, y, 100, 100])
        image = pg.Surface(rect.size).convert()
        blue_square(surface, image, rect)

def get_snap_cords(x, y) -> Cord:
    return (math.floor(x / SQUARE_SIZE) * SQUARE_SIZE,
            math.floor(y / SQUARE_SIZE) * SQUARE_SIZE)

def is_possible_square_r_c(square:tuple[int, int]) -> bool:
    return (0 <= square[0] <= 7) and (0 <= square[1] <= 7)

def r_c_to_int(square:tuple[int, int]) -> int:
    return square[0]*8 + square[1]

def get_square_after_move(start:int, offset_r_c:tuple[int, int]) -> int:
    start_r_c = my_divmod(start, 8)
    new_square_r_c = add_tuples(start_r_c, offset_r_c)
    return r_c_to_int(new_square_r_c)

def will_move_out(starting_square:int, offset_r_c:tuple[int, int]) -> bool:
    square_r_c = my_divmod(starting_square, 8)
    new_square_r_c = add_tuples(square_r_c, offset_r_c)
    will_go_out = not is_possible_square_r_c(new_square_r_c)
    print(f"the move: {square_r_c} with offset {offset_r_c} goes to{new_square_r_c} and will_go_out = {will_go_out}")
    return will_go_out

def fen_to_pieces(fen) -> BoardInput:
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

def piece_map_to_board_input(piece_map:dict[int:'Piece']) -> BoardInput:
    pieces = piece_map.values()
    return [(piece.rect, piece.glyph) for piece in pieces]


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
        self.glyph = glyph
        self.square = self.get_square_index()
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

    def return_to_previous(self) -> None:
        self.rect.center = self.previous_center

    def is_same_colour(self, piece_2:'Piece') -> bool:
        return self.is_white == piece_2.is_white

    def can_pickup(self) -> bool:
        """
        Would not be able to be picked up if piece cant help with a check, or if
        its not the active colour
        """ 
        return self.is_white == self.board.is_white_turn

    def get_square_index(self) -> int:
        x, y = self.board.relative_board_cords(*self.rect[:2])
        x //= SQUARE_SIZE
        y //= SQUARE_SIZE
        return (y * 8) + x

    def move_to(self, new_square:int):
        # with new index as key, set value to self
        # then take original location in map and delete
        # set self.square to new location
        old_square = self.square
        if new_square == old_square: return
        print(f"move(): from: {old_square} to {new_square}")

        self.board.piece_map[new_square] = self
        del self.board.piece_map[old_square]

        self.square = self.get_square_index()

    def get_sliding_moves(self, offset:tuple[int, int]) -> list[int, int]:
        start_square = self.square
        depth = 1
        valid_moves = []
        while not will_move_out(start_square, multiply_in_tuple(offset, depth)):
            new_square = get_square_after_move(start_square, multiply_in_tuple(offset, depth))
            print(new_square)
            if new_square in self.board.piece_map.keys():
                if not self.board.piece_map[new_square].is_same_colour(self):
                    # if the piece is not the same colour as this one
                    valid_moves.append((start_square, new_square))
                break   
            else:
                # empty square
                valid_moves.append((start_square, new_square))
                depth += 1
        return valid_moves



    def snap_to_square(self) -> None:
        if self.board.mouse_inside_bounds():
            player_cords = (self.rect.center[0], self.rect.center[1])
            self.rect.topleft = get_snap_cords(*player_cords)


class Bishop(Piece):
    def __init__(self, board, rect, glyph):
        Piece.__init__(self, board, rect, glyph)


    def get_legal_moves(self) -> list[tuple[int, int]]:
        OFFSETS = ((-1, -1) ,(-1, 1), (1, 1), (1, -1))
        valid_moves = []
        for offset in OFFSETS:
            valid_moves += self.get_sliding_moves(offset)
        return valid_moves



class Board:
    # Each position corresponds to the arguments needed to instantiate
    # the PyGame.Rect class: (x, y, width, height) corresponding to a player

    # The Board class updates itself by asking the players to paint themselves.

    # It has a number of methods that exist so other parts of the program can
    # inquire about the current state of the board
    def __init__(self, game, positions:BoardInput, is_white_turn:bool, 
        move_count:int):

        self.game = game
        self.surface = pg.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
        self.piece_map = {}
        for piece_data in positions:
            rect = piece_data[RECT_DATA]
            glyph = piece_data[GLYPH]
            square:int = self.get_square_index(*rect[:2])
            match glyph:
                case 'b' | 'B':
                    self.piece_map[square] = Bishop(self, rect, glyph)
        self.is_white_turn = is_white_turn
        self.move_count = move_count

    def get_fen(self) -> str:
        fen = ''
        for c_i in range(LEN_ROW):
            consecutive_empty = 0
            for r_i in range(LEN_ROW):
                square_index = (8*c_i) + r_i
                try:
                    glyph = self.piece_map[square_index].glyph
                    if consecutive_empty > 0:
                        fen += str(consecutive_empty)
                        consecutive_empty = 0
                    fen += glyph
                except KeyError:
                    consecutive_empty += 1
            if consecutive_empty > 0:
                fen += str(consecutive_empty)
            fen += '/'
        fen = fen[:-1] # remove last slash, easier than checking if its last row

        fen += 'w - - 0 1'
        return fen



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
    
    def relative_board_cords(self, x, y) -> Cord:
        return (x-TOP_LEFT, y-TOP_LEFT)

    def switch_is_white_turn(self) -> str:
        return not self.is_white_turn

    def get_square_index(self, x, y) -> int:
        """
        Precondition: x, y point must be inside board already
        """
        x, y = self.relative_board_cords(x, y)
        x //= SQUARE_SIZE
        y //= SQUARE_SIZE
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
            if piece.rect.collidepoint(pg.mouse.get_pos()) and \
               piece.can_pickup():
                if not piece.click:
                    # store current center
                    piece.previous_center = piece.rect.center
                piece.click = True
                squares = list(map(lambda t : t[1], self.game.get_current_board().piece_map[piece.get_square_index()].get_legal_moves()))
                print(self.game.get_current_board())
                make_squares_blue(self.game.get_current_board().surface, squares)
                print(self)


    def on_mouse_up(self) -> None: 
        pieces_to_be_deleted = []
        pieces_to_be_moved = [] 
        for piece in self.get_players():
            
            if not piece.click: continue

            # if valid location and is legal move()
            if piece.board.mouse_inside_bounds() and True:
                mouse_square = self.get_square_index(*pg.mouse.get_pos())
                # does piece collide with another piece
                if mouse_square in self.piece_map.keys():
                    # mouse_square must be in map
                    piece_to_take = self.piece_map[mouse_square]
                    if not piece.is_same_colour(piece_to_take):
                        # if colliding with piece with different colour
                        # delete piece from piece_list and then snap
                        pieces_to_be_deleted.append(piece_to_take)                      
                        piece.snap_to_square()
                        pieces_to_be_moved.append(piece)
                    else:
                        piece.return_to_previous()
                else:
                    # if not colliding with any piece
                    piece.snap_to_square()
                    pieces_to_be_moved.append(piece)
            # else set cords to last square
            else:
                piece.return_to_previous()
            piece.click = False
        for piece_to_del in pieces_to_be_deleted:
            self.del_piece(piece_to_del)
        for piece_to_be_moved in pieces_to_be_moved:
            new_square = piece_to_be_moved.get_square_index()
            old_square = piece_to_be_moved.square
            self.game.add_board(self.get_board_after_move(old_square,
                                                          new_square))
            print(f"move #{len(self.game.boards) - 1}")
        #pprint(self.piece_map)


    def get_board_after_move(self, start_square:int, end_square:int) -> 'Board':
        '''
        1. determine the piece map after a move
            a.
        2. convert from piece map back to the format we used to instantiate
            a board [(rect, glyph)]
        3. return said board
        '''
        new_piece_map = self.piece_map
        new_piece_map[start_square].move_to(end_square)
        board_input = piece_map_to_board_input(new_piece_map)
        new_move_count = self.move_count + 1
        return Board(self.game, board_input, self.switch_is_white_turn(),
                     new_move_count)


    def update_board(self):
        self.clear_surface()
        self.display_grid()
        for piece in self.get_players():
            piece.update()

class Game:
    def __init__(self, starting_fen=STARTING_FEN) -> None:
        fen_componants = starting_fen.split(' ')
        is_white_turn = fen_componants[FEN_ACTIVE_COLOUR] == 'w'
        move_count = int(fen_componants[FEN_MOVE_COUNT])
        self.boards = [Board(self, fen_to_pieces(starting_fen), is_white_turn, 
                             move_count)]
        min_to_sec = lambda m : m * 60
        self.white_time = min_to_sec(5)
        self.black_time = min_to_sec(5)
        self.is_game_over = False

    def get_current_board(self):
        return self.boards[-1]

    def add_board(self, board) -> None:
        self.boards.append(board)



def main(game):
    # listen for events and update board in response to them
    cur_board = game.get_current_board()
    game_event_loop(game)
    cur_board.update_board()


# Notice that the event loop has been given its own function. This makes
# the program easier to understand.
def game_event_loop(game):
    cur_board = game.get_current_board()
    for event in pg.event.get():
        if event.type == pg.MOUSEBUTTONDOWN:
            cur_board.on_mouse_down()
        elif event.type == pg.MOUSEBUTTONUP:
            cur_board.on_mouse_up()
        elif event.type == pg.QUIT:
            pg.quit()
            sys.exit()

def get_random_fen() -> str:
    with open('/home/alonge/Documents/code/capstone/engine/random_fens.txt') as fen_file:
        fens = fen_file.readlines()
    fen = fens[randint(0, len(fens) - 1)]
    print(fen)
    return fen

test_fen_strings = [
'8/8/8/8/8/8/8/8 w - - 0 1',
'kK6/8/8/8/8/8/8/8 w - - 0 1',
'8/8/8/3bB3/8/8/8/8 b - - 0 1',
get_random_fen()
]

if __name__ == "__main__":
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pg.init()
    game = Game(test_fen_strings[2])
    MyClock = pg.time.Clock()   
    while not game.is_game_over:
        main(game)
        pg.display.update()
        MyClock.tick(60)
