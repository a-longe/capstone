import os
import subprocess
from chessboard import constants


STOCKFISH_RUN_COMMAND = "~/Documents/stockfish/stockfish/./stockfish-ubuntu-x86-64-avx2"
BESTMOVE_LINE_INDEX:tuple = (9, 14)
FEN_LINE_INDEX = 5

def call_stockfish(commands: list[str]) -> str:
    cmd_string = "\n".join(commands)
    responce = subprocess.check_output(f'printf "{cmd_string}" | {STOCKFISH_RUN_COMMAND}'
                                            , shell=True, text=True, timeout=5)
    return responce

def get_last_line_with_prefix(s:str, prefix:str) -> str:
    count = -1
    lines = s.split("\n")
    for i in lines:
        if prefix in lines[count]:
            return lines[count]
        count -= 1
    return "" 

def get_bestmove(fen:str, time_ms:int, moves:str) -> str:
    sf_responce = call_stockfish([f"position fen {fen} moves {moves}", f"go movetime {str(time_ms)}", "ucinewgame"])
    bestmove_line = get_last_line_with_prefix(sf_responce, "bestmove")
    return bestmove_line[BESTMOVE_LINE_INDEX[0]:BESTMOVE_LINE_INDEX[1]]
    
def get_fen_after_move(fen:str, moves:str) -> str:
    sf_responce = call_stockfish([f"position fen {fen} moves {moves}", "d", "ucinewgame"])
    fen_line = get_last_line_with_prefix(sf_responce, "Fen:")
    return fen_line[FEN_LINE_INDEX:]

move_time = 1000
moves: list[str] = []
