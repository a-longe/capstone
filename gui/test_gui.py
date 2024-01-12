import pytest
import gui
	
random_fens = open("random_fens.txt", 'r')
game = gui.Game(gui.STARTING_FEN)

@pytest.mark.parametrize("expected", [fen.strip() for fen in random_fens])
def test_get_fen(expected):
	board = gui.Board(game, *gui.fen_to_board_input(expected))
	assert expected == board.get_fen()