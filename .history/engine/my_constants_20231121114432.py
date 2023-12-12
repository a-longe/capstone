from piece import Piece, Pawn, Rook, Knight, Bishop, Queen, King
from board import Board

PIECE_LOCATION_COLUMN = 0
PIECE_LOCATION_ROW = 1

LEN_ROW = 8
NUM_ROWS = 8
NUM_SQUARES = 64

STARTING_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
EMPTY_FEN_ROW = '8/'

STARTING_PIECE_LIST = [Rook('b', ('a',  '8'), STARTING_BOARD), Knight('b', ('b',  '8'), STARTING_BOARD), Bishop('b', ('c',  '8'), STARTING_BOARD),
                       Queen('b', ('d',  '8'), STARTING_BOARD), King('b', ('e',  '8'), STARTING_BOARD), Bishop('b', ('f',  '8'), STARTING_BOARD),
                       Knight('b', ('g',  '8'), STARTING_BOARD), Rook('b', ('h',  '8'), STARTING_BOARD), Pawn('b', ('a',  '7'), STARTING_BOARD),
                       Pawn('b', ('b',  '7'), STARTING_BOARD), Pawn('b', ('c',  '7'), STARTING_BOARD), Pawn('b', ('d',  '7'), STARTING_BOARD),
                       Pawn('b', ('e',  '7'), STARTING_BOARD), Pawn('b', ('f',  '7'), STARTING_BOARD), Pawn('b', ('g',  '7'), STARTING_BOARD),
                       Pawn('b', ('h',  '7'), STARTING_BOARD), Pawn('w', ('a',  '2'), STARTING_BOARD), Pawn('w', ('b',  '2'), STARTING_BOARD),
                       Pawn('w', ('c',  '2'), STARTING_BOARD), Pawn('w', ('d',  '2'), STARTING_BOARD), Pawn('w', ('e',  '2'), STARTING_BOARD),
                       Pawn('w', ('f',  '2'), STARTING_BOARD), Pawn('w', ('g',  '2'), STARTING_BOARD), Pawn('w', ('h',  '2'), STARTING_BOARD),
                       Rook('w', ('a',  '1'), STARTING_BOARD), Knight('w', ('b',  '1'), STARTING_BOARD), Bishop('w', ('c',  '1'), STARTING_BOARD),
                       Queen('w', ('d',  '1'), STARTING_BOARD), King('w', ('e',  '1'), STARTING_BOARD), Bishop('w', ('f',  '1'), STARTING_BOARD),
                       Knight('w', ('g',  '1'), STARTING_BOARD), Rook('w', ('h',  '1'), STARTING_BOARD)]

STARTING_CASTLING_RIGHTS = {
    'K':True,
    'Q':True,
    'k':True,
    'q':True
}

STARTING_IS_WHITE = True
STARTING_EN_PASSANT_TARGET = '-'
STARTING_HALFMOVE_CLOCK = 0
STARTING_FULLMOVE_CLOCK = 1

STARTING_METADATA = (
    STARTING_IS_WHITE,
    STARTING_CASTLING_RIGHTS,
    STARTING_EN_PASSANT_TARGET,
    STARTING_HALFMOVE_CLOCK,
    STARTING_FULLMOVE_CLOCK
)

STARTING_BOARD = Board(STARTING_PIECE_LIST, STARTING_EN_PASSANT_TARGET, 
                       STARTING_CASTLING_RIGHTS, STARTING_IS_WHITE, 
                       STARTING_HALFMOVE_CLOCK, STARTING_FULLMOVE_CLOCK)
