import piece

row_index_to_legend = {
	0:8,
	1:7,
	2:6,
	3:5,
	4:4,
	5:3,
	6:2,
	7:1
}

row_legend_to_index = {(v,k) for (k,v) in row_index_to_legend.items()}

column_index_to_letter = {
	0: 'a',
	1: 'b',
	2: 'c',
	3: 'd',
	4: 'e',
	5: 'f',
	6: 'g',
	7: 'h'
}

def get_piece_obj(piece_type:str, color:str, position:str):
    """
    piece type: char('b', 'n', 'r', 'p', 'q', 'k')
    color: char('w', 'b')
    location: str(ex. 'b5')
    """
    match piece_type:
        case 'p': return piece.Pawn(color, position)
        case 'b': return piece.Bishop(color, position)
        case 'n': return piece.Knight(color, position)
        case 'r': return piece.Rook(color, position)
        case 'q': return piece.Queen(color, position)
        case 'k': return piece.King(color, position)