## This file lists the different pieces of the game Hive
## Their moves will be defined in another file

class Piece():

    def __init__(self):

        self.colour = 0
        self.coords = (0, 0)
        self.symbol = None
        
    def __repr__(self):
        return self.symbol


class Queen(Piece):

    def __init__(self, colour=0):
        super(Queen, self).__init__()
        
        self.colour = colour
        self.symbol = "Q"

        
class Spider(Piece):

    def __init__(self, colour=0):
        super(Spider, self).__init__()
        
        self.colour = colour
        self.symbol = "S"


class Beetle(Piece):

    def __init__(self, colour=0):
        super(Beetle, self).__init__()
        
        self.colour = colour
        self.symbol = "B"


class Grasshopper(Piece):

    def __init__(self, colour=0):
        super(Grasshopper, self).__init__()
        
        self.colour = colour
        self.symbol = "G"


class Ant(Piece):

    def __init__(self, colour=0):
        super(Ant, self).__init__()
        
        self.colour = colour
        self.symbol = "A"



starting_pieces = {"Q" : 1,
                   "B" : 2,
                   "S" : 2,
                   "A" : 3,
                   "G" : 3}
