from my_constants import STARTING_FEN as STARTING_FEN, LOCATION_ROW
from my_utils import row_index_to_legend, row_legend_to_index, get_piece_obj, column_index_to_letter
from piece import Piece

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
        piece_str, active_color, castling_rights_str, en_passant_target,\
        halfmove_clock_str, fullmove_clock_str = fen.split()

        # set piece list
        self.piece_list = []
        rows = piece_str.split('/')
        for index, row in enumerate(rows):
            row_legend = str(row_index_to_legend[index])
            column_index_counter = 0
            for char in row:
                if char.isdigit():
                    column_index_counter += int(char)
                else:
                    if char.islower():
                        color = 'b'
                    else:
                        color = 'w'
                    position = column_index_to_letter[column_index_counter] + row_legend
                    self.piece_list.append(get_piece_obj(char.lower(), color, position))
                    column_index_counter += 1
        
        # set white turn
        self.white_turn = active_color == 'w'

        # set castling_rights
        self.castling_rights['K'] = 'K' in castling_rights_str
        self.castling_rights['Q'] = 'Q' in castling_rights_str
        self.castling_rights['k'] = 'k' in castling_rights_str
        self.castling_rights['q'] = 'q' in castling_rights_str


        # set en passant target
        self.en_passant_target = en_passant_target

        # set move clocks
        self.halfmove_clock = int(halfmove_clock_str)
        self.fullmove_clock = int(fullmove_clock_str)



    # EVENTUALLY REMOVE ALL PARAMETERS, DISPLAYS CURRENT BOARD STATE, 
    # NOT A GIVEN ONE
    def display_board(self, fen:str) -> None:
        piece_str = fen.split()[0]
        rows = piece_str.split('/')
        for row in rows:
            for char in row:
                if char.isdigit():
                    print('-' * int(char), end='')
                else:
                    print(char, end=' ')
            print('\n', end='')
        print(fen)


    def get_fen(self) -> str:
        # create dictionary with the rows as keys and all the pieces in
        # each row goes in the value
        rows = {}
        for piece in self.piece_list:
            dict_key = row_legend_to_index[int(piece.position[LOCATION_ROW])]
            if dict_key in rows.keys():
                rows[dict_key].append(piece)
            else:
                rows[dict_key] = [piece]
        print(rows)
                
        

    def get_all_moves(self, color:str):
        pass