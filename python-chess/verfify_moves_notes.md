## Board Repersentation

- I really like the idea of denser bitboards
- the 'denser' part comes from instead of using arrays for each type of piece (w. pawn, b. pawn, w. rook, ect.) using less 'boards' by combining them and comparing to find the individual boards (w. pieces, rooks, pawns, ect.)
- While not nessisary for the original use of this project (verfiying moves)
- when we transition to building a chess engine this board repersentation already being used will greatly help us

## Verfiy Moves

### Pawn
- Determine what colour pawn it is
  - white moves in one direction and black will move in the other
- Can always move foreward unless there is ANY piece in front
- Can move diagonally if there is an enemy piece there or if there is a en passant target there (found in fen string)
  - might need to check if pawn in on edge row for out of range errors
- organization might look like this
  ```
    if colour = white:
        if row = 1:
            movement += north * 2
        # check if enemy piece or en passant target is ne or nw
          # if so add those movements
        movement += north
    else:
        if row = 6:
            movement += south * 2
        # check if enemy piece or en passant target is se or sw
          # if so add those movements
        movement += south

    if column = 0:
        # remove movement from column to left
    elif column = 7:
        # remove movement from column to right

    
    # compare movement array to friendly_pieces array and enemy_pieces array to find indexes of possible moves

    # use function that turns those coordinates into a string that can be fed into a program using the UCI
 
 - 
