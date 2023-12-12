from curses.ascii import isdigit
from my_constants import STARTING_FEN
from my_utils import row_index_to_legend, get_piece_obj, column_index_to_letter
from piece import Piece, Pawn, Rook, Knight, Bishop, Queen, King

class Board:
    def __init__(self, piece_list:list[Piece], 
                en_passant_target:str,
                castling_rights:dict[str, bool],
                white_turn:bool,
                halfmove_clock:int,
                fullmove_clock:int) -> None:
        self.piece_list = piece_list
        self.en_passant_target = en_passant_target
        self.castling_rights = castling_rights
        self.white_turn = white_turn
        self.halfmove_clock = halfmove_clock
        self.fullmove_clock = fullmove_clock

    def setup_board(self, fen=STARTING_FEN) -> None:
        piece_str = fen.split()[0]
        piece_list = []
        rows = piece_str.split('/')
        for index, row in enumerate(rows):
            row_legend = str(row_index_to_legend[index])
            column_index_counter = 0
            for char in row:
                if char.isdigit():
                    column_index_counter += int(char)
                else:
                    if char.islower():
                        color = 'w'
                    else:
                        color = 'b'
                    position = column_index_to_letter[column_index_counter] + row_legend
                    piece_list.append(get_piece_obj(char.lower(), color, position))
                    column_index_counter += 1
        print(piece_list)

    
    def display_board(self, fen:str) -> None:
        piece_str = fen.split()[0]
        rows = piece_str.split('/')
        for row in rows:
            for char in row:
                if char.isdigit():
                    print(' ' * int(char))
                else:
                    print(char)


    def get_fen() -> str:
        pass

    def get_all_moves(color:str):
        pass