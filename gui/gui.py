import pygame as pg
import os
import sys
import math
from random import randint
from pprint import pprint

sys.path.insert(0, "/home/alonge/Documents/code/capstone/python-chess")
import uci_handler as engine


PiecePositionInput = tuple[int, int, int, str]
PIECE_X = 0
PIECE_Y = 1
PIECE_SIZE = 2 # do not need width and height as pieces are square images
PIECE_GLYPH = 3

DIVMOD_ROW = 0
DIVMOD_COLUMN = 1

BoardFenInput = tuple[list[PiecePositionInput], bool, int, int, dict[str,bool], int]

STARTING_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

Move = tuple[int, int]
MOVE_START = 0
MOVE_END = 1

Cord = tuple[int, int]
CORD_X = 0
CORD_Y = 1

IMAGE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images')

INT_TO_LETTER = {
    0: 'a',
    1: 'b',
    2: 'c',
    3: 'd',
    4: 'e',
    5: 'f',
    6: 'g',
    7: 'h',
}

class MoveEvalResponces:
    INVALID_MOVE = 0
    MOVE_TO_EMPTY = 1
    CAPTURE_MOVE = 2
    CASTLE_KINGSIDE = 3
    CASTLE_QUEENSIDE = 4
    EN_PASSENT = 5
    DOUBLE_PUSH = 6
    PROMOTION = 7

def add_tuples(t1:tuple, t2:tuple) -> tuple[int, int]:
    """Precondition: tuples must both be len(2)"""
    return (t1[0] + t2[0], t1[1] + t2[1])

def my_divmod(num, divisor)->tuple[int, int]:
    if num < 0:
        is_neg = -1
    else:
        is_neg = 1

    num = abs(num)
    return is_neg*(num//divisor), is_neg*(num%divisor)

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

def make_squares_blue(surface, square_size, squares:list[int]) -> None:
    for square in squares:
        x, y = my_divmod(square, 8)[1] * square_size + 100, my_divmod(square, 8)[0] * square_size + 100
        rect = pg.Rect([x, y, 100, 100])
        image = pg.Surface(rect.size).convert()
        blue_square(surface, image, rect)

def square_index_to_algebraic(square_index:int) -> str:
    row, column = divmod(square_index, 8)
    return INT_TO_LETTER[column] + str(8 - (row))

def algebraic_to_square(square:str) -> int:
    column_str, row = square[0], int(square[1])
    column = {v:k for k, v in INT_TO_LETTER.items()}[column_str]
    return (8 - row) * 8 + column

def multiply_in_tuple(t1:tuple[int, int], multiplier:int) -> tuple[int, int]:
    return (t1[0] * multiplier, t1[1] * multiplier)

def will_move_out(starting_square:int, offset_r_c:tuple[int, int]) -> bool:
    square_r_c = my_divmod(starting_square, 8)
    new_square_r_c = add_tuples(square_r_c, offset_r_c)
    will_go_out = not is_possible_square_r_c(new_square_r_c)
    #print(f"the move: {square_r_c} with offset {offset_r_c} goes to{new_square_r_c} and will_go_out = {will_go_out}")
    return will_go_out

def is_possible_square_r_c(square:tuple[int, int]) -> bool:
    return (0 <= square[0] <= 7) and (0 <= square[1] <= 7)

def r_c_to_int(square:tuple[int, int]) -> int:
    return square[0]*8 + square[1]

def get_square_after_move(start:int, offset_r_c:tuple[int, int]) -> int:
    start_r_c = my_divmod(start, 8)
    new_square_r_c = add_tuples(start_r_c, offset_r_c)
    return r_c_to_int(new_square_r_c)

def get_snap_cords(x, y, square_size) -> Cord:
    return (math.floor(x / square_size) * square_size,
            math.floor(y / square_size) * square_size)

def get_piece_img(glyph:str) -> pg.Surface:
    if glyph.isupper():
        color = 'w'
    else:
        color = 'b'
    piece_type = glyph.upper()
    return pg.image.load(os.path.join(IMAGE_DIR, f"{color}{piece_type}.png"))

def on_mouse_down(game):
    print(f"clicked on {game.get_square_index(*pg.mouse.get_pos())}")
    for piece in game.get_current_board().get_pieces():
        # The event positions is the mouse coordinates
        if piece.rect.collidepoint(pg.mouse.get_pos()) and \
           piece.can_pickup():
            print(piece)
            # store current center
            piece.previous_center = piece.rect.center
            piece.click = True

def on_mouse_up(game) -> None:
    cur_board = game.get_current_board()
    piece = game.get_current_board().get_clicked_piece()
    if piece == -1: return # would like to make this nicer but will get back to it later
    start_square = piece.square
    end_square = game.get_square_index(*pg.mouse.get_pos())
    move = (start_square, end_square)
    piece.snap_to_square()
    piece.click = False
    
    """
    We're going to check if a move is legal her now instead of checking in eval_move
    """

    new_board = cur_board.get_board_after_move(piece, start_square, end_square)
    # check for invalid move
    if new_board == -1 or move not in piece.get_valid_moves(): 
        return

    game.add_board(new_board)
    print(game.get_current_board().get_fen())
    print(f"is_in_check? white: {new_board.is_in_check(True)} black: {new_board.is_in_check(False)}")
    cur_board.print()


def fen_to_pieces(fen, game) -> PiecePositionInput:
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
                lo_pieces.append((c_i * game.square_size + game.square_size,
                                  r_i * game.square_size + game.square_size,
                                  game.square_size,
                                  char))
            c_i += 1
        r_i += 1
    return lo_pieces


def fen_to_board_input(fen, game) -> BoardFenInput:
    piece_str, active_colour_str, castling_rights_str, en_passent_str, \
    move_count_str, halfmove_count_str = fen.split(' ')

    board_piece_input = fen_to_pieces(fen, game)
    is_white = True if active_colour_str == 'w' else False
    castling_rights = {
        'K': False,
        'Q': False,
        'k': False,
        'q': False
    }
    for castle_right in castling_rights_str:
        if castle_right in castling_rights.keys():
            castling_rights[castle_right] = True
    en_passent_target = int(en_passent_str) if en_passent_str != '-' else -1
    move_count = int(move_count_str)
    halfmove_count = int(halfmove_count_str)
    return board_piece_input, is_white, move_count, halfmove_count, \
           castling_rights, en_passent_target


class Piece:
    def __init__(self, board, rect, glyph) -> None:
        self.board = board
        self.rect = rect
        self.glyph = glyph
        self.square = board.game.get_square_index(*rect[:2])
        self.previous_center = self.rect.center
        self.click = False
        self.image = pg.transform.scale(get_piece_img(glyph), (board.game.square_size,
                                                               board.game.square_size))
        self.is_white = glyph.isupper()

    def update(self) -> None:
        if self.click:
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
        x //= self.board.game.square_size
        y //= self.board.game.square_size
        return (y * 8) + x

    def move_to(self, new_square:int) -> None:
        # with new index as key, set value to self
        # then take original location in map and delete
        # set self.square to new location
        cur_board = self.board
        old_square = self.square
        move = (old_square, new_square)

        print(move)

        cur_board.piece_map[new_square] = self
        del cur_board.piece_map[old_square]
        
        cur_board.piece_map[new_square].rect.topleft = cur_board.game.get_cords_from_index(new_square) 

        self.square = self.get_square_index()

    def get_valid_moves(self) -> list[Move]:
        print("ERROR: This piece has not been classified past being a piece")
        return [(self.square, self.square)]


    def snap_to_square(self) -> None:
        if self.board.game.mouse_inside_bounds():
            player_cords = (self.rect.center[0], self.rect.center[1])
            self.rect.topleft = get_snap_cords(*player_cords, self.board.game.square_size)


class Bishop(Piece):
    def __init__(self, board, rect, glyph) -> None:
        Piece.__init__(self, board, rect, glyph)


    def get_valid_moves(self) -> list[Move]:
        OFFSETS = ((-1, -1) ,(-1, 1), (1, 1), (1, -1))
        valid_moves = []
        for offset in OFFSETS:
            valid_moves += self.board.get_sliding_moves(self.square, offset)
        return valid_moves

class Rook(Piece):
    def __init__(self, board, rect, glyph) -> None:
        Piece.__init__(self, board, rect, glyph)


    def get_valid_moves(self) -> list[Move]:
        OFFSETS = ((1, 0) ,(-1, 0), (0, 1), (0, -1))
        valid_moves = []
        for offset in OFFSETS:
            valid_moves += self.board.get_sliding_moves(self.square, offset)
        return valid_moves


class Queen(Piece):
    def __init__(self, board, rect, glyph) -> None:
        Piece.__init__(self, board, rect, glyph)

    def get_valid_moves(self) -> list[Move]:
        OFFSETS = ((-1, -1) ,(-1, 1), (1, 1), (1, -1), (1, 0) ,(-1, 0), (0, 1), (0, -1))
        valid_moves = []
        for offset in OFFSETS:
            valid_moves += self.board.get_sliding_moves(self.square, offset)
        return valid_moves

class Knight(Piece):
    def __init__(self, board, rect, glyph) -> None:
        Piece.__init__(self, board, rect, glyph)

    def get_valid_moves(self) -> list[Move]:
        OFFSETS = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), \
                    (1, -2), (1, 2), (2, -1), (2, 1))
        valid_moves =  self.board.get_jumping_moves(self.square, OFFSETS)
        return valid_moves

class King(Piece):
    def __init__(self, board, rect, glyph) -> None:
        Piece.__init__(self, board, rect, glyph)

    def get_valid_moves(self) -> list[Move]:
        valid_moves = []
        OFFSETS = ((-1, -1), (-1, 0), (-1, 1), (0, -1), \
                    (0, 1), (1, -1), (1, 0), (1, 1))
        CASTLING_KINGSIDE_OFFSET = [(0, 2)]
        CASTLING_QUEENSIDE_OFFSET = [(0, -2)]
        valid_moves = self.board.get_jumping_moves(self.square, OFFSETS)

        castling_kingside_moves = self.board.get_jumping_moves(self.square, CASTLING_KINGSIDE_OFFSET)
        castling_queenside_moves = self.board.get_jumping_moves(self.square, CASTLING_QUEENSIDE_OFFSET)

        if self.square + 1 in self.board.piece_map or \
            self.square + 2 in self.board.piece_map:
            castling_kingside_moves = []
        elif self.square - 1 in self.board.piece_map or \
            self.square - 2 in self.board.piece_map or \
            self.square - 3 in self.board.piece_map:
            castling_queenside_moves = []

        c_r_to_check = ['K', 'Q'] if self.board.is_white_turn else ['k', 'q']
        for castling_right in c_r_to_check:
            if self.board.castling_rights[castling_right]:
                if castling_right.lower() == 'k':
                    valid_moves += castling_kingside_moves
                elif castling_right.lower() == 'q':
                    valid_moves += castling_queenside_moves

        return valid_moves

class Pawn(Piece):
    def __init__(self, board, rect, glyph) -> None:
        Piece.__init__(self, board, rect, glyph)

    def promote(self) -> None:
        has_valid_glyph = False
        while not has_valid_glyph:
            glyph = input("enter a valid glyph")
            has_valid_glyph = True
            glyph = glyph.upper() if self.is_white else glyph.lower()
            match glyph:
                case 'q' | 'Q':
                    self.board.piece_map[self.square] = Queen(self.board, self.rect, glyph)
                case 'n' | 'N':
                    self.board.piece_map[self.square] = Knight(self.board, self.rect, glyph)
                case 'r' | 'R':
                    self.board.piece_map[self.square] = Rook(self.board, self.rect, glyph)
                case 'b' | 'B':
                    self.board.piece_map[self.square] = Bishop(self.board, self.rect, glyph)
                case _:
                    print('Invalid Glyph')
                    has_valid_glyph = False
        print(f"after promotion: {self}")


    def get_valid_moves(self) -> list[Move]:
        valid_moves = []
        direction = -1 if self.is_white else 1
        move_offsets = [(1*direction, 0)]

        if (self.is_white and divmod(self.square, 8)[DIVMOD_ROW] == 6):
            move_offsets.append((-2, 0))
        elif (not self.is_white and divmod(self.square, 8)[DIVMOD_ROW] == 1):
            move_offsets.append((2, 0))

        take_offsets = ((1*direction, 1), (1*direction, -1))

        for take_offset in take_offsets:
            if will_move_out(self.square, take_offset): continue
            new_sqr = get_square_after_move(self.square, take_offset)
            if (new_sqr in self.board.piece_map.keys() and
                not self.board.piece_map[new_sqr].is_same_colour(self)) or \
                new_sqr == self.board.en_passent_target:
                # is different colour or en passent taget is there
                valid_moves.append((self.square, new_sqr))

        for move_offset in move_offsets:
            if will_move_out(self.square, move_offset): continue
            new_sqr = get_square_after_move(self.square, move_offset)
            if new_sqr not in self.board.piece_map.keys():
                # no piece at new square
                valid_moves.append((self.square, new_sqr))
        return valid_moves

class Board:
    def __init__(self, game, piece_positions:list[PiecePositionInput],
                is_white_turn:bool, move_count:int, halfmove_count:int,
                castling_rights:dict[str, bool], en_passent_target:int) -> None:
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
                case 'q' | 'Q':
                    self.piece_map[square] = Queen(self, rect, glyph)
                case 'p' | 'P':
                    self.piece_map[square] = Pawn(self, rect, glyph)
                case 'k' | 'K':
                    self.piece_map[square] = King(self, rect, glyph)
                case 'n' | 'N':
                    self.piece_map[square] = Knight(self, rect, glyph)
                case _:
                    self.piece_map[square] = Piece(self, rect, glyph)
        self.is_white_turn = is_white_turn
        self.move_count = move_count
        self.halfmove_count = halfmove_count
        self.castling_rights = castling_rights
        self.en_passent_target = en_passent_target
        self.legal_moves_map = {}

    def print(self) -> None:
        for square_index in range(64):
            try:
                glyph = self.piece_map[square_index].glyph
            except KeyError:
                glyph = '-'
            # hacky workaround pythons f-str
            nl = "\n"
            print(f"{glyph}{nl if (square_index+1)%8 == 0 else ' '}", end='')

    def does_move_create_check(self, is_king_white:bool, move:Move) -> bool:
        return False
        piece = self.piece_map[move[MOVE_START]]
        print(f"does_move... piece: {piece}")
        board_after = self.get_board_after_move(piece, *move)
        return board_after.is_in_check(is_king_white)

    def is_in_check(self, is_king_white:bool) -> bool:
        glyph_to_find = 'K' if is_king_white else 'k'
        king_square = [piece for piece in self.get_pieces() if piece.glyph == glyph_to_find][0].square
        return king_square in [move[MOVE_END] for move in self.get_all_valid_moves()]

    def get_all_valid_moves(self) -> list[Move]:
        valid_moves = []
        for piece in self.get_pieces():
            valid_moves += piece.get_valid_moves()
        return valid_moves

    def eval_move(self, piece, new_square) -> int:
        # if valid location and is legal move()
        move = (piece.square, new_square)
        is_in_board = self.game.mouse_inside_bounds()

        if is_in_board:
            if self.is_move_castling(move):
                if self.is_castle_kingside(move):
                    return MoveEvalResponces.CASTLE_KINGSIDE
                else:
                    return MoveEvalResponces.CASTLE_QUEENSIDE
            elif self.is_move_en_passent(move): return MoveEvalResponces.EN_PASSENT
            elif self.is_move_double_push(move): return MoveEvalResponces.DOUBLE_PUSH
            elif self.is_move_promotion(move): return MoveEvalResponces.PROMOTION

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

    def piece_map_to_board_input(self, piece_map:dict[int, 'Piece']) -> PiecePositionInput:
        pieces = piece_map.values()
        return [(*piece.rect[:3], piece.glyph) for piece in pieces]

    def is_move_promotion(self, move:Move) -> bool:
        if type(self.piece_map[move[0]]) == Pawn:
            end_row = 0 if self.piece_map[move[0]].is_white else 7
            move_to_row = divmod(move[1], 8)[0]
            return move_to_row == end_row
        return False

    def is_move_double_push(self, move:Move):
        if type(self.piece_map[move[0]]) == Pawn:
            if abs(move[0] - move[1]) == 16:
                print("double push")
                return True
        return False

    def is_move_en_passent(self, move:Move):
        piece = self.piece_map[move[0]]
        if type(piece) == Pawn:
            if (piece.is_white and piece.square < 32) or \
                (not piece.is_white and piece.square >= 32):
                    print(move[1], self.en_passent_target)
                    if move[1] == self.en_passent_target:
                        print("en passent")
                        return True
        return False

    def is_move_castling(self, move:Move):
        if type(self.piece_map[move[0]]) == King:
            if abs(move[0] - move[1]) == 2:
                print("castling")
                return True
        return False

    def is_castle_kingside(self, move:Move) -> bool:
        """
        Precondition: move must be a castle for function to be accurate
        """
        start, end = move
        diff = end - start
        return diff == 2

    def update_castling_rights(self, start_square, end_square) -> None:
        if self.is_move_castling((start_square, end_square)):
            # remove one colours castling rights
            castling_rights_to_change = ['k', 'q']

            for cr_to_chg in castling_rights_to_change:
                if self.is_white_turn: cr_to_chg = cr_to_chg.upper()
                self.castling_rights[cr_to_chg] = False

        elif type(self.piece_map[start_square]) == Rook:
            match start_square:
                case 0: self.castling_rights['q'] = False
                case 7: self.castling_rights['k'] = False
                case 56: self.castling_rights['Q'] = False
                case 63: self.castling_rights['K'] = False

        elif type(self.piece_map[start_square]) == King:
            if self.piece_map[start_square].is_white:
                self.castling_rights['K'] = False
                self.castling_rights['Q'] = False
            else:
                self.castling_rights['k'] = False
                self.castling_rights['q'] = False

        match end_square:
            case 0: self.castling_rights['q'] = False
            case 7: self.castling_rights['k'] = False
            case 56: self.castling_rights['Q'] = False
            case 63: self.castling_rights['K'] = False


    def get_board_after_halfmove(self, move:Move) -> 'Board':
        start_square, end_square = move
        if type(self.piece_map[start_square]) == Pawn:
            new_halfmove_count = 0
        else:
            new_halfmove_count = self.halfmove_count + 1

        new_piece_map = self.piece_map

        self.update_castling_rights(*move)

        new_move_count = self.move_count + 1 if self.is_white_turn else self.move_count

        new_en_passent_target = self.en_passent_target

        new_piece_map[start_square].move_to(end_square)
        piece_map_board_input = self.piece_map_to_board_input(new_piece_map)

        if (-1 < self.en_passent_target < 32 and self.is_white_turn) or \
                (self.en_passent_target >= 32 and not self.is_white_turn):
            new_en_passent_target = -1
     
        return Board(self.game, piece_map_board_input, 
                     self.switch_is_white_turn(), new_move_count,
                     new_halfmove_count, self.castling_rights, 
                     new_en_passent_target)

    def get_board_after_capture(self, move:Move) -> 'Board':
        start_square, end_square = move
        new_halfmove_count = 0
        new_piece_map = self.piece_map

        self.update_castling_rights(*move)

        new_move_count = self.move_count + 1 if self.is_white_turn else self.move_count

        new_en_passent_target = self.en_passent_target

        new_piece_map[start_square].move_to(end_square)
        piece_map_board_input = self.piece_map_to_board_input(new_piece_map)

        if (-1 < self.en_passent_target < 32 and self.is_white_turn) or \
        (self.en_passent_target >= 32 and not self.is_white_turn):
            new_en_passent_target = -1

        return Board(self.game, piece_map_board_input,
                     self.switch_is_white_turn(), new_move_count,
                     new_halfmove_count, self.castling_rights,
                     new_en_passent_target)

    def get_board_after_castle_kingside(self, move:Move) -> 'Board':
        start_square, end_square = move
        new_piece_map = self.piece_map

        self.update_castling_rights(*move)

        new_move_count = self.move_count + 1 if self.is_white_turn else self.move_count
        new_halfmove_count = self.halfmove_count + 1

        new_en_passent_target = self.en_passent_target
        
        rook_start_sqr = end_square + 1
        rook_end_sqr = end_square - 1
        
        new_piece_map[rook_start_sqr].move_to(rook_end_sqr)
        new_piece_map[start_square].move_to(end_square)

        piece_map_board_input = self.piece_map_to_board_input(new_piece_map)

        if (-1 < self.en_passent_target < 32 and self.is_white_turn) or \
        (self.en_passent_target >= 32 and not self.is_white_turn):
            new_en_passent_target = -1

        return Board(self.game, piece_map_board_input,
                     self.switch_is_white_turn(), new_move_count,
                     new_halfmove_count, self.castling_rights,
                     new_en_passent_target)


    def get_board_after_castle_queenside(self, move:Move) -> 'Board':
        start_square, end_square = move
        new_piece_map = self.piece_map

        self.update_castling_rights(*move)

        new_move_count = self.move_count + 1 if self.is_white_turn else self.move_count
        new_halfmove_count = self.halfmove_count + 1

        new_en_passent_target = self.en_passent_target
        
        rook_start_sqr = end_square - 2 
        rook_end_sqr = end_square + 1
    
        new_piece_map[start_square].move_to(end_square)
        new_piece_map[rook_start_sqr].move_to(rook_end_sqr)

        piece_map_board_input = self.piece_map_to_board_input(new_piece_map)

        if (-1 < self.en_passent_target < 32 and self.is_white_turn) or \
        (self.en_passent_target >= 32 and not self.is_white_turn):
            new_en_passent_target = -1

        return Board(self.game, piece_map_board_input,
                     self.switch_is_white_turn(), new_move_count,
                     new_halfmove_count, self.castling_rights,
                     new_en_passent_target)


    def get_board_after_en_passent(self, move:Move) -> 'Board':
        start_square, end_square = move
        new_piece_map = self.piece_map

        self.update_castling_rights(*move)

        new_move_count = self.move_count + 1 if self.is_white_turn else self.move_count
        new_halfmove_count = 0

        new_en_passent_target = self.en_passent_target
        
        direction = -1 if self.is_white_turn else 1
        square_to_del = end_square + (8 * -direction)
        
        new_piece_map[start_square].move_to(end_square)
        del new_piece_map[square_to_del]

        piece_map_board_input = self.piece_map_to_board_input(new_piece_map)
        
        new_en_passent_target = -1
        
        return Board(self.game, piece_map_board_input,
                     self.switch_is_white_turn(), new_move_count,
                     new_halfmove_count, self.castling_rights,
                     new_en_passent_target)

    def get_board_after_double_push(self, move:Move) -> 'Board':
        start_square, end_square = move
        new_piece_map = self.piece_map
        new_en_passent_target = sum(move) // 2 

        self.update_castling_rights(*move)

        new_move_count = self.move_count + 1 if self.is_white_turn else self.move_count
        new_halfmove_count = 0
            
        new_piece_map[start_square].move_to(end_square)

        piece_map_board_input = self.piece_map_to_board_input(new_piece_map)

        return Board(self.game, piece_map_board_input,
                     self.switch_is_white_turn(), new_move_count,
                     new_halfmove_count, self.castling_rights,
                     new_en_passent_target)

    def get_board_after_promotion(self, move:Move) -> 'Board':
        start_square, end_square = move
        new_piece_map = self.piece_map 

        self.update_castling_rights(*move)

        new_move_count = self.move_count + 1 if self.is_white_turn else self.move_count
        new_halfmove_count = 0
        
        new_en_passent_target = self.en_passent_target

        new_piece_map[start_square].move_to(end_square) 
        new_piece_map[end_square].promote()

        piece_map_board_input = self.piece_map_to_board_input(new_piece_map)

        if (-1 < self.en_passent_target < 32 and self.is_white_turn) or \
        (self.en_passent_target >= 32 and not self.is_white_turn):
            new_en_passent_target = -1

        return Board(self.game, piece_map_board_input,
                     self.switch_is_white_turn(), new_move_count,
                     new_halfmove_count, self.castling_rights,
                     new_en_passent_target)

    def get_board_after_move(self, piece:Piece, start_square:int, end_square:int) -> 'Board':
        piece = self.piece_map[start_square]
        move_evalutation = self.eval_move(piece, end_square)
        print(f"move_eval: {move_evalutation}")
        match move_evalutation:
            case MoveEvalResponces.INVALID_MOVE:
                piece.return_to_previous()
                new_board = -1

            case MoveEvalResponces.MOVE_TO_EMPTY:
                new_board = self.get_board_after_halfmove((start_square,
                                                              end_square))

            case MoveEvalResponces.CAPTURE_MOVE:
                if type(self.piece_map[end_square]) == King: self.game.is_game_over = True
                new_board = self.get_board_after_capture((start_square,
                                                          end_square))

            case MoveEvalResponces.CASTLE_KINGSIDE:
                new_board = self.get_board_after_castle_kingside((start_square,
                                                                   end_square))
            
            case MoveEvalResponces.CASTLE_QUEENSIDE:
                new_board = self.get_board_after_castle_queenside((start_square,
                                                               end_square))

            case MoveEvalResponces.EN_PASSENT:
                new_board = self.get_board_after_en_passent((start_square,
                                                               end_square))

            case MoveEvalResponces.DOUBLE_PUSH:
                new_board = self.get_board_after_double_push((start_square,
                                                               end_square))

            case MoveEvalResponces.PROMOTION:
                new_board = self.get_board_after_promotion((start_square,
                                                             end_square))
            case _:
                print('error with eval move')
        return new_board

    def get_clicked_piece(self) -> Piece:
        for piece in self.piece_map.values():
            if piece.click: return piece
        return -1

    def get_jumping_moves(self, start_square, offsets:list[tuple[int, int]]) -> list[Move]:
        valid_moves = []
        for offset in offsets:
            if not will_move_out(start_square, offset):
                new_square = get_square_after_move(start_square, offset)
                if new_square in self.piece_map.keys():
                    if not self.piece_map[new_square].is_same_colour(self.piece_map[start_square]):
                        # not same colour
                        valid_moves.append((start_square, new_square))
                else:
                    # empty square
                    valid_moves.append((start_square, new_square))
        return valid_moves



    def get_sliding_moves(self, start_square, offset:tuple[int, int], max_depth=8) -> list[Move]:
        depth = 1
        valid_moves = []
        while not will_move_out(start_square, multiply_in_tuple(offset, depth)) and depth<=max_depth:
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

        has_any_castle_right = len([active_cr for active_cr in self.castling_rights.values() if active_cr])>0
        for castle_right in self.castling_rights.keys():
            if self.castling_rights[castle_right]:
                fen += castle_right
        if not has_any_castle_right: fen += '-'
        fen+=' '

        fen += '- ' if self.en_passent_target == -1 else str(self.en_passent_target) + ' '

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

        self.square_size = 100
        self.top_left = 100
        self.bottom_right = self.top_left + (8 * self.square_size)
        SCREEN_WIDTH = 1000
        SCREEN_HEIGHT = 1000

        square_cords_gen  = range(self.top_left, self.bottom_right, self.square_size)
        self.square_cords = [[i, j] \
            for i in square_cords_gen \
            for j in square_cords_gen]
        self.surface = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.boards = [Board(self, *fen_to_board_input(starting_fen, self))]
        min_to_sec = lambda m : m * 60
        self.white_time = min_to_sec(5)
        self.black_time = min_to_sec(5)
        self.is_game_over = False
        self.display_blue = False
        """
        Note:
        Used to have is_white_turn and move_count in this init but because
        they WERE only used to create the board, it makes WAYYYY more sense to
        have a function that turns the fen string into everything EXCEPT the
        game being passed in
        """

    def toggle_blue(self) -> None:
        self.display_blue = ~self.display_blue

    def is_inside_bounds(self, x, y) -> bool:
        return (x >= self.top_left and x <= self.bottom_right and
                y >= self.top_left and y <= self.bottom_right)

    def mouse_inside_bounds(self) -> bool:
        return self.is_inside_bounds(*pg.mouse.get_pos())

    def relative_board_cords(self, x, y) -> Cord:
        return (x-self.top_left, y-self.top_left)

    def get_square_index(self, x, y) -> int:
        """
        Precondition: x, y point must be inside board already
        """
        x, y = self.relative_board_cords(x, y)
        x //= self.square_size
        y //= self.square_size
        return (y * 8) + x

    def get_cords_from_index(self, index:int) -> Cord:
        y, x  = divmod(index, 8)
        x *= self.square_size
        y *= self.square_size
        return x + 100, y + 100

    def get_current_board(self) -> 'Board':
        return self.boards[-1]

    def add_board(self, board) -> None:
        self.boards.append(board)

    def display_grid(self) -> None:
        for x, y in self.square_cords:
            row = x / 100
            column = y / 100
            rect = pg.Rect([x, y, 100, 100])
            image = pg.Surface(rect.size).convert()
            if not (is_odd(row) ^ is_odd(column)):
                black_square(self.surface, image, rect)
            else:
                white_square(self.surface, image, rect)
            
            square_num = game.get_square_index(x, y)
            font = pg.font.Font(None, 32)
            font_color = (0, 0, 0)
            square_num_rect = pg.Rect(x+10, y, 10, 10)
            algebraic_rect = pg.Rect(x+65, y, 10, 10)
            txt_square_i = font.render(str(square_num), True, font_color)
            txt_algebraic = font.render(str(square_index_to_algebraic(square_num)), True, font_color)
            self.surface.blit(txt_square_i, square_num_rect)
            #self.surface.blit(txt_algebraic, algebraic_rect)

    def clear_surface(self) -> None:
        self.surface.fill(0)

    def display_blue_squares(self) -> None:
        piece = self.get_current_board().get_clicked_piece()
        if piece == -1: return
        legal_squares = [move[1] for move in piece.get_valid_moves()]
        piece.board.legal_moves_map[piece.square] = legal_squares
        make_squares_blue(self.surface, self.square_size, legal_squares)

    def update_game(self) -> None:
        self.clear_surface()
        self.display_grid()
        if self.display_blue: self.display_blue_squares()
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
    return fen

test_fen_strings = [
STARTING_FEN,
'8/8/8/8/8/8/8/8 w - - 0 1',
'8/6p1/5P2/4p3/3P4/2p5/1P6/8 w - - 0 1',
'k7/8/8/3bQ3/3nR3/8/8/8 b KQkq - 0 1',
get_random_fen(),
'8/3pp3/8/8/8/8/3PP3/8 b - - 0 1',
'r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1',
'8/3P4/8/8/8/8/4p3/8 w - - 0 1',
'8/4k3/4r3/8/8/3R4/3K4/8 w - - 0 1'
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

fen_prompt = """
    choose a fen string,
    0 is standard staring fen string,
    1 is an empty board,
    2 will help test pawn movement,
    3 will test most other pieces,
    4 is a random fen string,
    5 is a en passent test,
    6 to test castling,
    7 to test promotion,
    8 for testing *legal* moves
"""

if __name__ == "__main__":
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pg.init()
    fen = test_fen_strings[int(input(fen_prompt))]
    print(fen)
    game = Game(fen)
    MyClock = pg.time.Clock()
    while not game.is_game_over:
        main(game)
        pg.display.update()
        MyClock.tick(60)
