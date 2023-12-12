import my_constants

class Bitboard:
    def __init__(self, num) -> None:
        self.num = num
        self.bin = bin(num)
    
    def display(self) -> None:
        board_num = self.num
        zeros_before = my_constants.NUM_SQUARES - board_num.bit_length()
        board_str = ('0'*zeros_before) + bin(board_num)[2:]
        for index_multiple in range(0, my_constants.NUM_ROWS):
            row_start_index = (0 + (my_constants.LEN_ROW*index_multiple))
            row_end_index = (my_constants.LEN_ROW + (my_constants.LEN_ROW*index_multiple))
            print(board_str[row_start_index:row_end_index])


class Board:
    def __init__(self, bitboards:list[Bitboard], 
                en_passant_targets:list[str],
                castling_rights:dict[str, bool],
                white_turn:bool,
                halfmove_clock:int,
                fullmove_clock:int) -> None:
        self.bitboards = bitboards
        self.en_passant_targets = en_passant_targets
        self.castling_rights = castling_rights
        self.white_turn = white_turn
        self.halfmove_clock = halfmove_clock
        self.fullmove_clock = fullmove_clock

