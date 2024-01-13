import pytest
import gui
import time, datetime
	
random_fens = open("../engine/random_fens.txt", 'r')
game = gui.Game(gui.STARTING_FEN)

@pytest.mark.parametrize("expected", [fen.strip() for fen in random_fens])
def test_get_fen(expected):
	board = gui.Board(game, *gui.fen_to_board_input(expected))
	assert expected == board.get_fen()

def test_get_legal_move_speed():
	with open("../engine/random_fens.txt", 'r') as rand_fens:
		boards = []
		for fen in rand_fens:
			boards.append(gui.Board(game, *gui.fen_to_board_input(fen)))

	start_time = time.time()
	sum_moves = 0
	for board in boards:
		for piece in board.get_pieces():
			sum_moves += len(piece.get_legal_moves())
	end_time = time.time()
	time_diff = end_time - start_time
	with open('get_legal_moves_time_log.txt', 'a') as logger:
		logger.write(f"{datetime.date.today().strftime('%A %B %d')} - {sum_moves} in {time_diff:.4f} -- {sum_moves/time_diff:.2f} mps\n")


random_fens.close()

