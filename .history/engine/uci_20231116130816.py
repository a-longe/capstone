from engine.board import Board
from engine.my_constants import *


def create_new_game() -> Board:
    return Board(STARTING_PIECE_LIST, True, STARTING_CASTLING_RIGHTS, [], 0, 0)


is_running = True

game_board = create_new_game()

while is_running:
    command = input('> ')
    match command:
        case 'exit': is_running = False
        case 'position': engine.board.create_new_game()
    
