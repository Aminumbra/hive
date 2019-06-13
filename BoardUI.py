# A class to visualize a board !

import pygame, math
import Moves
import Pieces

LIGHT_BLUE   = [153, 153, 255]
LIGHT_YELLOW = [255, 255, 170]
BLACK        = [0, 0, 0]
WHITE        = [255, 255, 255]
BROWN        = [153, 76, 30]


class Cell(pygame.sprite.Sprite):
    def __init__(self, radius=26, font=None, piece=None):
        super().__init__()

        self.piece = piece
        self.image = pygame.Surface([2 * radius, 2 * radius])
        self.image.fill(BROWN)

        self.board_x = 0
        self.board_y = 0

        self.radius = radius
        
        self.rect  = self.image.get_rect()
        self.font  = font
        self.image.set_colorkey(BROWN)

        if piece:
            self.draw_cell(x=radius, y=radius, player_colour=piece.colour)
            letter = self.font.render(piece.symbol, True, (0,0,0))
            letter_rect = letter.get_rect(center=(radius, radius))
            self.image.blit(letter, letter_rect)

        else:
            self.draw_cell(x=radius, y=radius, line_colour = WHITE, fill=False)


    def draw_cell(self, x, y, line_colour=BLACK, fill=True, fill_colour=[LIGHT_YELLOW, LIGHT_BLUE], player_colour=0):

        # Adds an hexagonal surface, centered on (x, y), of colour 'colour',
        # and of radius 'radius', on the main window.
        # Need to get the coordinates of the 6 points : trigonometry !

        points = []

        new_x, new_y = x, y

        for i in range(6):
            new_x = x + self.radius * math.cos(2 * math.pi * i / 6)
            new_y = y + self.radius * math.sin(2 * math.pi * i / 6)

            points.append([new_x, new_y])

        pygame.draw.polygon(self.image, line_colour, points, 3)

        if fill:
            pygame.draw.polygon(self.image, fill_colour[player_colour], points, 0)


    def draw(self, screen):
        screen.blit(self.image, self.rect)

        

class BoardUI():
    
    def __init__(self, board, radius=26, offset=[0, 0]):

        self.board    = board

        self.radius   = radius
        self.offset   = offset

        # Screen to visualize the game
        self.screen   = pygame.display.set_mode([1400, 1000], pygame.RESIZABLE)
        self.font     = None
        self.offset   = [0, 0]

        self.cell_list = pygame.sprite.Group()
        self.selected_cell = None

        self.start_renderer()


    ################

    # Technical functions to manage the events
        
    def start_renderer(self):
        pygame.font.init()
        pygame.init()

        self.font = pygame.font.SysFont('Comic Sans MS', 12)
        self.menu_font = pygame.font.SysFont('Arial', 24)
        
        pygame.display.set_caption("Hive game")

        self.screen.fill(BROWN)

        self.update()


    def manage_all_events(self):

        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    return
                
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1: # Select or move a piece

                    if self.selected_cell:
                        
                        self.move_piece_event(event)
                        
                    else:
                        self.select_piece_event(event)


                elif event.type == pygame.MOUSEBUTTONUP and event.button == 3: # Add a piece

                    self.place_piece_event(event)
                    
                    

    def move_piece_event(self, event):
        x, y      = event.pos
        to_cell   = self.screen_to_coord(x, y)
        from_cell = (self.selected_cell.board_x, self.selected_cell.board_y)

        Moves.play_legal_move(self.board, from_cell, to_cell)
        
        self.selected_cell = None
        self.render()
        

    def select_piece_event(self, event):
        for cell in self.cell_list:
            
            if cell.rect.collidepoint(event.pos):
                                
                x, y = cell.board_x, cell.board_y

                piece = self.board.piece_on(x, y)

                if piece.colour == self.board.player:
                    self.selected_cell = cell
                    moves = Moves.moves_piece(self.board, x, y)
                    self.render_moves(moves)
                
                break
            

    def place_piece_event(self, event):

        pos_x, pos_y = event.pos
        
        x, y = self.screen_to_coord(pos_x, pos_y)
        colour = self.board.player
                    
        new_event = pygame.event.wait()

        if new_event.type == pygame.KEYDOWN:
            key   = new_event.key
            piece = None

            if key == ord("a"):
                piece = Pieces.Ant(colour)

            elif key == ord("q"):
                piece = Pieces.Queen(colour)

            elif key == ord("b"):
                piece = Pieces.Beetle(colour)

            elif key == ord("g"):
                piece = Pieces.Grasshopper(colour)

            elif key == ord("s"):
                piece = Pieces.Spider(colour)
                        
            if piece:
                Moves.place_piece(self.board, x, y, piece)
                self.render()


    def wait_for_move(self):

        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    return
                
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1: # Select or move a piece

                    if self.selected_cell:
                        
                        self.move_piece_event(event)
                        
                    else:
                        self.select_piece_event(event)

                    return


                elif event.type == pygame.MOUSEBUTTONUP and event.button == 3: # Add a piece

                    self.place_piece_event(event)
                    return

                    


    ##################

    # Visualization function

    def coord_to_screen(self, x, y):

        # Horizontal coordinate : same formula regardless of the cell

        ratio  = self.radius + 1
        offset = self.offset

        new_y = math.sqrt(3) * ratio * y + ratio  # The final '+' is an offset to see the (0, 0) cell
        
        # Vertical coordinate : depends on the current column

        new_x = 2 * ratio * x

        if y % 2 == 1:
            new_x += ratio


        # Compute offset, in case of scrolling :

        new_x += offset[0]
        new_y += offset[1]

        return new_y, new_x


    def screen_to_coord(self, x, y):
        # Inverse operation : gets a (x, y) point on screen, return the corresponding
        # board cell coordinates
        # TODO : CLEVER THINGS !

        radius, offset = self.radius + 1, self.offset

        for i in range(0, self.board.height()):
            for j in range(0, self.board.width()):

                virtual_cell = Cell()
                v_y, v_x = self.coord_to_screen(i, j)
                virtual_cell.rect.center = (v_y, v_x)
                
                if virtual_cell.rect.collidepoint(x, y):
                    return (i, j)
                    


    def draw_hexagon_(self, x, y, line_colour=BLACK, fill=True, fill_colour=[LIGHT_YELLOW, LIGHT_BLUE], player_colour=0):

        # Adds an hexagonal surface, centered on (x, y), of colour 'colour',
        # and of radius 'radius', on the main window.
        # Need to get the coordinates of the 6 points : trigonometry !

        points = []
        radius = self.radius

        new_x, new_y = x, y

        for i in range(6):
            new_x = x + radius * math.cos(2 * math.pi * i / 6)
            new_y = y + radius * math.sin(2 * math.pi * i / 6)

            points.append([new_x, new_y])

        pygame.draw.polygon(self.screen, line_colour, points, 3)

        if fill:
            pygame.draw.polygon(self.screen, fill_colour[player_colour], points, 0)

            


    def draw_piece(self, p, x, y):

        radius = self.radius
        ratio  = radius + 1
        
        new_y, new_x = self.coord_to_screen(x, y)

        self.draw_hexagon_(new_y, new_x, player_colour=p.colour)
        
        letter = self.font.render(p.symbol, True, (0,0,0))
        letter_rect = letter.get_rect(center=(new_y, new_x))
        self.screen.blit(letter, letter_rect)


        

    def get_cells_sprite(self):

        for x in range(self.board.top, self.board.bot):
            for y in range(self.board.left, self.board.right):

                p = self.board.piece_on(x, y)

                if p:
                    cell = Cell(radius=self.radius, font=self.font, piece=p)
                    self.cell_list.add(cell)
                    
        

                    
    def render_moves(self, moves, line_colour=WHITE):

        for x, y in moves:

            new_y, new_x = self.coord_to_screen(x, y)

            cell_move = Cell(radius=self.radius)
            cell_move.rect.center = (new_y, new_x)
            cell_move.draw(self.screen)

        self.update()
        
            
        
    def render(self):

        self.screen.fill(BROWN)
        
        for x in range(self.board.top, self.board.bot):
            for y in range(self.board.left, self.board.right):

                p = self.board.piece_on(x, y)

                if p:

                    ### TODO : implement other things so sprite are added ON CREATION, not on rendering
                    # and so they ALREADY have a correct rect.x, rect.y
                    
                    cell = Cell(radius=self.radius, font=self.font, piece=p)
                    cell.board_x = x
                    cell.board_y = y
                    
                    self.cell_list.add(cell)
                    
                    new_y, new_x = self.coord_to_screen(x, y)
                    cell.rect.center = (new_y, new_x)
                    cell.draw(self.screen)


        player_colour_str  = "Player " + str(self.board.player + 1)
        player_colour      = self.menu_font.render(player_colour_str, True, WHITE)
        player_colour_rect = player_colour.get_rect(topleft=(100, 100))
        self.screen.blit(player_colour, player_colour_rect)

        movecount_str      = "Move number " + str(self.board.movecount)
        movecount          = self.menu_font.render(movecount_str, True, WHITE)
        movecount_rect     = movecount.get_rect(topleft=(100, 150))
        self.screen.blit(movecount, movecount_rect)
        
        self.update()


    def render_endgame(self, winner):

        self.render()

        message_str         = "Player " + str(winner + 1) + " has won the game !"
        message_colour      = self.menu_font.render(message_str, True, WHITE)
        message_colour_rect = message_colour.get_rect(center=(self.screen.get_width() // 2, 50))
        self.screen.blit(message_colour, message_colour_rect)

        self.update()


    def update(self):
        pygame.display.update()
