from chessboard import display, constants
import subprocess
import uci_handler, mouse_event_handler

game_board = display.start()
display.update(constants.STARTING_FEN, game_board)
fen = constants.STARTING_FEN
MOVETIME = 5000

while True:
    display.check_for_quit()
    best_move = uci_handler.get_bestmove(fen, MOVETIME, "")
    print(best_move)
    fen = uci_handler.get_fen_after_move(fen, best_move)
    print(fen)
    display.update(fen, game_board)

    # board flip interface
    if not game_board.flipped:
        display.flip(game_board)
