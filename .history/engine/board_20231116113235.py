import engine.my_constants
import engine.my_utils
import engine.piece

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

    def setup_board(self, fen=my_constants.STARTING_FEN) -> None:
        piece_str, active_color, castling_rights_str, en_passant_target, \
        halfmove_str, fullmove_str = fen.split()
        piece_list = []
        rows = piece_str.split('/')
        for index, row in enumerate(rows):
            row_legend = my_utils.row_index_to_legend[index]
            column_index_counter = 0
            for piece in row:
                if piece.is_digit():
                    column_index_counter += int(piece)
                else:
                    
                    column_index_counter += 1


    def get_fen_() -> str:
        pass

    def get_all_moves(color:str):
        pass