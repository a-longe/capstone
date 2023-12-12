from board import Board
from my_constants import *


def create_new_game() -> Board:
    return Board(STARTING_PIECE_LIST, STARTING_EN_PASSANT_TARGET, STARTING_CASTLING_RIGHTS, True, 0, 0)


is_running = True

game_board = create_new_game()

while is_running:
    commands = input('> ').split()
    match commands[0]:
        case 'exit': is_running = False
        case 'position': game_board = create_new_game()
    
