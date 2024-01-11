import pytest
import gui
	
random_fens = open("random_fens.txt", 'r')
game = gui.Game(gui.STARTING_FEN)

@pytest.mark.parametrize("input_fen, expected", [(fen.strip(), fen.strip()) for fen in random_fens])
def test_get_fen(input_fen, expected):
	assert expected == gui.Board(game, *gui.fen_to_board_input(input_fen)).get_fen()