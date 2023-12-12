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

def get_piece_obj(piece_type:str, color:str, location:str):
    """
    piece type: char(b, n, r, p, q, k)
    color: char('w', 'b')
    location: str(ex. b5)
    """