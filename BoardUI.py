# A class to visualize a board !

import pygame, math

LIGHT_BLUE   = [153, 153, 255]
LIGHT_YELLOW = [255, 255, 170]
BLACK        = [0, 0, 0]
WHITE        = [255, 255, 255]
BROWN        = [153, 76, 30]


class Cell(pygame.sprite.Sprite):
    def __init__(self, radius=26, piece=None, colour=0):
        super().__init__()

        self.image = pygame.Surface([2 * radius, 2 * radius])
        self.image.fill(BROWN)

        

class BoardUI():
    
    def __init__(self, board):

        self.board = board

        # Screen to visualize the game
        self.screen   = pygame.display.set_mode([1400, 1000], pygame.RESIZABLE)
        self.font     = None
        self.offset   = [0, 0]
        
        self.start_renderer()
            
    def start_renderer(self):
        pygame.font.init()
        self.font = pygame.font.SysFont('Comic Sans MS', 12)
        
        pygame.display.set_caption("Hive game")

        self.screen.fill(BROWN)

        self.update()



    def manage_events(self):

        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    return


    def coord_to_screen(self, x, y, ratio, offset=[0, 0]):

        # Horizontal coordinate : same formula regardless of the cell

        new_y = math.sqrt(3) * ratio * y + ratio  # The final '+' is an offset to see the (0, 0) cell
        
        # Vertical coordinate : depends on the current column

        new_x = 2 * ratio * x

        if y % 2 == 1:
            new_x += ratio


        # Compute offset, in case of scrolling :

        new_x += offset[0]
        new_y += offset[1]

        return new_y, new_x


    def draw_hexagon_(self, x, y, radius=26, line_colour=BLACK, fill=True, fill_colour=[LIGHT_BLUE, LIGHT_YELLOW], player_colour=0):

        # Adds an hexagonal surface, centered on (x, y), of colour 'colour',
        # and of radius 'radius', on the main window.
        # Need to get the coordinates of the 6 points : trigonometry !

        points = []

        new_x, new_y = x, y

        for i in range(6):
            new_x = x + radius * math.cos(2 * math.pi * i / 6)
            new_y = y + radius * math.sin(2 * math.pi * i / 6)

            points.append([new_x, new_y])

        pygame.draw.polygon(self.screen, line_colour, points, 3)

        if fill:
            pygame.draw.polygon(self.screen, fill_colour[player_colour], points, 0)


    def draw_piece(self, p, x, y, radius=26, ratio=None, offset=[0, 0]):

        if not ratio:
            ratio = radius + 1

        new_y, new_x = self.coord_to_screen(x, y, ratio, offset)

        self.draw_hexagon_(new_y, new_x, radius, player_colour=p.colour)
        letter = self.font.render(p.symbol, True, (0,0,0))
        letter_rect = letter.get_rect(center=(new_y, new_x))
        self.screen.blit(letter, letter_rect)


    def render_moves(self, moves, radius=26, offset = [0, 0], line_colour=WHITE):

        ratio = radius + 1

        for x, y in moves:

            new_y, new_x = self.coord_to_screen(x, y, ratio, offset)

            self.draw_hexagon_(new_y, new_x, line_colour=line_colour, fill=False)

        self.update()
        
            
        
    def render(self, radius=26, offset=[0, 0]):
        
        for x in range(self.board.top, self.board.bot):
            for y in range(self.board.left, self.board.right):

                p = self.board.piece_on(x, y)

                if p:
                    self.draw_piece(p, x, y, radius)
                    

        self.update()


    def update(self):
        pygame.display.update()
