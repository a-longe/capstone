import pygame as pg
import os
import sys
import math
from random import randint
from pprint import pprint

PiecePositionInput = tuple[int, int, int, str]
PIECE_X = 0
PIECE_Y = 1
PIECE_SIZE = 2 # do not need width and height as pieces are square images
PIECE_GLYPH = 3

BoardFenInput = tuple[list[PiecePositionInput], bool, int, int, dict[str:bool], int]

STARTING_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

Move = tuple[int, int]
MOVE_START = 0
MOVE_END = 1

Cord = tuple[int, int]
CORD_X = 0
CORD_Y = 1

TOP_LEFT = 100
BOTTOM_RIGHT = 900
SQUARE_SIZE = 100
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000

SQUARE_COORDS = [[i, j] for i in range(TOP_LEFT, BOTTOM_RIGHT, SQUARE_SIZE) \
                for j in range(TOP_LEFT, BOTTOM_RIGHT, SQUARE_SIZE)]


IMAGE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images')

class MoveEvalResponces:
    INVALID_MOVE = 0
    MOVE_TO_EMPTY = 1
    CAPTURE_MOVE = 2

def is_odd(num) -> bool:
    return bool(num % 2)

def black_square(surface, image, rect):
    image.fill((187,190,100))
    surface.blit(image, rect)


def white_square(surface, image, rect):
    image.fill((234,240,206))
    surface.blit(image, rect)


def blue_square(surface, image, rect):
    image.fill((100, 100, 250))
    surface.blit(image, rect)

def get_snap_cords(x, y) -> Cord:
    return (math.floor(x / SQUARE_SIZE) * SQUARE_SIZE,
            math.floor(y / SQUARE_SIZE) * SQUARE_SIZE)

def get_piece_img(glyph:str) -> pg.Surface:
    if glyph.isupper():
        color = 'w'
    else:
        color = 'b'
    piece_type = glyph.upper()
    return pg.image.load(os.path.join(IMAGE_DIR, f"{color}{piece_type}.png"))

def on_mouse_down(game):
    for piece in game.get_current_board().get_pieces():
        # The event positions is the mouse coordinates
        if piece.rect.collidepoint(pg.mouse.get_pos()) and \
           piece.can_pickup():
            # store current center
            piece.previous_center = piece.rect.center
            piece.click = True


def on_mouse_up(game) -> None: 
    pieces_to_be_deleted = []
    pieces_to_be_moved = [] 

    piece = game.get_current_board().get_clicked_piece()
    if piece == "ERROR": return # would like to make this nicer but will get back to it later

    mouse_square = game.get_square_index(*pg.mouse.get_pos())

    match game.get_current_board().eval_move(piece, mouse_square):
        case MoveEvalResponces.INVALID_MOVE:
            piece.return_to_previous()
        case MoveEvalResponces.MOVE_TO_EMPTY:
            pieces_to_be_moved.append(piece)
        case MoveEvalResponces.CAPTURE_MOVE:
            pieces_to_be_moved.append(piece)
            pieces_to_be_deleted.append(game.get_current_board().piece_map[mouse_square])

    piece.snap_to_square()
    piece.click = False


    for piece_to_del in pieces_to_be_deleted:
        game.get_current_board().del_piece(piece_to_del)
    for piece_to_be_moved in pieces_to_be_moved:
        new_square = piece_to_be_moved.get_square_index()
        old_square = piece_to_be_moved.square
        game.add_board(game.get_current_board().get_board_after_move(old_square,
                                                                    new_square))
        print(f"move #{len(game.boards) // 2}")
        print(game.get_current_board().get_fen())
    #pprint(self.piece_map)

def fen_to_pieces(fen) -> PiecePositionInput:
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
                lo_pieces.append((c_i * SQUARE_SIZE + SQUARE_SIZE,
                                  r_i * SQUARE_SIZE + SQUARE_SIZE,
                                  SQUARE_SIZE, 
                                  char))
            c_i += 1
        r_i += 1
    return lo_pieces


def fen_to_board_input(fen) -> BoardFenInput:
    piece_str, active_colour_str, casting_rights_str, en_passent_str, \
    move_count_str, halfmove_count_str = fen.split(' ')

    board_piece_input = fen_to_pieces(fen)
    is_white = True if active_colour_str == 'w' else False
    casting_rights = {
        'K': False,
        'Q': False,
        'k': False,
        'q': False
    }
    for castle_right in casting_rights_str:
        if castle_right in casting_rights.keys():
            casting_rights[castle_right] = True
    en_passent_target = int(en_passent_str) if en_passent_str != '-' else -1
    move_count = int(move_count_str)
    halfmove_count = int(halfmove_count_str)
    return board_piece_input, is_white, move_count, halfmove_count, \
           casting_rights, en_passent_target


class Piece:
    def __init__(self, board, rect, glyph) -> None:
        self.board = board
        self.rect = rect
        self.glyph = glyph
        self.square = board.game.get_square_index(*rect[:2])
        self.previous_center = self.rect.center
        self.click = False
        self.image = pg.transform.scale(get_piece_img(glyph), (SQUARE_SIZE, 
                                                               SQUARE_SIZE))
        self.is_white = glyph.isupper()

    def update(self) -> None:
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
        x, y = self.board.game.relative_board_cords(*self.rect[:2])
        x //= SQUARE_SIZE
        y //= SQUARE_SIZE
        return (y * 8) + x

    def move_to(self, new_square:int) -> None:
        # with new index as key, set value to self
        # then take original location in map and delete
        # set self.square to new location
        old_square = self.square
        if new_square == old_square: return
        print(f"move(): from: {old_square} to {new_square}")

        self.board.piece_map[new_square] = self
        del self.board.piece_map[old_square]

        self.square = self.get_square_index()

    def get_legal_moves(self) -> list[Move]:
        print("ERROR: This piece has not been classified past being a piece")
        return [(self.square, self.square)]


    def snap_to_square(self) -> None:
        if self.board.game.mouse_inside_bounds():
            player_cords = (self.rect.center[0], self.rect.center[1])
            self.rect.topleft = get_snap_cords(*player_cords)


class Bishop(Piece):
    def __init__(self, board, rect, glyph) -> None:
        Piece.__init__(self, board, rect, glyph)


    def get_legal_moves(self) -> list[Move]:
        OFFSETS = ((-1, -1) ,(-1, 1), (1, 1), (1, -1))
        valid_moves = []
        for offset in OFFSETS:
            valid_moves += self.board.get_sliding_moves(self.square, offset)
        return valid_moves

class Rook(Piece):
    def __init__(self, board, rect, glyph) -> None:
        Piece.__init__(self, board, rect, glyph)


    def get_legal_moves(self) -> list[Move]:
        OFFSETS = ((1, 0) ,(-1, 0), (0, 1), (0, -1))
        valid_moves = []
        for offset in OFFSETS:
            valid_moves += self.board.get_sliding_moves(self.square, offset)
        return valid_moves

class Board:
    def __init__(self, game, piece_positions:list[PiecePositionInput],
                is_white_turn:bool, move_count:int, halfmove_count:int,
                casting_rights:dict[str:bool], en_passent_target:int) -> None:
        self.surface = game.surface # passed by reference
        self.game = game
        self.piece_map = {}
        for piece_data in piece_positions:
            rect = pg.Rect(piece_data[PIECE_X], piece_data[PIECE_Y],
                    piece_data[PIECE_SIZE], piece_data[PIECE_SIZE])
            square = self.game.get_square_index(*rect[:2])
            glyph = piece_data[PIECE_GLYPH]
            match glyph:
                case 'b' | 'B':
                    self.piece_map[square] = Bishop(self, rect, glyph)
                case 'r' | 'R':
                    self.piece_map[square] = Rook(self, rect, glyph)
                case _:
                    self.piece_map[square] = Piece(self, rect, glyph)
        self.is_white_turn = is_white_turn
        self.move_count = move_count
        self.halfmove_count = halfmove_count
        self.casting_rights = casting_rights
        self.en_passent_target = en_passent_target

    def eval_move(self, piece, new_square) -> int:
        # if valid location and is legal move()
        is_valid = self.game.mouse_inside_bounds() and True

        if is_valid:
            # does piece collide with another piece
            is_colliding = new_square in game.get_current_board().piece_map.keys()

            if is_colliding:
                piece_to_take = game.get_current_board().piece_map[new_square]
                is_diff_colour = not piece.is_same_colour(piece_to_take)

                if is_diff_colour:
                    return MoveEvalResponces.CAPTURE_MOVE
                else:
                    return MoveEvalResponces.INVALID_MOVE
            else:
                return MoveEvalResponces.MOVE_TO_EMPTY
        else:
            return MoveEvalResponces.INVALID_MOVE

    def piece_map_to_board_input(self, piece_map:dict[int:'Piece']) -> PiecePositionInput:
        pieces = piece_map.values()
        return [(*piece.rect[:3], piece.glyph) for piece in pieces]

    def get_board_after_move(self, start_square:int, end_square:int) -> 'Board':
        '''
        1. determine the piece map after a move
        2. convert from piece map back to the format we used to instantiate
            a board [(rect, glyph)]
        3. return said board
        '''
        new_piece_map = self.piece_map
        new_piece_map[start_square].move_to(end_square)
        board_input = self.piece_map_to_board_input(new_piece_map)   
        new_move_count = self.move_count + 1 if self.is_white_turn else self.move_count
        return Board(self.game, board_input, self.switch_is_white_turn(),
                     new_move_count, self.halfmove_count+1, 
                     self.casting_rights, self.en_passent_target)

    def get_clicked_piece(self) -> Piece:
        for piece in self.piece_map.values():
            if piece.click: return piece
        return "ERROR" 

    def get_sliding_moves(self, start_square, offset:tuple[int, int]) -> list[int, int]:
        depth = 1
        valid_moves = []
        while not will_move_out(start_square, multiply_in_tuple(offset, depth)):
            new_square = get_square_after_move(start_square, multiply_in_tuple(offset, depth))
            if new_square in self.piece_map.keys():
                if not self.piece_map[new_square].is_same_colour(self.piece_map[start_square]):
                    # if the piece is not the same colour as this one
                    valid_moves.append((start_square, new_square))
                break   
            else:
                # empty square
                valid_moves.append((start_square, new_square))
                depth += 1
        return valid_moves

    def get_fen(self) -> str:
        fen = ''
        for c_i in range(8):
            consecutive_empty = 0
            for r_i in range(8):
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

        fen += ' w ' if self.is_white_turn else ' b '

        for castle_right in self.casting_rights.keys():
            if self.casting_rights[castle_right]:
                fen += castle_right
        fen+=' '

        fen += '- ' if self.en_passent_target == -1 else str(self.en_passent_target) + ' '
        # NOTE: MIGHT HAVE TO CHANGE DEPENDING ON EN PASSENT REPERSENTATION

        fen += str(self.move_count) + ' '

        fen += str(self.halfmove_count)

        return fen

    def get_pieces(self) -> list[Piece]:
        return self.piece_map.values()


    def switch_is_white_turn(self) -> str:
        return not self.is_white_turn


    def del_piece(self, piece:Piece) -> None:
        map_key = self.game.get_square_index(*piece.rect[:2])
        del self.piece_map[map_key]

    def update_pieces(self) -> None:
        for piece in self.get_pieces():
            piece.update()


class Game:
    def __init__(self, starting_fen=STARTING_FEN) -> None:
        self.surface = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.boards = [Board(self, *fen_to_board_input(starting_fen))]
        min_to_sec = lambda m : m * 60
        self.white_time = min_to_sec(5)
        self.black_time = min_to_sec(5)
        self.is_game_over = False
        """
        Note:
        Used to have is_white_turn and move_count in this init but because
        they WERE only used to create the board, it makes WAYYYY more sense to 
        have a function that turns the fen string into everything EXCEPT the 
        game being passed in
        """

    def is_inside_bounds(self, x, y) -> bool:
        return (x >= TOP_LEFT and x <= BOTTOM_RIGHT and 
                y >= TOP_LEFT and y <= BOTTOM_RIGHT)

    def mouse_inside_bounds(self) -> bool:
        return self.is_inside_bounds(*pg.mouse.get_pos())

    def relative_board_cords(self, x, y) -> Cord:
        return (x-TOP_LEFT, y-TOP_LEFT)

    def get_square_index(self, x, y) -> int:
        """
        Precondition: x, y point must be inside board already
        """
        x, y = self.relative_board_cords(x, y)
        x //= SQUARE_SIZE
        y //= SQUARE_SIZE
        return (y * 8) + x

    def get_current_board(self) -> Board:
        return self.boards[-1]

    def add_board(self, board) -> None:
        self.boards.append(board)

    def display_grid(self) -> None:
        for x, y in SQUARE_COORDS:
            row = x / 100
            column = y / 100
            rect = pg.Rect([x, y, 100, 100])
            image = pg.Surface(rect.size).convert()
            if not (is_odd(row) ^ is_odd(column)):
                black_square(self.surface, image, rect)
            else:
                white_square(self.surface, image, rect)

    def clear_surface(self) -> None:
        self.surface.fill(0)

    def update_game(self) -> None:
        self.clear_surface()
        self.display_grid()
        self.get_current_board().update_pieces()
 

# the main loop needs to call an event loop to establish an interactive game
# and needs to call the game to update itself
def main(cur_game:Game) -> None:
    game_event_loop(game)
    game.update_game()


# Notice that the event loop has been given its own function. This makes
# the program easier to understand.
def game_event_loop(game) -> None:
    for event in pg.event.get():
        if event.type == pg.MOUSEBUTTONDOWN:
            on_mouse_down(game)
        elif event.type == pg.MOUSEBUTTONUP:
            on_mouse_up(game)
        elif event.type == pg.QUIT:
            pg.quit()
            sys.exit()


RAND_FENS_PATH = '/home/alonge/Documents/code/capstone/engine/random_fens.txt'
def get_random_fen() -> str:
    with open(RAND_FENS_PATH) as fen_file:
        fens = fen_file.readlines()
    fen = fens[randint(0, len(fens) - 1)]
    print(fen)
    return fen

test_fen_strings = [
'8/8/8/8/8/8/8/8 w - - 0 1',
'kK6/8/8/8/8/8/8/8 w - - 0 1',
'k7/8/8/3bB3/3rR3/8/8/8 b KQkq - 0 1',
get_random_fen()
]

"""
these lines code below are pygame witchcraft but essentially
we need to center the executable environment, initiate pygame
and create the game of chess we're going to play.
The clock simply makes sure that the pygame window is always doing
something, otherwise the operating system attempts the shut it down
because it dosent think the program is doing anything then, we want 
the main loop (main()) to run every frame followed by updating pygame's
display, not to be confused with updating the board or pieces.
"""
if __name__ == "__main__":
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pg.init()
    game = Game(STARTING_FEN)
    MyClock = pg.time.Clock()
    while not game.is_game_over:
        main(game)
        pg.display.update()
        MyClock.tick(60)