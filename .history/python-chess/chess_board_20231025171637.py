from chessboard import display, constants
import subprocess, threading
import uci_handler, verify_moves
import mouse_event_handler as meh
import time
import pygame

game_board = display.start()
display.update(constants.STARTING_FEN, game_board)
fen = constants.STARTING_FEN
is_dragging = False
# print(verify_moves.parse_piece_rect(game_board.piece_rect))
MOVETIME = 500

while True:
    display.check_for_quit()
    # best_move = uci_handler.get_bestmove(fen, MOVETIME, "")
    # print(best_move)
    # fen = uci_handler.get_fen_after_move(fen, best_move)
    # print(fen)
    display.update(fen, game_board)
      
    # on any pygame events
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            # is mouse down event
            # find square that mouse is on
            event_sqr = meh.get_board_pos(*meh.get_mouse_pos())

    # print(meh.get_board_pos(*meh.get_mouse_pos()))

    # board flip interface
    if not game_board.flipped:
        display.flip(game_board)
