from engine.board import Board
import engine.my_constants 


def test_example() -> None:
    assert True

def test_get_fen() -> None:
    board = Board(my_constants.STARTING_PIECE_LIST, my_constants.STARTING_EN_PASSANT_TARGET, my_constants.STARTING_CASTLING_RIGHTS, my_constants.STARTING_IS_WHITE, 0, 0)