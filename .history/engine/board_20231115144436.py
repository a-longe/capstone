import my_constants

class Bitboard:
    def __init__(self, num) -> None:
        self.num = num
        self.bin = bin(num)
    
    def display(self) -> None:
        board_num = self.num
        zeros_before = 64 - board_num.bit_length()
        board_str = ('0'*zeros_before) + bin(board_num)[2:]
        for index_multiple in range(0, 8):
            print(board_str[(0 + (8*index_multiple)):(8 + (8*index_multiple))])


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

