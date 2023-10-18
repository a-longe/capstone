import pygame
from chessboard import board

SQUARE_WIDTH = 50


def print_mouse_pos()->None:
    pos = pygame.mouse.get_pos()
    print(get_board_cords(pos[0], pos[1]))

def get_board_cords(x:float, y:float) -> str:
    is_found = False
    board_cords = board.Board.board_rect
    row_location:int = 0
    square_location:int = 0
    for row_index, row in enumerate(board_cords):
        for square_index, square in enumerate(row):
            x_min = square[0]
            y_min = square[1]
            x_max = x_min + SQUARE_WIDTH
            y_max = y_min + SQUARE_WIDTH
            print(f"x: {x_min} <= x < {x_max}")
            print(f"y: {y_min} <= y < {y_max}")
            print(f"cords: {square}")
            if x >= x_min and x < x_max:
                if y >= y_min and y < y_max:
                    is_found = True
                    row_location = row_index
                    square_location = square_index
                    break
        if is_found: break
        else: KeyError() ; return "OOB"
    # convert location_indecies into a string
    # print(row_location, square_location)
    return f'{index_to_letter[row_location]}{ square_location + 1}'
    

