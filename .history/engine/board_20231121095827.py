import my_constants as const
from my_utils import row_index_to_legend, row_legend_to_index, column_index_to_letter, column_letter_to_index
from piece import get_piece_obj, Piece


class Board:
    def __init__(self, piece_list:list, # list of type piece, circular import
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
        

    def setup_board(self, fen=const.STARTING_FEN) -> None:
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
                    position = (column_index_to_letter[column_index_counter], row_legend)
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
                    print('- ' * int(char), end='')
                else:
                    print(char, end=' ')
            print('\n', end='')
        print(fen)


    def get_fen(self) -> str:
        # create dictionary with the rows as keys and all the pieces in
        # each row goes in the value
        rows = {}
        for piece in self.piece_list:
            dict_key = row_legend_to_index[int(piece.position[const.PIECE_LOCATION_ROW])]
            if dict_key in rows.keys():
                rows[dict_key].append(piece)
            else:
                rows[dict_key] = [piece]
        
        fen_str = ''
        for row_index in range(const.NUM_ROWS):
            row_str = ''
            if row_index in rows.keys():
                # there are pieces on this row
                row_list = ['-' for not_accessed in range(const.LEN_ROW)]
                pieces_on_row = rows[row_index]
                for piece in pieces_on_row:
                    piece_symbol = piece.piece_type
                    if piece.color == 'w': piece_symbol = piece_symbol.upper()
                    column_letter = piece.position[const.PIECE_LOCATION_COLUMN]
                    row_list[column_letter_to_index[column_letter]] = piece_symbol
                    # row_list should be something like:
                    # ['-', 'P', '-', 'k', 'Q', 'n', '-', '-']
                consecutive_empty = 0
                for char in row_list:
                    if char == '-':
                        consecutive_empty += 1
                    else:
                        if consecutive_empty > 0:
                            row_str+=str(consecutive_empty)
                            consecutive_empty = 0
                        row_str+=char
            else:
                row_str = const.EMPTY_FEN_ROW
            fen_str += row_str + '/'
        fen_str = fen_str[:-1] # take away last char to remove last /
        print(fen_str)
                
        

    def get_all_moves(self, color:str):
        pass