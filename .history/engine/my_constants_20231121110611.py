from piece import Piece, Pawn, Rook, Knight, Bishop, Queen, King

PIECE_LOCATION_COLUMN = 0
PIECE_LOCATION_ROW = 1

LEN_ROW = 8
NUM_ROWS = 8
NUM_SQUARES = 64

STARTING_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
EMPTY_FEN_ROW = '8/'

STARTING_PIECE_LIST = [Rook('b', ('a',  '8')), Knight('b', ('b',  '8')), Bishop('b', ('c',  '8')),
                       Queen('b', ('d',  '8')), King('b', ('e',  '8')), Bishop('b', ('f',  '8')),
                       Knight('b', ('g',  '8')), Rook('b', ('h',  '8')), Pawn('b', ('a',  '7')),
                       Pawn('b', ('b',  '7')), Pawn('b', ('c',  '7')), Pawn('b', ('d',  '7')),
                       Pawn('b', ('e',  '7')), Pawn('b', ('f',  '7')), Pawn('b', ('g',  '7')),
                       Pawn('b', ('h',  '7')), Pawn('w', ('a',  '2')), Pawn('w', ('b',  '2')),
                       Pawn('w', ('c',  '2')), Pawn('w', ('d',  '2')), Pawn('w', ('e',  '2')),
                       Pawn('w', ('f',  '2')), Pawn('w', ('g',  '2')), Pawn('w', ('h',  '2')),
                       Rook('w', ('a',  '1')), Knight('w', ('b',  '1')), Bishop('w', ('c',  '1')),
                       Queen('w', ('d',  '1')), King('w', ('e',  '1')), Bishop('w', ('f',  '1')),
                       Knight('w', ('g',  '1')), Rook('w', ('h',  '1'))]

STARTING_CASTLING_RIGHTS = {
    'K':True,
    'Q':True,
    'k':True,
    'q':True
}

STARTING_IS_WHITE = True
STARTING_EN_PASSANT_TARGET = '-'
STARTING_HALFMOVE_CLOCK = 0
STARTING_FULLMOVE_CLOCK = 0

STARTING_METADATA = (
    STARTING_IS_WHITE,
    STARTING_CASTLING_RIGHTS,
    STARTING_EN_PASSANT_TARGET,
    STARTING_HALFMOVE_CLOCK,
    STARTING_FULLMOVE_CLOCK
)