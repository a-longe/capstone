import board

# base piece class, different piece classes will inherit from this
# make sure only functions that will be the SAME for each piece are in here
class Piece:
	def __init__(self, color:str, position:tuple[str, str]):
		self.color = color
		self.position = position

	def get_moves(self, board:Board) -> list[Board]:
		pass


class Pawn(Piece):
	def __init__(self, color:str, position:tuple[str,str]):
		Piece.__init__(self, color, position)
		self.piece_type = 'p'

	def get_moves(self, board:Board) -> list[Board]:
		pass
		

class Knight(Piece):
	def __init__(self, color:str, position:tuple[str,str]):
		Piece.__init__(self, color, position)
		self.piece_type = 'n'

	def get_moves(self, board:Board) -> list[Board]:
		pass
		

class Bishop(Piece):
	def __init__(self, color:str, position:tuple[str,str]):
		Piece.__init__(self, color, position)
		self.piece_type = 'b'

	def get_moves(self, board:Board) -> list[Board]:
		pass
		

class Rook(Piece):
	def __init__(self, color:str, position:tuple[str,str]):
		Piece.__init__(self, color, position)
		self.piece_type = 'r'

	def get_moves(self, board:Board) -> list[Board]:
		pass
		

class Queen(Piece):
	def __init__(self, color:str, position:tuple[str,str]):
		Piece.__init__(self, color, position)
		self.piece_type = 'q'

	def get_moves(self, board:Board) -> list[Board]:
		pass
		

class King(Piece):
	def __init__(self, color:str, position:tuple[str,str]):
		Piece.__init__(self, color, position)
		self.piece_type = 'k'

	def get_moves(self, board:Board) -> list[Board]:
		pass
		
