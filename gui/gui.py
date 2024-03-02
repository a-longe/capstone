#!/bin/python3

from copy import deepcopy
import math
import os
from random import randint
import sys
import time

import pygame as pg

import engine_handler as engine

STOCKFISH_PATH = (
    "/home/alonge/Documents/stockfish/stockfish/stockfish-ubuntu-x86-64-avx2"
)

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 1080

TAKEN_PIECE_DISPLAY_INIT_X_OFFSET = 150
TAKEN_PIECE_DISPLAY_W_Y_OFFSET = 200
TAKEN_PIECE_DISPLAY_B_Y_OFFSET = 400
TAKEN_PIECE_DISPLAY_IMG_SIZE = 20
TAKEN_PIECE_DISPLAY_OFFSET_BETWEEN_PIECES = 20

TIMER_WIDTH = 200
TIMER_HEIGHT = 100
TIMER_FONT_COLOR = (255, 255, 255)
TIMER_FONT_SIZE = 100
TIMER_X_OFFSET = 150
TIMER_W_Y_OFFSET = 500
TIMER_B_Y_OFFSET = 100

PiecePositionInput = tuple[int, int, int, str]
PIECE_X = 0
PIECE_Y = 1
PIECE_SIZE = 2  # do not need width and height as pieces are square images
PIECE_GLYPH = 3

DIVMOD_ROW = 0
DIVMOD_COLUMN = 1

WHITE_PROMOTION_PIECES = ["Q", "N", "R", "B"]
BLACK_PROMOTION_PIECES = [piece.lower() for piece in WHITE_PROMOTION_PIECES]

BoardFenInput = tuple[list[PiecePositionInput], bool, int, int, dict[str, bool], int]

STARTING_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

Move = tuple[int, int, str]
MOVE_START = 0
MOVE_END = 1
MOVE_PROMOTION = 2

Cord = tuple[int, int]
CORD_X = 0
CORD_Y = 1

IMAGE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")

INT_TO_LETTER = {
    0: "a",
    1: "b",
    2: "c",
    3: "d",
    4: "e",
    5: "f",
    6: "g",
    7: "h",
}


class MoveEvalResponces:
    INVALID_MOVE = -1
    MOVE_TO_EMPTY = 1
    CAPTURE_MOVE = 2
    CASTLE_KINGSIDE = 3
    CASTLE_QUEENSIDE = 4
    EN_PASSENT = 5
    DOUBLE_PUSH = 6
    PROMOTION = 7


def add_tuples(t1: tuple, t2: tuple) -> tuple[int, int]:
    """Precondition: tuples must both be len(2)"""
    return (t1[0] + t2[0], t1[1] + t2[1])


def my_divmod(num, divisor) -> tuple[int, int]:
    if num < 0:
        is_neg = -1
    else:
        is_neg = 1

    num = abs(num)
    return is_neg * (num // divisor), is_neg * (num % divisor)


def is_odd(num) -> bool:
    return bool(num % 2)


def black_square(surface, image, rect):
    image.fill((187, 190, 100))
    surface.blit(image, rect)


def white_square(surface, image, rect):
    image.fill((234, 240, 206))
    surface.blit(image, rect)


def blue_square(surface, image, rect):
    image.fill((100, 100, 250))
    surface.blit(image, rect)


def make_squares_blue(game, surface, square_size, squares: list[int]) -> None:
    for square in squares:
        x, y = game.get_cords_from_index(square)
        rect = pg.Rect([x, y, square_size, square_size])
        image = pg.Surface(rect.size).convert()
        blue_square(surface, image, rect)


def square_index_to_algebraic(square_index: int) -> str:
    row, column = divmod(square_index, 8)
    return INT_TO_LETTER[column] + str(8 - (row))


def algebraic_to_square(square: str) -> int:
    column_str, row = square[0], int(square[1])
    column = {v: k for k, v in INT_TO_LETTER.items()}[column_str]
    return (8 - row) * 8 + column


def multiply_in_tuple(t1: tuple[int, int], multiplier: int) -> tuple[int, int]:
    return (t1[0] * multiplier, t1[1] * multiplier)


def will_move_out(starting_square: int, offset_r_c: tuple[int, int]) -> bool:
    square_r_c = my_divmod(starting_square, 8)
    new_square_r_c = add_tuples(square_r_c, offset_r_c)
    will_go_out = not is_possible_square_r_c(new_square_r_c)
    return will_go_out


def is_possible_square_r_c(square: tuple[int, int]) -> bool:
    return (0 <= square[0] <= 7) and (0 <= square[1] <= 7)


def r_c_to_int(square: tuple[int, int]) -> int:
    return square[0] * 8 + square[1]


def get_square_after_move(start: int, offset_r_c: tuple[int, int]) -> int:
    start_r_c = my_divmod(start, 8)
    new_square_r_c = add_tuples(start_r_c, offset_r_c)
    return r_c_to_int(new_square_r_c)


def get_snap_cords(x, y, square_size) -> Cord:
    return (
        math.floor(x / square_size) * square_size,
        math.floor(y / square_size) * square_size,
    )


def get_piece_img(glyph: str) -> pg.Surface:
    if glyph.isupper():
        color = "w"
    else:
        color = "b"
    piece_type = glyph.upper()
    return pg.image.load(os.path.join(IMAGE_DIR, f"{color}{piece_type}.png"))


def on_mouse_down(game):
    if game.is_white_promoting or game.is_black_promoting:
        return
    for piece in game.get_current_board().get_pieces():
        # The event positions is the mouse coordinates
        if piece.rect.collidepoint(pg.mouse.get_pos()) and piece.can_pickup():
            valid_targets = [move[MOVE_END] for move in piece.get_valid_moves()]
            print(piece, valid_targets)
            # store current center
            piece.previous_center = piece.rect.center
            piece.click = True


def on_mouse_up(game) -> None:
    cur_board = game.get_current_board()
    if game.is_promoting():
        print(pg.mouse.get_pos())
        selected_promotion = game.get_selected_promotion_option()
        if selected_promotion != "":
            game.is_black_promoting = False
            game.is_white_promoting = False
            move = *game.attempted_promotion[:MOVE_PROMOTION], selected_promotion
            piece = cur_board.piece_map[move[MOVE_START]]
            print(move)
            new_board = cur_board.get_board_after_move(piece, move)
            print("new board in promotion branch", new_board)
        else:
            return
    else:
        piece = cur_board.get_clicked_piece()
        if piece == -1:
            return
        start_square = piece.square
        end_square = game.get_square_index(*pg.mouse.get_pos())
        move = (start_square, end_square, "")
        if start_square == end_square:
            piece.snap_to_square()
            piece.click = False
            return

        if move[:2] not in [move[:2] for move in cur_board.get_all_valid_moves()] or \
                start_square == end_square:
            piece.return_to_previous()
            piece.click = False
            return

        new_board = cur_board.get_board_after_move(piece, move)

        print(new_board, piece, move)

        if new_board.is_in_check(not new_board.is_white_turn):
            print("not a legal move")
            # when calling is_in_check piece is move for some reason, atm
            # fix by moveing it back but will fix it better later
            # NOTE: the more i look at this the more i want to throw up
            # cur_board.move(end_square, start_square)
            piece.click = False
            piece.return_to_previous()
            return

        if end_square in cur_board.piece_map:
            taken_piece = cur_board.piece_map[end_square]
            if taken_piece.is_white:
                game.white_taken_pieces.append(taken_piece.glyph)
            else:
                game.black_taken_pieces.append(taken_piece.glyph)

        elif cur_board.is_move_en_passent(move):
            if cur_board.is_white_turn:
                game.black_taken_pieces.append("p")
            else:
                game.white_taken_pieces.append("P")

        if cur_board.is_move_promotion((start_square, end_square, "")):
            if cur_board.is_white_turn:
                game.is_white_promoting = True
            else:
                game.is_black_promoting = True
            piece.click = False
            piece.snap_to_square()
            game.attempted_promotion = (start_square, end_square, "")
            return

        piece.snap_to_square()
        piece.click = False

    game.add_board(new_board)
    print("board: ", new_board)
    new_board.print()
    print(new_board.get_fen(), end="\n\n")
    print(f"Time Remaining - White: {game.white_time}, Black: {game.black_time}")
    print(
        f"Taken Pieces - White Pieces: {game.white_taken_pieces}, Black Pieces: {game.black_taken_pieces}"
    )


def fen_to_pieces(fen, game) -> PiecePositionInput:
    lo_pieces = []
    pieces = fen.split(" ")[0]
    rows = pieces.split("/")
    r_i = 0
    for row in rows:
        c_i = 0
        for char in row:
            if char.isdigit():
                c_i += int(char) - 1
            else:
                # convert c_i and r_i into square
                cords = (
                    c_i * game.square_size + game.top_left[0],
                    r_i * game.square_size + game.top_left[1],
                )
                lo_pieces.append((*cords, game.square_size, char))
            c_i += 1
        r_i += 1
    return lo_pieces


def fen_to_board_input(fen, game) -> BoardFenInput:
    (
        piece_str,
        active_colour_str,
        castling_rights_str,
        en_passent_str,
        move_count_str,
        halfmove_count_str,
    ) = fen.split(" ")

    board_piece_input = fen_to_pieces(fen, game)
    is_white = True if active_colour_str == "w" else False
    castling_rights = {"K": False, "Q": False, "k": False, "q": False}
    for castle_right in castling_rights_str:
        if castle_right in castling_rights.keys():
            castling_rights[castle_right] = True
    en_passent_target = int(en_passent_str) if en_passent_str != "-" else -1
    move_count = int(move_count_str)
    halfmove_count = int(halfmove_count_str)
    return (
        board_piece_input,
        is_white,
        move_count,
        halfmove_count,
        castling_rights,
        en_passent_target,
    )


class Piece:
    def __init__(self, board, rect, glyph) -> None:
        self.board = board
        self.rect = rect
        self.glyph = glyph
        self.square = board.game.get_square_index(*rect[:2])
        self.previous_center = self.rect.center
        self.click = False
        self.image = pg.transform.scale(
            get_piece_img(glyph), (board.game.square_size, board.game.square_size)
        )
        self.is_white = glyph.isupper()

    def __repr__(self) -> str:
        return f"Piece({self.glyph}, rect:{self.rect}, square:{self.square}, clicked:{self.click})"

    def update(self) -> None:
        if self.click:
            self.rect.center = pg.mouse.get_pos()
        self.board.surface.blit(self.image, self.rect)

    def return_to_previous(self) -> None:
        self.rect.center = self.previous_center

    def is_same_colour(self, piece_2: "Piece") -> bool:
        return self.is_white == piece_2.is_white

    def can_pickup(self) -> bool:
        """
        Would not be able to be picked up if piece cant help with a check, or if
        its not the active colour
        """
        return self.is_white == self.board.is_white_turn

    def get_valid_moves(self) -> list[Move]:
        print("ERROR: This piece has not been classified past being a piece")
        return [(self.square, self.square, "")]

    def snap_to_square(self) -> None:
        if self.board.game.mouse_inside_bounds():
            player_cords = (self.rect.center[0], self.rect.center[1])
            self.rect.topleft = get_snap_cords(
                *player_cords, self.board.game.square_size
            )


class Bishop(Piece):
    def __init__(self, board, rect, glyph) -> None:
        Piece.__init__(self, board, rect, glyph)

    def get_valid_moves(self) -> list[Move]:
        OFFSETS = ((-1, -1), (-1, 1), (1, 1), (1, -1))
        valid_moves = []
        for offset in OFFSETS:
            valid_moves += self.board.get_sliding_moves(self.square, offset)
        return valid_moves


class Rook(Piece):
    def __init__(self, board, rect, glyph) -> None:
        Piece.__init__(self, board, rect, glyph)

    def get_valid_moves(self) -> list[Move]:
        OFFSETS = ((1, 0), (-1, 0), (0, 1), (0, -1))
        valid_moves = []
        for offset in OFFSETS:
            valid_moves += self.board.get_sliding_moves(self.square, offset)
        return valid_moves


class Queen(Piece):
    def __init__(self, board, rect, glyph) -> None:
        Piece.__init__(self, board, rect, glyph)

    def get_valid_moves(self) -> list[Move]:
        OFFSETS = ((-1, -1), (-1, 1), (1, 1), (1, -1), (1, 0), (-1, 0), (0, 1), (0, -1))
        valid_moves = []
        for offset in OFFSETS:
            valid_moves += self.board.get_sliding_moves(self.square, offset)
        return valid_moves


class Knight(Piece):
    def __init__(self, board, rect, glyph) -> None:
        Piece.__init__(self, board, rect, glyph)

    def get_valid_moves(self) -> list[Move]:
        OFFSETS = (
            (-2, -1),
            (-2, 1),
            (-1, -2),
            (-1, 2),
            (1, -2),
            (1, 2),
            (2, -1),
            (2, 1),
        )
        valid_moves = self.board.get_jumping_moves(self.square, OFFSETS)
        return valid_moves


class King(Piece):
    def __init__(self, board, rect, glyph) -> None:
        Piece.__init__(self, board, rect, glyph)

    def get_valid_moves(self) -> list[Move]:
        valid_moves = []
        OFFSETS = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        CASTLING_KINGSIDE_OFFSET = [(0, 2)]
        CASTLING_QUEENSIDE_OFFSET = [(0, -2)]
        valid_moves = self.board.get_jumping_moves(self.square, OFFSETS)

        castling_kingside_moves = self.board.get_jumping_moves(
            self.square, CASTLING_KINGSIDE_OFFSET
        )
        castling_queenside_moves = self.board.get_jumping_moves(
            self.square, CASTLING_QUEENSIDE_OFFSET
        )

        if (
            self.square + 1 in self.board.piece_map
            or self.square + 2 in self.board.piece_map
        ):
            castling_kingside_moves = []
        elif (
            self.square - 1 in self.board.piece_map
            or self.square - 2 in self.board.piece_map
            or self.square - 3 in self.board.piece_map
        ):
            castling_queenside_moves = []

        c_r_to_check = ["K", "Q"] if self.board.is_white_turn else ["k", "q"]
        for castling_right in c_r_to_check:
            if self.board.castling_rights[castling_right]:
                if castling_right.lower() == "k":
                    valid_moves += castling_kingside_moves
                elif castling_right.lower() == "q":
                    valid_moves += castling_queenside_moves

        return valid_moves


class Pawn(Piece):
    def __init__(self, board, rect, glyph) -> None:
        Piece.__init__(self, board, rect, glyph)

    def promote(self, glyph) -> None:
        glyph = glyph.upper() if self.is_white else glyph.lower()
        match glyph:
            case "q" | "Q":
                self.board.piece_map[self.square] = Queen(self.board,
                                                          self.rect, glyph)
            case "n" | "N":
                self.board.piece_map[self.square] = Knight(self.board,
                                                           self.rect, glyph)
            case "r" | "R":
                self.board.piece_map[self.square] = Rook(self.board,
                                                         self.rect, glyph)
            case "b" | "B":
                self.board.piece_map[self.square] = Bishop(self.board,
                                                           self.rect, glyph)
            case _:
                print("Invalid Glyph:", glyph)

    def get_valid_moves(self) -> list[Move]:
        valid_moves = []
        direction = -1 if self.is_white else 1
        move_offsets = [(1 * direction, 0)]

        if self.is_white and divmod(self.square, 8)[DIVMOD_ROW] == 6:
            move_offsets.append((-2, 0))
        elif not self.is_white and divmod(self.square, 8)[DIVMOD_ROW] == 1:
            move_offsets.append((2, 0))

        take_offsets = ((1 * direction, 1), (1 * direction, -1))

        for take_offset in take_offsets:
            if will_move_out(self.square, take_offset):
                continue
            new_sqr = get_square_after_move(self.square, take_offset)
            if (
                new_sqr in self.board.piece_map.keys()
                and not self.board.piece_map[new_sqr].is_same_colour(self)
            ) or new_sqr == self.board.en_passent_target:
                # is different colour or en passent taget is there
                valid_moves.append((self.square, new_sqr, ""))

        for move_offset in move_offsets:
            if will_move_out(self.square, move_offset):
                continue
            new_sqr = get_square_after_move(self.square, move_offset)
            if new_sqr not in self.board.piece_map.keys():
                # no piece at new square
                valid_moves.append((self.square, new_sqr, ""))

        # loop over each valid move and check if it is a promotion move,
        # if it is, replace it with 4 copies of itself, one for each
        # possible promotion states
        possible_glyphs = ("n", "r", "b", "q")
        valid_moves_with_promotion = []
        for valid_move in valid_moves:
            if self.board.is_move_promotion(valid_move):
                disconstructed_moves = [
                    (valid_move[MOVE_START], valid_move[MOVE_END], possible_glyph)
                    for possible_glyph in possible_glyphs
                ]
                valid_moves_with_promotion += disconstructed_moves
            else:
                valid_moves_with_promotion.append(valid_move)
        return valid_moves_with_promotion


class Board:
    def __init__(
        self,
        game,
        piece_positions: list[PiecePositionInput],
        is_white_turn: bool,
        move_count: int,
        halfmove_count: int,
        castling_rights: dict[str, bool],
        en_passent_target: int,
    ) -> None:
        self.surface = game.surface  # passed by reference
        self.game = game
        self.piece_map = {}
        for piece_data in piece_positions:
            rect = pg.Rect(
                piece_data[PIECE_X],
                piece_data[PIECE_Y],
                piece_data[PIECE_SIZE],
                piece_data[PIECE_SIZE],
            )
            square = self.game.get_square_index(*rect[:2])
            glyph = piece_data[PIECE_GLYPH]
            match glyph:
                case "b" | "B":
                    self.piece_map[square] = Bishop(self, rect, glyph)
                case "r" | "R":
                    self.piece_map[square] = Rook(self, rect, glyph)
                case "q" | "Q":
                    self.piece_map[square] = Queen(self, rect, glyph)
                case "p" | "P":
                    self.piece_map[square] = Pawn(self, rect, glyph)
                case "k" | "K":
                    self.piece_map[square] = King(self, rect, glyph)
                case "n" | "N":
                    self.piece_map[square] = Knight(self, rect, glyph)
                case _:
                    self.piece_map[square] = Piece(self, rect, glyph)
        self.is_white_turn = is_white_turn
        self.move_count = move_count
        self.halfmove_count = halfmove_count
        self.castling_rights = castling_rights
        self.en_passent_target = en_passent_target
        self.legal_moves_map = {}

    def move(self, start_square: int, end_square: int) -> None:
        # with new index as key, set value to self
        # then take original location in map and delete
        # set self.square to new location
        move = (start_square, end_square)
        if start_square not in self.piece_map:
            self.print()

        piece = self.piece_map[start_square]

        self.piece_map[end_square] = piece
        del self.piece_map[start_square]

        self.piece_map[end_square].rect.topleft = self.game.get_cords_from_index(
            end_square
        )

        self.piece_map[end_square].square = self.game.get_square_index(*piece.rect[:2])

    def print(self) -> None:
        for square_index in range(64):
            try:
                glyph = self.piece_map[square_index].glyph
            except KeyError:
                glyph = "-"
            # hacky workaround pythons f-str
            nl = "\n"
            print(f"{glyph}{nl if (square_index+1)%8 == 0 else ' '}", end="")

    def is_in_check(self, is_check_on_white: bool) -> bool:
        glyph_to_find = "K" if is_check_on_white else "k"
        possible_king_squares = [
            piece for piece in self.get_pieces() if piece.glyph == glyph_to_find
        ]
        if len(possible_king_squares) != 0:
            king_square = possible_king_squares[0].square
        else:
            # no king on board
            return False
        valid_targets = [move[1] for move in self.get_all_valid_moves()]
        return king_square in valid_targets

    def get_all_valid_moves(self) -> list[Move]:
        valid_moves = []
        for piece in self.get_pieces():
            valid_moves += piece.get_valid_moves()
        return valid_moves

    def eval_move(self, piece: "Piece", new_square: int) -> int:
        """
        Fix function to make it cleaner, one flow of execution, one return statement
        match case?
        """
        move = (piece.square, new_square, "")
        is_same_square = piece.square == new_square
        is_in_valid_moves = move[MOVE_END] in [
            move[MOVE_END] for move in piece.get_valid_moves()
        ]
        is_valid = not is_same_square and is_in_valid_moves
        if not is_valid:
            print(move)
            return MoveEvalResponces.INVALID_MOVE

        if self.is_move_en_passent(move):
            return MoveEvalResponces.EN_PASSENT
        elif self.is_move_double_push(move):
            return MoveEvalResponces.DOUBLE_PUSH
        elif self.is_move_promotion(move):
            return MoveEvalResponces.PROMOTION
        elif self.is_move_castling(move):
            if self.is_castle_kingside(move):
                return MoveEvalResponces.CASTLE_KINGSIDE
            else:
                return MoveEvalResponces.CASTLE_QUEENSIDE

        if new_square in self.piece_map.keys():
            piece_to_take = game.get_current_board().piece_map[new_square]
            if not piece.is_same_colour(piece_to_take):
                return MoveEvalResponces.CAPTURE_MOVE
        else:
            return MoveEvalResponces.MOVE_TO_EMPTY
        print("error with eval_move, should never reach this case")
        return MoveEvalResponces.INVALID_MOVE

    def piece_map_to_board_input(
        self, piece_map: dict[int, "Piece"]
    ) -> list[PiecePositionInput]:
        pieces = piece_map.values()
        rect_size = self.game.square_size
        piece_pos_input = []
        for piece in pieces:
            abs_cords = self.game.get_cords_from_index(piece.square)
            piece_pos_input.append((*abs_cords, rect_size, piece.glyph))
        return piece_pos_input

    def is_move_promotion(self, move: Move) -> bool:
        if type(self.piece_map[move[MOVE_START]]) is Pawn:
            end_row = 0 if self.piece_map[move[MOVE_START]].is_white else 7
            move_to_row = divmod(move[MOVE_END], 8)[MOVE_START]
            return move_to_row == end_row
        return False

    def is_move_double_push(self, move: Move):
        if type(self.piece_map[move[MOVE_START]]) is Pawn:
            if abs(move[MOVE_START] - move[MOVE_END]) == 16:
                return True
        return False

    def is_move_en_passent(self, move: Move):
        piece = self.piece_map[move[MOVE_START]]
        if type(piece) is Pawn:
            if (piece.is_white and piece.square < 32) or (
                not piece.is_white and piece.square >= 32
            ):
                if move[MOVE_END] == self.en_passent_target:
                    return True
        return False

    def is_move_castling(self, move: Move):
        if type(self.piece_map[move[MOVE_START]]) is King:
            if abs(move[MOVE_START] - move[MOVE_END]) == 2:
                return True
        return False

    def is_castle_kingside(self, move: Move) -> bool:
        """
        Precondition: move must be a castle for function to be accurate
        """
        start, end, g = move
        diff = end - start
        return diff == 2

    def update_castling_rights(self, move: Move) -> dict[str, bool]:
        start_square, end_square, promotion_glyph = move
        new_castling_rights = deepcopy(self.castling_rights)
        if self.is_move_castling((start_square, end_square)):
            # remove one colours castling rights
            castling_rights_to_change = ["k", "q"]

            for cr_to_chg in castling_rights_to_change:
                if self.is_white_turn:
                    cr_to_chg = cr_to_chg.upper()
                new_castling_rights[cr_to_chg] = False

        elif type(self.piece_map[start_square]) is Rook:
            match start_square:
                case 0:
                    new_castling_rights["q"] = False
                case 7:
                    new_castling_rights["k"] = False
                case 56:
                    new_castling_rights["Q"] = False
                case 63:
                    new_castling_rights["K"] = False

        elif type(self.piece_map[start_square]) is King:
            if self.piece_map[start_square].is_white:
                new_castling_rights["K"] = False
                new_castling_rights["Q"] = False
            else:
                new_castling_rights["k"] = False
                new_castling_rights["q"] = False

        match end_square:
            case 0:
                new_castling_rights["q"] = False
            case 7:
                new_castling_rights["k"] = False
            case 56:
                new_castling_rights["Q"] = False
            case 63:
                new_castling_rights["K"] = False

        return new_castling_rights

    def get_board_after_halfmove(self, move: Move) -> "Board":
        start_square, end_square, promotion_glyph = move
        if type(self.piece_map[start_square]) is Pawn:
            new_halfmove_count = 0
        else:
            new_halfmove_count = self.halfmove_count + 1

        piece_map_board_input = self.piece_map_to_board_input(self.piece_map)

        new_castling_rights = self.update_castling_rights(move)

        new_move_count = self.move_count + 1 if self.is_white_turn else self.move_count

        new_en_passent_target = self.en_passent_target

        if (-1 < self.en_passent_target < 32 and self.is_white_turn) or (
            self.en_passent_target >= 32 and not self.is_white_turn
        ):
            new_en_passent_target = -1

        new_board = Board(
            self.game,
            piece_map_board_input,
            self.switch_is_white_turn(),
            new_move_count,
            new_halfmove_count,
            new_castling_rights,
            new_en_passent_target,
        )

        new_board.move(start_square, end_square)
        return new_board

    def get_board_after_capture(self, move: Move) -> "Board":
        start_square, end_square, promotion_glyph = move
        new_halfmove_count = 0

        new_castling_rights = self.update_castling_rights(move)

        new_move_count = self.move_count + 1 if self.is_white_turn else self.move_count

        new_en_passent_target = self.en_passent_target

        piece_map_board_input = self.piece_map_to_board_input(self.piece_map)

        if (-1 < self.en_passent_target < 32 and self.is_white_turn) or (
            self.en_passent_target >= 32 and not self.is_white_turn
        ):
            new_en_passent_target = -1

        new_board = Board(
            self.game,
            piece_map_board_input,
            self.switch_is_white_turn(),
            new_move_count,
            new_halfmove_count,
            new_castling_rights,
            new_en_passent_target,
        )

        new_board.move(start_square, end_square)
        return new_board

    def get_board_after_castle_kingside(self, move: Move) -> "Board":
        start_square, end_square, promotion_glyph = move

        new_castling_rights = self.update_castling_rights(move)

        new_move_count = self.move_count + 1 if self.is_white_turn else self.move_count
        new_halfmove_count = self.halfmove_count + 1

        new_en_passent_target = self.en_passent_target

        rook_start_sqr = end_square + 1
        rook_end_sqr = end_square - 1

        piece_map_board_input = self.piece_map_to_board_input(self.piece_map)

        if (-1 < self.en_passent_target < 32 and self.is_white_turn) or (
            self.en_passent_target >= 32 and not self.is_white_turn
        ):
            new_en_passent_target = -1

        new_board = Board(
            self.game,
            piece_map_board_input,
            self.switch_is_white_turn(),
            new_move_count,
            new_halfmove_count,
            new_castling_rights,
            new_en_passent_target,
        )

        new_board.move(rook_start_sqr, rook_end_sqr)
        new_board.move(start_square, end_square)
        return new_board

    def get_board_after_castle_queenside(self, move: Move) -> "Board":
        start_square, end_square, promotion_glyph = move

        new_castling_rights = self.update_castling_rights(move)

        new_move_count = self.move_count + 1 if self.is_white_turn else self.move_count
        new_halfmove_count = self.halfmove_count + 1

        new_en_passent_target = self.en_passent_target

        rook_start_sqr = end_square - 2
        rook_end_sqr = end_square + 1

        piece_map_board_input = self.piece_map_to_board_input(self.piece_map)

        if (-1 < self.en_passent_target < 32 and self.is_white_turn) or (
            self.en_passent_target >= 32 and not self.is_white_turn
        ):
            new_en_passent_target = -1

        new_board = Board(
            self.game,
            piece_map_board_input,
            self.switch_is_white_turn(),
            new_move_count,
            new_halfmove_count,
            new_castling_rights,
            new_en_passent_target,
        )

        new_board.move(start_square, end_square)
        new_board.move(rook_start_sqr, rook_end_sqr)
        return new_board

    def get_board_after_en_passent(self, move: Move) -> "Board":
        start_square, end_square, promotion_glyph = move

        new_castling_rights = self.update_castling_rights(move)

        new_move_count = self.move_count + 1 if self.is_white_turn else self.move_count
        new_halfmove_count = 0

        new_en_passent_target = self.en_passent_target

        direction = -1 if self.is_white_turn else 1
        square_to_del = end_square + (8 * -direction)

        piece_map_board_input = self.piece_map_to_board_input(self.piece_map)

        new_en_passent_target = -1

        new_board = Board(
            self.game,
            piece_map_board_input,
            self.switch_is_white_turn(),
            new_move_count,
            new_halfmove_count,
            new_castling_rights,
            new_en_passent_target,
        )

        new_board.move(start_square, end_square)
        del new_board.piece_map[square_to_del]
        return new_board

    def get_board_after_double_push(self, move: Move) -> "Board":
        start_square, end_square, promotion_glyph = move
        new_en_passent_target = (move[MOVE_START] + move[MOVE_END]) // 2

        new_castling_rights = self.update_castling_rights(move)

        new_move_count = self.move_count + 1 if self.is_white_turn else self.move_count
        new_halfmove_count = 0

        piece_map_board_input = self.piece_map_to_board_input(self.piece_map)

        new_board = Board(
            self.game,
            piece_map_board_input,
            self.switch_is_white_turn(),
            new_move_count,
            new_halfmove_count,
            new_castling_rights,
            new_en_passent_target,
        )

        new_board.move(start_square, end_square)
        return new_board

    def get_board_after_promotion(self, move: Move) -> "Board":
        start_square, end_square, glyph = move

        new_castling_rights = self.update_castling_rights(move)

        new_move_count = self.move_count + 1 if self.is_white_turn else self.move_count
        new_halfmove_count = 0

        new_en_passent_target = self.en_passent_target

        piece_map_board_input = self.piece_map_to_board_input(self.piece_map)

        if (-1 < self.en_passent_target < 32 and self.is_white_turn) or (
            self.en_passent_target >= 32 and not self.is_white_turn
        ):
            new_en_passent_target = -1

        new_board = Board(
            self.game,
            piece_map_board_input,
            self.switch_is_white_turn(),
            new_move_count,
            new_halfmove_count,
            new_castling_rights,
            new_en_passent_target,
        )

        new_board.move(start_square, end_square)
        new_board.piece_map[end_square].promote(glyph)
        return new_board

    def get_board_after_move(self, piece: Piece, move: Move) -> "Board":
        start_square, end_square, promotion_glyph = move
        move_evalutation = self.eval_move(piece, end_square)
        match move_evalutation:
            case MoveEvalResponces.INVALID_MOVE:
                piece.return_to_previous()
                new_board = -1

            case MoveEvalResponces.MOVE_TO_EMPTY:
                new_board = self.get_board_after_halfmove(move)

            case MoveEvalResponces.CAPTURE_MOVE:
                # if type(self.piece_map[end_square]) == King: self.game.is_game_over = True
                new_board = self.get_board_after_capture(move)

            case MoveEvalResponces.CASTLE_KINGSIDE:
                new_board = self.get_board_after_castle_kingside(move)

            case MoveEvalResponces.CASTLE_QUEENSIDE:
                new_board = self.get_board_after_castle_queenside(move)

            case MoveEvalResponces.EN_PASSENT:
                new_board = self.get_board_after_en_passent(move)

            case MoveEvalResponces.DOUBLE_PUSH:
                new_board = self.get_board_after_double_push(move)

            case MoveEvalResponces.PROMOTION:
                new_board = self.get_board_after_promotion(move)
            case _:
                print("error with eval move")

        return new_board

    def get_clicked_piece(self) -> Piece:
        for piece in self.piece_map.values():
            if piece.click:
                return piece
        return -1

    def get_jumping_moves(
        self, start_square, offsets: list[tuple[int, int]]
    ) -> list[Move]:
        valid_moves = []
        for offset in offsets:
            if not will_move_out(start_square, offset):
                new_square = get_square_after_move(start_square, offset)
                if new_square in self.piece_map.keys():
                    if not self.piece_map[new_square].is_same_colour(
                        self.piece_map[start_square]
                    ):
                        # not same colour
                        valid_moves.append((start_square, new_square, ""))
                else:
                    # empty square
                    valid_moves.append((start_square, new_square, ""))
        return valid_moves

    def get_sliding_moves(
        self, start_square, offset: tuple[int, int], max_depth=8
    ) -> list[Move]:
        if start_square not in self.piece_map:
            self.print()
        depth = 1
        valid_moves = []
        while (
            not will_move_out(start_square, multiply_in_tuple(offset, depth))
            and depth <= max_depth
        ):
            new_square = get_square_after_move(
                start_square, multiply_in_tuple(offset, depth)
            )
            if new_square in self.piece_map.keys():
                if not self.piece_map[new_square].is_same_colour(
                    self.piece_map[start_square]
                ):
                    # if the piece is not the same colour as this one
                    valid_moves.append((start_square, new_square, ""))
                break
            else:
                # empty square
                valid_moves.append((start_square, new_square, ""))
                depth += 1
        return valid_moves

    def get_fen(self) -> str:
        fen = ""
        for c_i in range(8):
            consecutive_empty = 0
            for r_i in range(8):
                square_index = (8 * c_i) + r_i
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
            fen += "/"
        fen = fen[:-1]  # remove last slash, easier than checking if its last row

        fen += " w " if self.is_white_turn else " b "

        has_any_castle_right = (
            len([active_cr for active_cr in self.castling_rights.values() if active_cr])
            > 0
        )
        for castle_right in self.castling_rights.keys():
            if self.castling_rights[castle_right]:
                fen += castle_right
        if not has_any_castle_right:
            fen += "-"
        fen += " "

        fen += (
            "- " if self.en_passent_target == -1 else str(self.en_passent_target) + " "
        )

        fen += str(self.move_count) + " "

        fen += str(self.halfmove_count)

        return fen

    def get_pieces(self) -> list[Piece]:
        return self.piece_map.values()

    def switch_is_white_turn(self) -> bool:
        return not self.is_white_turn

    def del_piece(self, piece: Piece) -> None:
        del self.piece_map[piece.square]

    def update_pieces(self) -> None:
        for piece in self.get_pieces():
            piece.update()


class Game:
    def __init__(self, starting_fen=STARTING_FEN) -> None:
        self.engine = engine.Engine(STOCKFISH_PATH)
        self.square_size = 100
        self.top_left = (200, 100)
        self.bottom_right = (
            self.top_left[0] + (8 * self.square_size),
            self.top_left[1] + (8 * self.square_size),
        )
        square_cords_gen_x = range(
            self.top_left[0], self.bottom_right[0], self.square_size
        )
        square_cords_gen_y = range(
            self.top_left[1], self.bottom_right[1], self.square_size
        )
        self.square_cords = [
            [i, j] for i in square_cords_gen_x for j in square_cords_gen_y
        ]
        self.white_prom_start = self.top_left[0], self.top_left[1] - 1.5 * self.square_size
        self.black_prom_start = self.top_left[0], self.top_left[1] + (7*self.square_size)
        self.surface = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.boards = [Board(self, *fen_to_board_input(starting_fen, self))]
        self.boards[0].print()
        self.white_taken_pieces = []
        self.black_taken_pieces = []
        self.last_update = time.time()
        min_to_sec = lambda m: m * 60
        self.white_time = min_to_sec(5)
        self.black_time = min_to_sec(5)
        self.is_white_promoting = False
        self.is_black_promoting = False
        self.attempted_promotion: Move
        self.is_game_over = False
        self.display_blue = True
        self.is_engine_white = False
        self.enable_engine = False
        """
        Note:
        Used to have is_white_turn and move_count in this init but because
        they WERE only used to create the board, it makes WAYYYY more sense to
        have a function that turns the fen string into everything EXCEPT the
        game being passed in
        """

    def is_promoting(self) -> bool:
        return self.is_white_promoting or self.is_black_promoting

    def is_engine_turn(self) -> bool:
        return (
            self.get_current_board().is_white_turn == self.is_engine_white
            and self.enable_engine
        )

    def toggle_blue(self) -> None:
        self.display_blue = ~self.display_blue

    def is_inside_bounds(self, abs_x, abs_y) -> bool:
        return (
            self.top_left[0] <= abs_x <= self.bottom_right[0]
            and self.top_left[1] <= abs_y <= self.bottom_right[1]
        )

    def mouse_inside_bounds(self) -> bool:
        return self.is_inside_bounds(*pg.mouse.get_pos())

    def relative_board_cords(self, x, y) -> Cord:
        return (x - self.top_left[0], y - self.top_left[1])

    def absolute_board_cords(self, rel_x, rel_y) -> Cord:
        return (rel_x + self.top_left[0], rel_y + self.top_left[1])

    def get_square_index(self, x, y) -> int:
        """
        Precondition: x, y point must be inside board already
        """
        x, y = self.relative_board_cords(x, y)
        x //= self.square_size
        y //= self.square_size
        return (y * 8) + x

    def get_cords_from_index(self, index: int) -> Cord:
        y, x = divmod(index, 8)
        x *= self.square_size
        y *= self.square_size
        return self.absolute_board_cords(x, y)

    def get_current_board(self) -> "Board":
        return self.boards[-1]

    def add_board(self, board) -> None:
        self.boards.append(board)

    def get_promotion_query_rects(self) -> list[tuple[str, pg.Rect]]:
        rects = []
        promotion_query_cords = (self.white_prom_start
                                 if self.is_white_promoting
                                 else self.black_prom_start)

        promotion_pieces = (
            WHITE_PROMOTION_PIECES
            if self.is_white_promoting
            else BLACK_PROMOTION_PIECES
        )
        for count, piece_glyph in enumerate(promotion_pieces):
            abs_cords = add_tuples(
                promotion_query_cords, (50 * count, self.square_size)
            )
            rect = pg.Rect(*abs_cords, self.square_size, self.square_size)
            rects.append((piece_glyph, rect))
        return rects

    def display_promotion_query(self):
        for glyph, rect in self.get_promotion_query_rects():
            piece_img = get_piece_img(glyph)
            pg.transform.scale(piece_img, (self.square_size, self.square_size))
            self.surface.blit(piece_img, rect)

    def get_selected_promotion_option(self) -> str:
        mouse_cords = pg.mouse.get_pos()
        for glyph, rect in self.get_promotion_query_rects():
            if rect.collidepoint(mouse_cords):
                return glyph
        return ""

    def update_timer(self) -> None:
        # subtract the difference between the last update and current time
        # onto the current colors remaining time
        cur_time = time.time()
        delta_time = cur_time - self.last_update
        if self.get_current_board().is_white_turn:
            self.white_time -= delta_time
        else:
            self.black_time -= delta_time

        self.last_update = time.time()

    def display_gui(self) -> None:
        # update timers by setting font test to current timers
        timer_font = pg.font.Font(None, TIMER_FONT_SIZE)
        white_timer_rect = pg.Rect(
            self.bottom_right[0] + TIMER_X_OFFSET,
            self.top_left[1] + TIMER_W_Y_OFFSET,
            TIMER_WIDTH,
            TIMER_HEIGHT,
        )
        black_timer_rect = pg.Rect(
            self.bottom_right[0] + TIMER_X_OFFSET,
            self.top_left[1] + TIMER_B_Y_OFFSET,
            TIMER_WIDTH,
            TIMER_HEIGHT,
        )
        white_time_min, white_time_sec = divmod(self.white_time, 60)
        black_time_min, black_time_sec = divmod(self.black_time, 60)
        white_time_txt = timer_font.render(
            f"{white_time_min:.0f}:{white_time_sec:.1f}", True, TIMER_FONT_COLOR
        )
        black_time_txt = timer_font.render(
            f"{black_time_min:.0f}:{black_time_sec:.1f}", True, TIMER_FONT_COLOR
        )
        self.surface.blit(white_time_txt, white_timer_rect)
        self.surface.blit(black_time_txt, black_timer_rect)

        # display pieces taken
        white_display_counter = 0
        for white_taken_glyph in self.white_taken_pieces:
            img = get_piece_img(white_taken_glyph)
            pg.transform.scale(
                img, (TAKEN_PIECE_DISPLAY_IMG_SIZE, TAKEN_PIECE_DISPLAY_IMG_SIZE)
            )
            self.surface.blit(
                img,
                pg.Rect(
                    self.bottom_right[0]
                    + TAKEN_PIECE_DISPLAY_INIT_X_OFFSET
                    + (
                        TAKEN_PIECE_DISPLAY_OFFSET_BETWEEN_PIECES
                        * white_display_counter
                    ),
                    self.top_left[1] + TAKEN_PIECE_DISPLAY_W_Y_OFFSET,
                    TAKEN_PIECE_DISPLAY_IMG_SIZE,
                    TAKEN_PIECE_DISPLAY_IMG_SIZE,
                ),
            )
            white_display_counter += 1

        black_display_counter = 0
        for black_taken_glyph in self.black_taken_pieces:
            img = get_piece_img(black_taken_glyph)
            pg.transform.scale(
                img, (TAKEN_PIECE_DISPLAY_IMG_SIZE, TAKEN_PIECE_DISPLAY_IMG_SIZE)
            )
            self.surface.blit(
                img,
                pg.Rect(
                    self.bottom_right[0]
                    + TAKEN_PIECE_DISPLAY_INIT_X_OFFSET
                    + (
                        TAKEN_PIECE_DISPLAY_OFFSET_BETWEEN_PIECES
                        * black_display_counter
                    ),
                    self.top_left[1] + TAKEN_PIECE_DISPLAY_B_Y_OFFSET,
                    TAKEN_PIECE_DISPLAY_IMG_SIZE,
                    TAKEN_PIECE_DISPLAY_IMG_SIZE,
                ),
            )
            black_display_counter += 1

        if self.is_white_promoting or self.is_black_promoting:
            self.display_promotion_query()

    def display_grid(self) -> None:
        for x, y in self.square_cords:
            row = x // self.square_size
            column = y // self.square_size
            rect = pg.Rect([x, y, self.square_size, self.square_size])
            image = pg.Surface(rect.size).convert()
            if not (is_odd(row) ^ is_odd(column)):
                black_square(self.surface, image, rect)
            else:
                white_square(self.surface, image, rect)

            square_num = game.get_square_index(x, y)
            font = pg.font.Font(None, 32)
            font_color = (0, 0, 0)
            square_num_rect = pg.Rect(x + 10, y, 10, 10)
            algebraic_rect = pg.Rect(x + 65, y, 10, 10)
            txt_square_i = font.render(str(square_num), True, font_color)
            txt_algebraic = font.render(
                str(square_index_to_algebraic(square_num)), True, font_color
            )
            self.surface.blit(txt_square_i, square_num_rect)
            # self.surface.blit(txt_algebraic, algebraic_rect)
        if self.display_blue:
            self.display_blue_squares()

    def clear_surface(self) -> None:
        self.surface.fill((20, 20, 20))

    def display_blue_squares(self) -> None:
        board = self.get_current_board()
        if board == -1:
            return
        piece = board.get_clicked_piece()
        if piece == -1:
            return
        legal_squares = []
        for move in piece.get_valid_moves():
            target_sqr = move[MOVE_END]
            board_after = board.get_board_after_move(piece, move)
            if board_after != -1:
                if not board_after.is_in_check(not board_after.is_white_turn):
                    legal_squares.append(target_sqr)
            else:
                print(f"this board is not valid {move}")
        make_squares_blue(self, self.surface, self.square_size, legal_squares)

    def update_game(self) -> None:
        self.clear_surface()
        self.display_grid()
        self.update_timer()
        self.display_gui()
        self.get_current_board().update_pieces()


# the main loop needs to call an event loop to establish an interactive game
# and needs to call the game to update itself
def main(game: Game) -> None:
    frame_start = time.time()
    game_event_loop(game)
    game.update_game()
    frame_end = time.time()
    time.sleep(max(((1 / 60) - (frame_end - frame_start), 0)))


# Notice that the event loop has been given its own function. This makes
# the program easier to understand.
def game_event_loop(game) -> None:
    # maybe add divergent path for engine input here?
    if game.is_engine_turn():
        board = game.get_current_board()
        try:
            best_move_str = engine.get_bestmove(board.get_fen(), 1000, "")
            print(best_move_str)
        except:  # do not know how to define stockfish crash as exp.
            return
        alg_start, alg_end = best_move_str[:2], best_move_str[2:]
        start_square = algebraic_to_square(alg_start)
        end_square = algebraic_to_square(alg_end)
        move = (start_square, end_square, "")
        piece = board.piece_map[start_square]
        new_board = board.get_board_after_move(piece, move)
        game.add_board(new_board)
    else:
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                on_mouse_down(game)
            elif event.type == pg.MOUSEBUTTONUP:
                on_mouse_up(game)
            elif event.type == pg.QUIT:
                pg.quit()
                sys.exit()


RAND_FENS_PATH = "/home/alonge/Documents/code/capstone/engine/random_fens.txt"


def get_random_fen() -> str:
    with open(RAND_FENS_PATH) as fen_file:
        fens = fen_file.readlines()
    fen = fens[randint(0, len(fens) - 1)]
    return fen


test_fen_strings = [
    STARTING_FEN,
    "8/8/8/8/8/8/8/8 w - - 0 1",
    "8/6p1/5P2/4p3/3P4/2p5/1P6/8 w - - 0 1",
    "k7/8/8/3bQ3/3nR3/8/8/8 b KQkq - 0 1",
    get_random_fen(),
    "8/3pp3/8/8/8/8/3PP3/8 b - - 0 1",
    "r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1",
    "8/3P4/8/K7/7k/8/4p3/8 w - - 0 1",
    "8/R3k3/7b/8/8/3R4/3K4/8 w - - 0 1",
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
"rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1"
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
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    pg.init()
    fen = test_fen_strings[int(input(fen_prompt))]
    print(fen)
    game = Game(fen)
    MyClock = pg.time.Clock()
    while not game.is_game_over:
        main(game)
        pg.display.update()
        MyClock.tick(60)
