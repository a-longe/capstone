from chessboard import display

fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'

game_board = display.start()

while True:
    display.check_for_quit()
    display.update(fen, game_board)

    # board flip interface
    if not game_board.flipped:
        display.flip(game_board)
    fen = input("fen: ")