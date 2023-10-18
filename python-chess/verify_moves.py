import my_utils

CHESS_BOARD_LEN = 64
BINARY_PREFIX = '0b'

class CompassRose:
    n = -8
    ne = -7
    e = +1
    se = +9
    s = +8
    sw = +7
    w = -1
    nw = -9

class Bitboards:
    STARTING_BLACK_PIECES = int(
        "11111111"
        "11111111"
        "00000000"
        "00000000"
        "00000000"
        "00000000"
        "00000000"
        "00000000"
        , 2)

    STARTING_WHITE_PIECES = int(
        "00000000"
        "00000000"
        "00000000"
        "00000000"
        "00000000"
        "00000000"
        "11111111"
        "11111111"
        , 2)

    STARTING_PAWNS = int(
        "00000000"
        "11111111"
        "00000000"
        "00000000"
        "00000000"
        "00000000"
        "11111111"
        "00000000"
        , 2) 

    STARTING_KNIGHTS = int(
        "00100100"
        "00000000"
        "00000000"
        "00000000"
        "00000000"
        "00000000"
        "00000000"
        "00100100"
        , 2) 

    STARTING_BISHOPS = int(
        "01000010"
        "00000000"
        "00000000"
        "00000000"
        "00000000"
        "00000000"
        "00000000"
        "01000010"
        , 2) 

    STARTING_ROOKS = int(
        "10000001"
        "00000000"
        "00000000"
        "00000000"
        "00000000"
        "00000000"
        "00000000"
        "10000001"
        , 2)

    STARTING_KINGS = int(
        "00001000"
        "00000000"
        "00000000"
        "00000000"
        "00000000"
        "00000000"
        "00000000"
        "00001000"
        , 2)

    STARTING_QUEENS = int(
        "00010000"
        "00000000"
        "00000000"
        "00000000"
        "00000000"
        "00000000"
        "00000000"
        "00010000"
        , 2)


def get_bitboard_index(location:str) -> int:
    """
    Takes a chess board location as a string ("a1") and returns
    a index for the bitboards
    >>> get_bitboard_index('a1')
    56
    >>> get_bitboard_index('a8')
    0
    >>> get_bitboard_index('h1')
    63
    >>> get_bitboard_index('h8')
    7
    >>> get_bitboard_index('b8')
    1
    """
    row_offset = (8 - int(location[1])) * 8
    return row_offset + (my_utils.letter_to_index[location[:1]] + 1) - 1


def create_piece_bitboard(location:str) -> int:
    index = get_bitboard_index(location)
    zeros_before = index - 1
    zeros_after = CHESS_BOARD_LEN - 1 - index
    bitboard:str = BINARY_PREFIX + \
                '0' * zeros_before + \
                '1' + \
                '0' * zeros_after
    return int(bitboard, 2)

