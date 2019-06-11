## This file contains an implementation of an hexagonal Board,
## used to play Hive.
## Each cell can be either empty, or contain one or several pieces
## (Beetles can jump on top of other pieces)
#
## Form of the board :
#
# +-----+     +-----+     |
# |     |     |     |     |
# | 0,0 +-----+ 0,2 +-----+
# |     |     |     |     |
# +-----+ 0,1 +-----+ 0,3 +
# |     |     |     |     |
# | 1,0 +-----+ 1,2 +-----+
# |     |     |     |     |
# +-----+ 1,1 +-----+ 1,3 +
# |     |     |     |     |
# | 2,0 +-----+ 2,2 +-----+
# |     |     |     |     |
# +-----+ 2,1 +-----+ 2,3 +
# |     |     |     |     |


class Board():

    def __init__(self):

        ## The game contains up to 50 pieces
        ## Therefore, we must account for the possibility of forming
        ## a chain of length 25 in any direction
        ## We pre-allocate a large empty board instead of dealing with
        ## a data structure of variable size
        
        self.__width  = 51
        self.__height = 51

        # With the Beetle mechanic, each position can be occupied by several pieces
        # Therefore, we use lists to represent the pieces at each cell
        self.board    = [[[] for i in range(self.__width)] for j in range(self.__height)]
        self.center   = (26, 26)

        # To visualize or compute things, it might be useful to remember
        # where are the rightmost, leftmost ... pieces on the board.
        # TODO : actually use it
        self.left     = 0
        self.right    = 51
        self.top      = 0
        self.bot      = 51

        # Some rules need to now the current move
        self.moves    = 1
        self.player   = 0

        # Some rules need to know which Queens are already on the board
        self.white_queen = False
        self.black_queen = False


    ##############################################################

    ## Useful functions

    def all_pieces_on(self, i, j):
        return self.board[i][j] 

    def piece_on(self, i, j):

        P = self.all_pieces_on(i, j)

        if P:
            return P[-1]
        else:
            return None
            
    
    def cells_of_colour(self, colour):
        """
        Returns a set with all the cells that 'belong' to a
        given player.
        If a beetle is on top of a stack of pieces, the cell's
        colour is the beetle's colour.
        """

        cells = set()
        
        for i in range(self.top, self.bot):
            for j in range(self.left, self.right):

                p = self.piece_on(i, j)

                if p and p.colour == colour:
                    cells.add((i, j))

        return cells



    def all_cells_coord(self):
        
        cells = set()

        for i in range(self.top, self.bot):
            for j in range(self.left, self.right):

                p = self.piece_on(i, j)

                if p:
                    cells.add((i, j))

        return cells

    

    def adjacent_cells(self, i, j):

        """
        Returns a dictionnary, corresponding to the neighbours of the
        square (i, j).
        If the square is one of the 'border' square, the corresponding
        tuple is 'None'.
        """

        neighbours = dict()

        # South and North neighbours do not depend on (i, j)
        neighbours["SOUTH"] = (i+1, j)
        neighbours["NORTH"] = (i-1, j)

        if j % 2 == 0:
            neighbours["NORTH-WEST"] = (i-1, j-1)
            neighbours["SOUTH-WEST"] = (i  , j-1)
            neighbours["NORTH-EAST"] = (i-1, j+1)
            neighbours["SOUTH-EAST"] = (i  , j+1)

        else: # j % 2 == 1
            neighbours["NORTH-WEST"] = (i  , j-1)
            neighbours["SOUTH-WEST"] = (i+1, j-1)
            neighbours["NORTH-EAST"] = (i  , j+1) 
            neighbours["SOUTH-EAST"] = (i+1, j+1)


        for direction in neighbours:
            i, j = neighbours[direction]

            if (   i < 0
                or i > self.__height
                or j < 0
                or j > self.__width):

                neighbours[direction] = None

        return neighbours


    def free_adjacent_cells(self, i, j):

        cells = set()
        
        adj = self.adjacent_cells(i, j)
        
        for d in adj:
            x, y = adj[d]
            
            if not self.piece_on(x, y):
                cells.add((x, y))

        return cells


    def occupied_adjactent_cells(self, i, j):

        cells = set()

        adj = self.adjacent_cells(i, j)
        
        for d in adj:
            x, y = adj[d]
            
            if self.piece_on(x, y):
                cells.add((x, y))

        return cells


    def spawn_cells_for_colour(self, colour):
        """
        Returns a set of all the cells where a given player can
        directly place its own pieces.
        Rule : when placed, a piece must be adjacent to at least
        another piece, and must only be adjacent to allied pieces.
        """

        allied_adjacent = cells_of_colour(colour)
        ennemy_adjacent = cells_of_colour(1-colour)

        return allied_adjacent.difference(ennemy_adjacent)


    #####################################################################


