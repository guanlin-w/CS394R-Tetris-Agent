import pygame
import random

# sourced from https://www.techwithtim.net/tutorials/game-development-with-python/tetris-pygame/tutorial-1

class Piece(object):
    rows = 20
    columns = 10
    def __init__(self,shape,game):
        index = game.shapes.index(shape)
        self.start_pos = game.shape_start[index]

        self.x = self.start_pos[0]
        self.y = self.start_pos[1]
        self.shape = shape
        self.color = game.shape_colors[index]
        self.rotation = 0 # 0-3 determines the rotation

    def reset_position(self):
        self.x = self.start_pos[0]
        self.y = self.start_pos[1]
class Base():




    def __init__(self):
        pygame.font.init()
        # screen global var
        self.s_width = 800
        self.s_height = 700

        # play area global var
        self.play_width = 300
        self.play_height = 600 + 30*3 #allocate a 3 row buffer 
        self.block_size = 30

        self.top_left_x = (self.s_width - self.play_width) // 2
        self.top_left_y = self.s_height - self.play_height

        # Additional Game settings
        self.look_ahead = 4 # denotes the number of pieces you can look ahead for

        # SHAPE FORMATS

        S = [[
            '.00',
            '00.',
            '...'],
            [
            '.0.',
            '.00',
            '..0'],
            [
            '...',
            '.00',
            '00.'],
            [
            '0..',
            '00.',
            '.0.']]

        Z = [[
            '00.',
            '.00',
            '...'],
            [
            '..0',
            '.00',
            '.0.'],
            [
            '...',
            '00.',
            '.00'],
            [
            '.0.',
            '00.',
            '0..']]

        I = [
                ['....',
                '0000',
                '....',
                '....'],

                ['..0.',
                '..0.',
                '..0.',
                '..0.'],

                ['....',
                '....',
                '0000',
                '....'],

                ['.0..',
                '.0..',
                '.0..',
                '.0..']

            ]

        O = [[
            '00',
            '00'
            ]]

        J = [[
            '0..',
            '000',
            '...'],
            [
            '.00',
            '.0.',
            '.0.'],
            [
            '...',
            '000',
            '..0'],
            [
            '.0.',
            '.0.',
            '00.']]

        L = [[
            '..0',
            '000',
            '...'],
            [
            '.0.',
            '.0.',
            '.00'],
            [
            '...',
            '000',
            '0..'],
            [
            '00.',
            '.0.',
            '.0.']]

        T = [[
            '.0.',
            '000',
            '...'],
            [
            '.0.',
            '.00',
            '.0.'],
            [
            '...',
            '000',
            '.0.'],
            [
            '.0.',
            '00.',
            '.0.']]

        self.shapes = [S, Z, I, O, J, L, T]
        self.shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]

        # the x offset is 3 blocks except for the O piece 
        self.shape_start = [(3,0),(3,0),(3,0),(4,0),(3,0),(3,0),(3,0)]
        # allow for the piece to slide for 4 moves before settling on the ground
        self.settle = 4 


 

    # determines how to draw the grid
    def create_grid(self,locked_positions={}):
        grid = [[(0,0,0) for _ in range(10)] for _ in range(23)]

        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if (j,i) in locked_positions:
                    c = locked_positions[(j,i)]
                    grid[i][j] = c
        return grid

    # Conver the format into game space coordinates
    def convert_shape_format(self,shape):
        positions = []
        format = shape.shape[shape.rotation % len(shape.shape)]
    
        for i, line in enumerate(format):
            row = list(line)
            for j, column in enumerate(row):
                if column == '0':
                    positions.append((shape.x + j, shape.y + i))
        return positions

    def valid_space(self,shape,grid):

        # check for empty spaces
        accepted_positions = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20+3)]
        accepted_positions = [j for sub in accepted_positions for j in sub]
        formatted = self.convert_shape_format(shape)
        for pos in formatted:
            if pos not in accepted_positions:
                if pos[1] > -1:
                    return False
    
        return True

    # handles special instance of rotation
    # in Tetr.io the frame containing the piece is shifted one right/left
    # if the rotation would make a collision with the sides
    # returns the x offset needed for the correction (0 if none is needed)
    def wall_rotation_check(self,shape,grid):
        


        # left wall check
        shape.x += 1
        if self.valid_space(shape,grid):
            return True
        shape.x -= 1

        shape.x -= 1
        # right wall check
        if self.valid_space(shape,grid):
            return True
        shape.x += 1


        # need to do this for the long pieces
        # one side will protrude by 2
        shape.x += 2
        if self.valid_space(shape,grid):
            return True
        shape.x -= 2

        shape.x -= 2
        # right wall check
        if self.valid_space(shape,grid):
            return True
        shape.x += 2

        return False

    def check_lost(self,positions):
        for pos in positions:
            x, y = pos
            # account for buffer
            if y < 3:
                return True
        return False

    def get_shape(self):
        global shapes, shape_colors
        return Piece(random.choice(self.shapes),self)

    def draw_text_middle(self,surface, text, size, color):
        font = pygame.font.SysFont("comicsans", size, bold=True)
        label = font.render(text, 1, color)

        surface.blit(label, (self.top_left_x + self.play_width /2 - (label.get_width()/2), self.top_left_y + self.play_height/2 - label.get_height()/2))
    
    def draw_grid(self,surface, grid):
    # This function draws the grey grid lines that we see
        sx = self.top_left_x
        sy = self.top_left_y+90
        for i in range(len(grid)):
            pygame.draw.line(surface, (128,128,128), (sx, sy+ i*30), (sx + self.play_width, sy + i * 30))  # horizontal lines
            for j in range(len(grid[i])):
                pygame.draw.line(surface, (128,128,128), (sx + j * 30, sy), (sx + j * 30, sy + self.play_height))  # vertical lines

    def clear_rows(self,grid, locked):
        # need to see if row is clear the shift every other row above down one

        inc = 0
        for i in range(len(grid)-1,-1,-1):
            row = grid[i]
            if (0, 0, 0) not in row:
                inc += 1
                # add positions to remove from locked
                ind = i
                for j in range(len(row)):
                    try:
                        del locked[(j, i)]
                    except:
                        continue
        # handle row consolidation
        if inc > 0:
            for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
                x, y = key
                if y < ind:
                    newKey = (x, y + inc)
                    locked[newKey] = locked.pop(key)
        return inc


    # handle extra points for single,double,triple,quad, and full clears
    def scoring_func(self,grid,rows):
        score = 0

        match rows:
            case 1:
                score += 100
            case 2:
                score += 300
            case 3:
                score += 500
            case 4:
                score += 800
        if len(grid) == 0:
            score += 3500 
        return score



    def draw_next_shape(self,shapes, surface):
        font = pygame.font.SysFont('comicsans', 30)
        label = font.render('Next Shapes', 1, (255,255,255))
        for ind,shape in enumerate(shapes):
            sx = self.top_left_x + self.play_width + 50
            sy = self.top_left_y + self.play_height/2 - 100 + ind*100
            format = shape.shape[0]

            for i, line in enumerate(format):
                row = list(line)
                for j, column in enumerate(row):
                    if column == '0':
                        pygame.draw.rect(surface, shape.color, (sx + j*30, sy + i*30, 30, 30), 0)

        surface.blit(label, (self.top_left_x + self.play_width + 25, self.top_left_y + self.play_height/2 - 100 - 50))

    def draw_hold_shape(self,shape, surface):
        font = pygame.font.SysFont('comicsans', 30)
        label = font.render('Holding', 1, (255,255,255))
        sx = self.top_left_x - 150
        sy = self.top_left_y + self.play_height/2 -200
        if shape:

            format = shape.shape[0]
            for i, line in enumerate(format):
                row = list(line)
                for j, column in enumerate(row):
                    if column == '0':
                        pygame.draw.rect(surface, shape.color, (sx + j*30, sy + i*30, 30, 30), 0)
        surface.blit(label, (sx, self.top_left_y + self.play_height/2 - 260))


    def draw_window(self,surface, grid, score=0, last_score = 0):
        surface.fill((0, 0, 0))

        pygame.font.init()
        font = pygame.font.SysFont('comicsans', 60)
        label = font.render('Tetris', 1, (255, 255, 255))

        surface.blit(label, (self.top_left_x + self.play_width / 2 - (label.get_width() / 2), 30))

        # current score
        font = pygame.font.SysFont('comicsans', 30)
        label = font.render('Score: ' + str(score), 1, (255,255,255))

        sx = self.top_left_x + self.play_width + 25
        sy = self.top_left_y + self.play_height/2 - 400

        surface.blit(label, (sx + 20, sy + 160))
        # last score
        label = font.render('High Score: ' + str(last_score), 1, (255,255,255))

        sx = self.top_left_x - 200
        sy = self.top_left_y + 200

        surface.blit(label, (sx + 20, sy + 160))

        for i in range(len(grid)):
            for j in range(len(grid[i])):
                pygame.draw.rect(surface, grid[i][j], (self.top_left_x + j*self.block_size, self.top_left_y + i*self.block_size, self.block_size, self.block_size), 0)

        pygame.draw.rect(surface, (255, 0, 0), (self.top_left_x, self.top_left_y+90, self.play_width, self.play_height), 5)

        self.draw_grid(surface, grid)

    def main(self,win):
    
        self.locked_positions = {}  # (x,y):(255,0,0)
        self.grid = self.create_grid(self.locked_positions)
        self.change_piece = False
        self.run = True
        self.current_piece = self.get_shape()
        self.next_piece = [self.get_shape() for _ in range(self.look_ahead)]
        self.hold_piece = None
        self.clock = pygame.time.Clock()
        self.fall_time = 0
        self.level_time = 0
        self.score = 0
        # can only initiate swap if a piece has been placed
        self.swap = False
        
        # allow the pieces to be able to slide before settling
        # can only slide for self.settle per piece 
        self.onGround = False
        self.moves_slid = 0 
        while self.run:
            self.level_time += self.clock.get_rawtime()
            if self.level_time/1000 > 5:
                self.level_time = 0
                if self.level_time > 0.12:
                    self.level_time -= 0.005
            fall_speed = 0.27
            
            self.grid = self.create_grid(self.locked_positions)
            self.fall_time += self.clock.get_rawtime()
            self.clock.tick()
        
            # PIECE FALLING CODE
            if self.fall_time/1000 >= fall_speed:
                self.fall_time = 0
                self.current_piece.y += 1
                if not (self.valid_space(self.current_piece, self.grid)) and self.current_piece.y > 0:
                    self.current_piece.y -= 1
                    # we have hit a bottom collision
                    self.onGround = True

                else:
                    self.onGround = False
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                    pygame.display.quit()
                    quit()
    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.current_piece.x -= 1
                        if not self.valid_space(self.current_piece, self.grid):
                            self.current_piece.x += 1
                        elif self.onGround:
                            self.moves_slid += 1
    
                    elif event.key == pygame.K_RIGHT:
                        self.current_piece.x += 1
                        if not self.valid_space(self.current_piece, self.grid):
                            self.current_piece.x -= 1
                        elif self.onGround:
                            self.moves_slid += 1
                    elif event.key == pygame.K_UP:
                        # rotate shape
                        self.current_piece.rotation = self.current_piece.rotation + 1 % len(self.current_piece.shape)
                        if not self.valid_space(self.current_piece, self.grid):
                            displacement = self.wall_rotation_check(self.current_piece,self.grid)
                            if not displacement:
                                self.current_piece.rotation = self.current_piece.rotation - 1 % len(self.current_piece.shape)
    
                    elif event.key == pygame.K_DOWN:
                        # move shape down
                        self.current_piece.y += 1
                        if not self.valid_space(self.current_piece, self.grid):
                            self.current_piece.y -= 1
                            # instantly set the piece down
                            self.moves_slid = self.settle 
                        else:
                            self.score += 1
                    elif event.key == pygame.K_c and not self.swap:
                        # handle piece change if necessary
                        # handle the first swap
                        temp_piece = self.hold_piece
                        self.hold_piece = self.current_piece
                        if temp_piece is not None:
                            self.current_piece = temp_piece
                        else:
                            self.current_piece = self.next_piece.pop(0)
                            self.next_piece.append(self.get_shape())
                        self.hold_piece.reset_position() #reset to top
                        self.swap = True
                        self.moves_slid = 0
                        self.onGround = False
                
                    if event.key == pygame.K_SPACE:
                        # handle immediate drop
                        distance = 1
                        self.current_piece.y += 1
                        while self.valid_space(self.current_piece,self.grid):
                            self.current_piece.y += 1
                            distance += 1
                        distance -= 1
                        self.current_piece.y -= 1
                        self.score += 2*distance
                        self.change_piece = True
                        self.moves_slid = self.settle
            shape_pos = self.convert_shape_format(self.current_piece)

            # add color of piece to the grid for drawing
            for i in range(len(shape_pos)):
                x, y = shape_pos[i]
                if y > -1: # If we are not above the screen
                    self.grid[y][x] = self.current_piece.color
            if self.onGround and self.moves_slid >= self.settle:
                self.change_piece = True

            # IF PIECE HIT GROUND
            if self.change_piece:
                for pos in shape_pos:
                    p = (pos[0], pos[1])
                    self.locked_positions[p] = self.current_piece.color
                self.current_piece = self.next_piece.pop(0)
                self.next_piece.append(self.get_shape())
                self.change_piece = False

                rows_cleared = self.clear_rows(self.grid,self.locked_positions)
                self.score += self.scoring_func(self.locked_positions,rows_cleared)
                self.swap = False
                self.moves_slid = 0 


            self.draw_window(win,self.grid,self.score,0)
            self.draw_next_shape(self.next_piece, win)
            self.draw_hold_shape(self.hold_piece,win)
            pygame.display.update()
            if self.check_lost(self.locked_positions):
                self.draw_text_middle(win, "YOU LOST!", 80, (255,255,255))
                pygame.display.update()
                pygame.time.delay(1500)
                self.run = False

    def main_menu(self,win):  # *
        run = True
        while run:
            win.fill((0,0,0))
            self.draw_text_middle(win, 'Press Any Key To Play', 60, (255,255,255))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    self.main(win)

        pygame.display.quit()

    def start_game(self):
        win = pygame.display.set_mode((self.s_width, self.s_height))
        self.main_menu(win)  # start game
        pygame.display.set_caption('Tetris')



    # These functions are exclusively used for the gym env
    
    # handles the setup of the game; found at the top of the normal game entrypoint
    def setup(self):
        self.locked_positions = {}  # (x,y):(255,0,0)
        self.grid = self.create_grid(self.locked_positions)
        self.change_piece = False
        self.run = True
        self.current_piece = self.get_shape()
        self.next_piece = [self.get_shape() for _ in range(self.look_ahead)]
        self.hold_piece = None
        self.clock = pygame.time.Clock()
        self.fall_time = 0
        self.level_time = 0
        self.score = 0
        # can only initiate swap if a piece has been placed
        self.swap = False

    # manipulates the env using the action
    def action(self, action):
        return None


if __name__ == '__main__':
    game = Base()
    game.start_game()