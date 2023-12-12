from chessboard import display, constants
import subprocess, threading
import uci_handler, verify_moves
import mouse_event_handler as meh
import time
import pygame

piece_to_drag = None
game_board = display.start()
display.update(constants.STARTING_FEN, game_board)
fen = constants.STARTING_FEN
is_dragging = False
MOVETIME = 500

while True:
    display.check_for_quit()
    """
    best_move = uci_handler.get_bestmove(fen, MOVETIME, "")
    print(best_move)
    fen = uci_handler.get_fen_after_move(fen, best_move)
    print(fen)
    """
    display.update(fen, game_board)
    
    mouse_event = None
    # on any pygame events
    for event in pygame.event.get():
        # if there is a mouse botton up event, turn off dragging and
        # check what box the mouse is in, as long as it's not the same
        # box, release and snap to new box
        # NOTE Eventually add bitboard updates here
        if event.type == pygame.MOUSEBUTTONUP and is_dragging:
            is_dragging = False
            mouse_event = event
            new_sqr = meh.get_board_pos(*mouse_event.dict['pos'])
            exec("piece_to_drag['piece'].position = game_board." + new_sqr)
            piece_to_drag = None

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # is mouse down event
            mouse_event = event

            # find square that mouse is on
            event_sqr = meh.get_board_pos(*mouse_event.dict['pos'])
            print(event_sqr)

            # if the click is on the board (ie: not 'OOB')
            if event_sqr != 'OOB':
                # print piece information
                pieces = verify_moves.parse_piece_rect(game_board.piece_rect)
                if event_sqr in pieces.keys():
                    # if this suceeds, set dragging to True
                    is_dragging = True
                    piece_to_drag = pieces[event_sqr]

    # if is_dragging is true set position of 
    if is_dragging and piece_to_drag != None:
        piece_to_drag['piece'].position = meh.get_mouse_pos()
        print(piece_to_drag['piece'].position)
    # print(meh.get_board_pos(*meh.get_mouse_pos()))

    # board flip interface
    if not game_board.flipped:
        display.flip(game_board)