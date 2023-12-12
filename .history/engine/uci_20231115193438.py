from engine.board import Board
from engine.my_constants import *


is_running = True

game = Board(STARTING_BISHOPS, )

while is_running:
    command = input('> ')
    match command:
        case 'exit': is_running = False
        case 'position' 
    