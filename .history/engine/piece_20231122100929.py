from board import Board

def get_piece_obj(piece_type:str, color:str, position:tuple[str, str]):
    """
    piece type: char('b', 'n', 'r', 'p', 'q', 'k')
    color: char('w', 'b')
    location: str(ex. 'b5')
    """
    match piece_type:
        case 'p': return Pawn(color, position)
        case 'b': return Bishop(color, position)
        case 'n': return Knight(color, position)
        case 'r': return Rook(color, position)
        case 'q': return Queen(color, position)
        case 'k': return King(color, position)

# base piece class, different piece classes will inherit from this
# make sure only functions that will be the SAME for each piece are in here
class Piece:
	def __init__(self, color:str, position:tuple[str, str]):
		self.color = color
		self.position = position

	def get_moves(self, board) -> list: # type board, circular import
		pass


class Pawn(Piece):
	def __init__(self, color:str, position:tuple[str,str]):
		Piece.__init__(self, color, position)
		self.piece_type = 'p'

	def get_moves(self, board) -> list: # type board, circular import
		pass
		

class Knight(Piece):
	def __init__(self, color:str, position:tuple[str,str]):
		Piece.__init__(self, color, position)
		self.piece_type = 'n'

	def get_moves(self, board) -> list: # type board, circular import
		pass
		

class Bishop(Piece):
	def __init__(self, color:str, position:tuple[str,str]):
		Piece.__init__(self, color, position)
		self.piece_type = 'b'

	def get_moves(self, board) -> list: # type board, circular import
		pass
		

class Rook(Piece):
	def __init__(self, color:str, position:tuple[str,str]):
		Piece.__init__(self, color, position)
		self.piece_type = 'r'

	def get_moves(self, board) -> list: # type board, circular import
		pass
		

class Queen(Piece):
	def __init__(self, color:str, position:tuple[str,str]):
		Piece.__init__(self, color, position)
		self.piece_type = 'q'

	def get_moves(self, board) -> list: # type board, circular import
		pass
		

class King(Piece):
	def __init__(self, color:str, position:tuple[str,str]):
		Piece.__init__(self, color, position)
		self.piece_type = 'k'

	def get_moves(self, board) -> list: # type board, circular import
		pass
		