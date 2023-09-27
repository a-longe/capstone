import os
import subprocess

STOCKFISH_RUN_COMMAND = "~/Documents/stockfish/stockfish/./stockfish-ubuntu-x86-64-avx2"
# os.system(STOCKFISH_RUN_COMMAND)

# process = subprocess.Popen([STOCKFISH_RUN_COMMAND], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
# out = subprocess.run([STOCKFISH_RUN_COMMAND], shell=True, capture_output=True, text=True, timeout=5)
# print(out.stdout)

# output, errors = process.communicate()
# print(output, errors)
init_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
move_time = 1000

stockfish = subprocess.check_output(f'printf "position fen {init_fen}\ngo movetime {move_time}\nucinewgame\n" | {STOCKFISH_RUN_COMMAND}'
                                            , shell=True, text=True, timeout=5)

print(stockfish)