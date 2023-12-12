from engine.board import Board
from engine import my_constants


def test_example() -> None:
    assert True

def test_get_fen() -> None:
    board = Board(my_constants.STARTING_PIECE_LIST, 
                my_constants.STARTING_EN_PASSANT_TARGET, 
                my_constants.STARTING_CASTLING_RIGHTS, 
                my_constants.STARTING_IS_WHITE, 
                my_constants.STARTING_HALFMOVE_CLOCK, 
                my_constants.STARTING_FULLMOVE_CLOCK)
    assert board.get_fen() == my_constants.STARTING_FEN