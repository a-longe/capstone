from chessboard import display
import subprocess
import uci_handler

init_fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
game_board = display.start()
display.update(init_fen, game_board)

while True:
    display.check_for_quit()
    fen = input("fen: ")
    display.update(fen, game_board)

    # board flip interface
    if not game_board.flipped:
        display.flip(game_board)
    