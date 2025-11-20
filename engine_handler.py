import subprocess


class Engine:
    def __init__(self, path:str) -> None:
        self.engine = subprocess.Popen(path, 
                                       stdin=subprocess.PIPE,
                                       stdout=subprocess.PIPE,
                                       universal_newlines=True,
                                       shell=False)
    
    def push_cmd(self, command:str) -> None:
        self.engine.stdin.write(command + '\n')
        self.engine.stdin.flush()

    def reset_board(self) -> None:
        self.push_cmd(f"position startpos")

    def set_position(self, fen:str) -> None:
        self.push_cmd(f"position fen {fen}")
    
    def get_bestmove(self, fen:str, time_ms:int) -> str:
        self.set_position(fen)
        self.push_cmd(f"go movetime {time_ms}")
        while True:
            line = self.engine.stdout.readline()
            if "bestmove" in line:
                return line[9:14].strip()


    def get_fen_after_move(self, fen:str, move:str) -> str:
        self.push_cmd(f"position fen {fen} moves {move}")
        self.push_cmd("d")
        while True:
            line = self.engine.stdout.readline()
            if "Fen" in line:
                return line[5:].strip()

    def get_depth_zero_eval(self, fen:str) -> float:
        self.set_position(fen)
        self.push_cmd(f"eval")
        while True:
            line = self.engine.stdout.readline()
            if "Final evaluation" in line:
                return float(line[17:28].strip())

