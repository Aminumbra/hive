import Board
import Pieces


### Todo : implement the "One-Hive Rule" -> Hive must be connex at any point

directions = {"NORTH",
              "SOUTH",
              "NORTH-WEST",
              "SOUTH-WEST",
              "NORTH-EAST",
              "SOUTH-EAST"}


# To be able to move to a certain location, a piece must be able to
# continuously go from its initial position to this location by
# "shifting" : if means that if there if a piece is fully surrounded,
# it cannot move.
# But : in case a piece is too 'large' to pass through a space let by
# 2 adjacent pieces, it cannot move this way either : to be able to "shift"
# to an adjacent cell, there must be ANOTHER free cell next to it, also
# adjacent to the initial location
# Said differently, when moving, a piece needs the width of 2 pieces to
# be able to shift in a given direction : only 1 free adjacent square is not
# wide enough for it to shift through.


#####################################################################

# First utilities functions to help us generate the moves

def slip_moves(board, i, j):
    """
    Returns a set of cells reachable in 1 move from
    (i, j) on 'board' by slipping out of this cell
    """
    moves = set()

    us = board.piece_on(i, j)

    free_adjacent_us     = board.free_adjacent_cells(i, j) #Free cells, potential moves
    occupied_adjacent_us = board.occupied_adjacent_cells(i, j)
    
    for (x, y) in free_adjacent_us:

        free_adjacent_to_nghb = board.free_adjacent_cells(x, y)

        if free_adjacent_to_nghb.intersection(free_adjacent_us): # Wide enough gap to 'slip out'
            occupied_adjacent_nghb = board.occupied_adjacent_cells(x, y)

            if occupied_adjacent_us.intersection(occupied_adjacent_nghb): # Stay in contact with the hive at any point
            
                moves.add((x, y))

    return moves


def is_connected(board):

    all_cells = board.all_cells_coord()

    start = all_cells.pop()  # Takes any cell as starting point

    reachable = set()
    reachable.add(start)
    
    done = False
    
    while not done:
        done = True

        copy_reachable = reachable.copy()
        
        for cell in reachable:

            occupied_adj = board.occupied_adjacent_cells(cell[0], cell[1])

            for x, y in occupied_adj:
                copy_reachable.add((x, y))

        done = (reachable == copy_reachable)

        reachable = reachable.union(copy_reachable)

    return (len(reachable) == len(all_cells) + 1)  #+1 as we popped the start cell at the beginning !




def play_move(board, from_cell, to_cell):

    i, j = from_cell
    x, y = to_cell
    
    p = board.board[i][j].pop()
    board.board[x][y].append(p)


#####################################################################

# Actual move generation

# A queen moves freely, but only of 1 cell

def moves_queen(board, i, j):

    moves = set()
    
    us = board.piece_on(i, j)
    assert(isinstance(us, Pieces.Queen))

    potential_moves = slip_moves(board, i, j)

    for x, y in potential_moves:

        play_move(board, (i, j), (x, y))
        if is_connected(board):
            moves.add((x, y))

        play_move(board, (x, y), (i, j))

    return moves


# A beetle moves freely of 1 cell , and can even jump on other pieces,
# regardless of their colour

def moves_beetle(board, i, j):

    moves = set()

    potential_moves = set()
    
    us = board.piece_on(i, j)
    assert(isinstance(us, Pieces.Beetle))


    adj = board.adjacent_cells(i, j)

    for d in directions:
        if adj[d]:
            potential_moves.add(adj[d])


    for x, y in potential_moves:

        play_move(board, (i, j), (x, y))
        if is_connected(board):
            moves.add((x, y))

        play_move(board, (x, y), (i, j))
        
    return moves


# Grasshoppers jump in a direction as far as they can over pieces of
# both colours, until they reach a 'free' space (over which they can't
# jump : they must stop upon reaching an empty cell).

def moves_grasshopper(board, i, j):

    moves = set()

    us = board.piece_on(i, j)
    assert(isinstance(us, Pieces.Grasshopper))
    
    for d in directions:
        x, y = i, j

        while board.piece_on(x, y):
            x, y = board.adjacent_cells(x, y)[d]

        play_move(board, (i, j), (x, y))
        if is_connected(board):
            moves.add((x, y))

        play_move(board, (x, y), (i, j))

    return moves


# Spiders move by slipping out of their cells three times in a row,
# no more no less, and without possibility of 'backtracking'.

def moves_spider(board, i, j):

    moves = set()

    us = board.piece_on(i, j)
    assert(isinstance(us, Pieces.Spider))

    paths     = [[(i, j)]]
    new_paths = []

    for k in range(3):

        for path in paths:

            x, y = path[-1]

            play_move(board, (i, j), (x, y))
            
            potential_next_pos = slip_moves(board, x, y)

            play_move(board, (x, y), (i, j))

            next_pos = set()

            # Check that the next pos are actually legal moves

            for a, b in potential_next_pos:

                play_move(board, (i, j), (a, b))

                if is_connected(board):
                    next_pos.add((a, b))

                play_move(board, (a, b), (i, j))


            next_pos = next_pos.difference(set(path)) # We can't go back !

            for next_p in next_pos:
                new_paths.append(path + [next_p])

        paths     = new_paths
        new_paths = []


    for path in paths:
        final_pos = path[-1]

        moves.add(final_pos)

    return moves


# Ants move as much as they want, but they have to respect the 'slipping' rule
def moves_ant(board, i, j):

    moves = set()

    us= board.piece_on(i, j)
    assert(isinstance(us, Pieces.Ant))

    moves     = set()
    new_moves = set()
    
    moves.add((i, j))
    new_moves.add((i, j))
    
    done = False
    
    while not done:

        moves_added_last_step = new_moves.copy()
        
        prev_len = len(moves)
        new_moves = set()
        
        for cell in moves_added_last_step:

            pot_new_moves = slip_moves(board, cell[0], cell[1])

            for x, y in pot_new_moves:
                
                play_move(board, (i, j), (x, y))
                
                if is_connected(board):
                    new_moves.add((x, y))
                    
                play_move(board, (x, y), (i, j))

        moves = moves.union(new_moves)
        new_len = len(moves)

        done = (prev_len == new_len)

    moves.remove((i, j))
        
    return moves
    


# General function :

def moves_piece(board, i, j):

    p = board.piece_on(i, j)

    if isinstance(p, Pieces.Queen):
        return moves_queen(board, i, j)

    if isinstance(p, Pieces.Spider):
        return moves_spider(board, i, j)

    if isinstance(p, Pieces.Beetle):
        return moves_beetle(board, i, j)

    if isinstance(p, Pieces.Grasshopper):
        return moves_grasshopper(board, i, j)

    if isinstance(p, Pieces.Ant):
        return moves_ant(board, i, j)

    

def place_piece(board, i, j, piece):
    """
    Returns True and updates the board 'board' if placing
    the piece 'piece' on the cell (i, j) was legal.
    Returns False and doesn't modify the board otherwise.
    """

    col = piece.colour

    assert(col == board.player)
    
    if board.piece_on(i, j):
        return False

    board.board[i][j].append(Pieces.Queen())
    connected = is_connected(board)
    board.board[i][j].pop()
    
    if not connected:
        return False

    if board.movecount > 1:

        occupied_nghb = board.occupied_adjacent_cells(i, j)

        for x, y in occupied_nghb:
            p = board.piece_on(x, y)
            if p.colour != col:
                return False

    if board.movecount == 4:
        if (colour == 0 and not board.white_queen) or (colour == 1 and not black_queen):
            return False
    
    board.board[i][j].append(piece)

    return True
