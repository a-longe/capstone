from piece import Piece, Pawn, Rook, Knight, Bishop, Queen, King

LEN_ROW = 8
NUM_ROWS = 8
NUM_SQUARES = 64

STARTING_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

STARTING_PIECE_LIST = [Rook('b', 'a8'), Knight('b', 'b8'), Bishop('b', 'c8'),
                       Queen('b', 'd8'), King('b', 'e8'), Bishop('b', 'f8'),
                       Knight('b', 'g8'), Rook('b', 'h8'), Pawn('b', 'a7'),
                       Pawn('b', 'b7'), Pawn('b', 'c7'), Pawn('b', 'd7'),
                       Pawn('b', 'e7'), Pawn('b', 'f7'), Pawn('b', 'g7'),
                       Pawn('b', 'h7'), Pawn('w', 'a2'), Pawn('w', 'b2'),
                       Pawn('w', 'c2'), Pawn('w', 'd2'), Pawn('w', 'e2'),
                       Pawn('w', 'f2'), Pawn('w', 'g2'), Pawn('w', 'h2'),
                       Rook('w', 'a1'), Knight('w', 'b1'), Bishop('w', 'c1'),
                       Queen('w', 'd1'), King('w', 'e1'), Bishop('w', 'f1'),
                       Knight('w', 'g1'), Rook('w', 'h1')]

STARTING_CASTLING_RIGHTS = {
    'K':True,
    'Q':True,
    'k':True,
    'q':True
}

STARTING_IS_WHITE = True
STARTING_EN_PASSANT_TARGETS = '-'
STARTING_HALFMOVE_CLOCK = 0
STARTING_FULLMOVE_CLOCK = 0

STARTING_METADATA = (
    STARTING_IS_WHITE,
    STARTING_CASTLING_RIGHTS,
    STARTING_EN_PASSANT_TARGETS,
    STARTING_HALFMOVE_CLOCK,
    STARTING_FULLMOVE_CLOCK
)