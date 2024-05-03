import pygame
import random
import numpy as np
# sourced from https://www.techwithtim.net/tutorials/game-development-with-python/tetris-pygame/tutorial-1

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

shapes = [S, Z, I, O, J, L, T]

class StateActionFeatures():
    # def in_bounds(i, j, grid):
            #     return 
    # @staticmethod
    # def bfs(i, j, grid, visited, g2h):
    #     q = list()
    #     q.append((i, j))
        
    #     found_empties = list()
    #     touched_top = False
    #     while q:
    #         e = q.pop(0)

    #         i, j = e

    #         if not (i >= 0 and i < grid.shape[0] and j >= 0 and j < grid.shape[1]):
    #             continue
    #         if i == 0:
    #             touched_top = True
    #         if grid[i][j] == 1:
    #             continue
    #         if visited[i][j] == 1:
    #             continue

    #         found_empties.append((i, j))
    #         visited[i][j] = 1
    #         q.append((i-1, j))
    #         q.append((i+1, j))
    #         q.append((i, j-1))
    #         q.append((i, j+1))

    #     if not touched_top:
    #         g2h[len(g2h)] = found_empties

    # @staticmethod
    # def get_holes(grid):
    #     group_to_holes = dict()

    #     visited = np.zeros_like(grid)

    #     for i in range(len(grid)):
    #         for j in range(len(grid[0])):
    #             StateActionFeatures.bfs(i, j, grid, visited, group_to_holes)

    #     return group_to_holes

    @staticmethod
    def get_holes(grid):
        holes = list()
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == 0:
                    isHole = False
                    for i1 in range(i, -1, -1):
                        if grid[i1, j] == 1:
                            isHole = True
                    if isHole:
                        holes.append((i, j))
        return holes

    @staticmethod
    def num_holes(grid):
        
        # g2h = StateActionFeatures.get_holes(grid)
        # n_holes = 0
        # for k in g2h:
        #     n_holes += len(g2h[k])

        holes = StateActionFeatures.get_holes(grid)
        return len(holes)

    @staticmethod
    def rows_with_holes(grid):
        # g2h = StateActionFeatures.get_holes(grid)
        # rows = set()
        # for k in g2h:
        #     v = g2h[k]
        #     for (i, j) in v:
        #         rows.add(i)

        holes = StateActionFeatures.get_holes(grid)
        rows = set()
        for (i, j) in holes:
            rows.add(i)
        return len(rows)

    def column_transitions(grid):
        n_cts = 0
        for j in range(len(grid[0])):
            if 0 != grid[0][j]:
                n_cts += 1
            for i in range(0, len(grid)-1):
                if grid[i][j] != grid[i+1][j]:
                    n_cts += 1
            if grid[-1][j] != 1:
                n_cts += 1
        return n_cts
    
    def row_transitions(grid):
        n_rts = 0
        for i in range(len(grid)):
            if 1 != grid[i][0]:
                n_rts += 1
            for j in range(0, len(grid[0])-1):
                if grid[i][j] != grid[i][j+1]:
                    n_rts += 1
            if grid[i][-1] != 1:
                n_rts += 1
        return n_rts

    def landing_height(grid, vector):
        j_box = vector[0]
        i_box = vector[1]
        
        shape = shapes[vector[2]][vector[3]]

        height = 0
        for k in range(len(shape)):
            if '0' in shape[k]:
                height += 1
        
        dists = np.zeros(len(shape[0]))
        i_g_mins = np.zeros(len(shape[0]))
        for j_rel in range(len(shape[0])):
            j = j_box + j_rel

            # for i_rel in len(shape):
            #     i = i_box + i_rel
            #     for i1 in range(i, 23):
            #         if grid[i][j] == 1:
            #             lh_bot = 23 - i
            #             break
            i_p_max = -np.inf
            for i_rel in range(len(shape)):
                i = i_box + i_rel
                if shape[i_rel][j_rel] == '0':
                    i_p_max = i
            
            i_g_min = 23
            if i_p_max != -np.inf:
                for i_g in range(len(grid)-1, i_p_max, -1):
                    if grid[i_g][j] == 1:
                        i_g_min = i_g
            
            dists[j_rel] = i_g_min - i_p_max
            i_g_mins[j_rel] = i_g_min

        j_rel_min = np.argmin(dists)
        lh = (23 - i_g_mins[j_rel_min] + 1) + height/2 - 0.5

        return lh

    def cumulative_wells(grid):
        grid_pad = np.ones((grid.shape[0], grid.shape[1]+2))
        grid_pad[:, 1:-1] = grid

        n_cwells = 0
        for i in range(len(grid_pad)):
            for j in range(1, len(grid_pad[0])-1):
                i_curr = i
                while i_curr >= 0 and grid_pad[i_curr][j] == 0 and grid_pad[i_curr][j-1] == 1 and grid_pad[i_curr][j+1] == 1:
                    i_curr -= 1
                    n_cwells += 1

        return n_cwells
    
    def eroded_piece_cells(grid):
        return 0
    
    def hole_depth(grid):
        holes = StateActionFeatures.get_holes(grid)

        j2h = dict()
        for i, j in holes:
            if j not in j2h:
                j2h[j] = list()
            j2h[j].append(i)
        
        depth = 0
        for j in j2h:
            i_max = max(j2h[j])
            for i in range(i_max-1, -1, -1):
                if grid[i][j] == 1:
                    depth += 1
        return depth
        
        

class StateActionFeatureVector():
    def __init__(self):
        self.feature_dims = 8 + 4
        self.num_actions = 6


    def feature_vector_len(self):
        return self.feature_dims * self.num_actions
    
    def __call__(self, s, done, a):
        # s
        #     self.simple_grid 
        #     self.current_piece.x
        #     self.current_piece.y
        #     self.current_piece.index
        #     self.current_piece.rotation
        #     next_pieces_ind
        #     hold_piece_ind
        #     swapped_piece
        # a (0-5)
        # print('HERE')
        # print(len(s))
        # old grid
        # print(type(s))
        # print(len(s))
        simple_grid = s[:230]
        arr_grid = simple_grid.reshape((23,10))

        vector = s[230:]
        # print('vector')
        # print(vector)

        
        n_rows_with_holes = StateActionFeatures.rows_with_holes(arr_grid)
        n_cts = StateActionFeatures.column_transitions(arr_grid)
        n_holes = StateActionFeatures.num_holes(arr_grid)
        lh = StateActionFeatures.landing_height(arr_grid, vector)
        n_cwells = StateActionFeatures.cumulative_wells(arr_grid)
        n_rts = StateActionFeatures.row_transitions(arr_grid)
        n_epcs = StateActionFeatures.eroded_piece_cells(arr_grid)
        hd = StateActionFeatures.hole_depth(arr_grid)

        state_vec = np.array([n_rows_with_holes, n_cts, n_holes, lh, n_cwells, n_rts, n_epcs, hd, vector[0], vector[1], vector[2], vector[3]])
        sa_vec = np.zeros(len(state_vec) * self.num_actions)
        sa_vec[a * len(state_vec) : (a+1) * len(state_vec)] = state_vec

        return sa_vec


class Piece(object):
    rows = 20
    columns = 10
    def __init__(self,shape,game):
        self.index = game.shapes.index(shape)
        self.start_pos = game.shape_start[self.index]

        self.x = self.start_pos[0]
        self.y = self.start_pos[1]
        self.shape = shape
        self.color = game.shape_colors[self.index]
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
        self.shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (0, 0, 255), (255, 165, 0), (192, 0, 192)]

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
        return Piece(random.choice(self.shapes),self) #Piece(self.shapes[2],self)

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
    

    def initialize_game(self):
        # moved all the initialization component of the entrypoint here
        self.locked_positions = {}  # (x,y):(255,0,0)
        self.grid = self.create_grid(self.locked_positions)
        self.change_piece = False
        self.done = False
        self.current_piece = self.get_shape()
        self.next_piece = [self.get_shape() for _ in range(self.look_ahead)]
        self.hold_piece = None
        self.clock = pygame.time.Clock()
        self.fall_time = 0
        self.level_time = 0
        self.score = 0

        self.lost = False
        # can only initiate swap if a piece has been placed
        self.swap = False
        
        # allow the pieces to be able to slide before settling
        # can only slide for self.settle per piece 
        self.onGround = False
        self.moves_slid = 0 

    def main(self):
        
        while not self.done:
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
                    self.done = True
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
                        self.current_piece.rotation = (self.current_piece.rotation + 1) % len(self.current_piece.shape)
                        if not self.valid_space(self.current_piece, self.grid):
                            displacement = self.wall_rotation_check(self.current_piece,self.grid)
                            if not displacement:
                                self.current_piece.rotation = (self.current_piece.rotation - 1) % len(self.current_piece.shape)
    
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

            
            # another check to see if we're still on the ground
            self.current_piece.y += 1
            if not (self.valid_space(self.current_piece, self.grid)) and self.current_piece.y > 0:

                # we have hit a bottom collision
                self.onGround = True
            else:
                self.onGround = False
            self.current_piece.y -= 1

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

            self.evaluateBoard()


            self.draw_window(self.win,self.grid,self.score,0)
            self.draw_next_shape(self.next_piece,self.win)
            self.draw_hold_shape(self.hold_piece,self.win)
            if self.lost:
                self.draw_text_middle(self.win, "YOU LOST!", 80, (255,255,255))
                pygame.display.update()
                pygame.time.delay(1500)
            else:
                pygame.display.update()
            
    
    def evaluateBoard(self):
        # evaluate the board to see if we have won or loss
        # in this case, this only checks if the player has lost
        if self.check_lost(self.locked_positions):
                #pygame.display.update()
                self.done = True
                self.lost = True


    def main_menu(self):  # *
        run = True
        while run:
            self.win.fill((0,0,0))
            self.draw_text_middle(self.win, 'Press Any Key To Play', 60, (255,255,255))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    self.initialize_game()
                    self.main()

        pygame.display.quit()

    def start_game(self):
        self.win = pygame.display.set_mode((self.s_width, self.s_height))
        self.main_menu()  # start game
        pygame.display.set_caption('Tetris')



    # These functions are exclusively used for the gym env
    
    # handles the setup of the game; found at the top of the normal game entrypoint
    def setup(self):
        self.locked_positions = {}  # (x,y):(255,0,0)
        self.grid = []
        self.simple_grid = []
        # populates both grid and simple_grid
        self.create_grid(self.locked_positions)
        self.create_simple_grid(self.locked_positions)
        self.change_piece = False
        self.done = False
        self.current_piece = self.get_shape()
        self.next_piece = [self.get_shape() for _ in range(self.look_ahead)]
        self.hold_piece = None
        self.clock = pygame.time.Clock()
        self.fall_time = 0
        self.level_time = 0
        self.score = 0
        # can only initiate swap if a piece has been placed
        self.swap = False
        
        self.lost = False
        # exclusive to the gym env
        self.current_piece_format = self.convert_shape_format(self.current_piece)
        self.onGround = False
        self.moves_slid = 0
        self.done = False
        self.win = pygame.display.set_mode((self.s_width, self.s_height))
        pygame.display.set_caption('Tetris')
        
        # return the initial start state
        # State includes the following:
        # grid
        # the current piece (x,y) of the bounding box. The current shape index and the rotation index
        # the list of the next 4 pieces (in terms of index in the shapes list)
        # the hold piece index - index of 7 for no pieces
        # number to see if the player has already swapped (true = 1)
        next_pieces_ind = [x.index for x in self.next_piece]
        hold_piece_ind = 7


        #  3, 0, 5, 0, 1, 1, 1, 2, 7, 0
        #  10 23  7  4 7  7  7  7  8  2
        #  3, 0, 0, 0, 4, 6, 3, 0, 7, 0]
        s = np.array(self.simple_grid + [self.current_piece.x,self.current_piece.y,self.current_piece.index, self.current_piece.rotation] + next_pieces_ind + [hold_piece_ind,0])
        
        X = StateActionFeatureVector()
        x = X(s, False, 5)
        new_s = {'vector': s[230:], 'grid': s[:230].reshape((23,10))}
        return x


    # manipulates the env using the action
    def action(self, action):
        # 0 - Left
        # 1 - Right
        # 2 - Up (rotate)
        # 3 - Down
        # 4 - C (swap)
        # 5 - space
        self.grid = self.create_grid(self.locked_positions)
        match action:
            case 0:
                # L
                self.current_piece.x -= 1
                if not self.valid_space(self.current_piece, self.grid):
                    self.current_piece.x += 1
                elif self.onGround:
                    self.moves_slid += 1
            case 1:
                # R
                self.current_piece.x += 1
                if not self.valid_space(self.current_piece, self.grid):
                    self.current_piece.x -= 1
                elif self.onGround:
                    self.moves_slid += 1
            case 2:
                # rotate shape
                self.current_piece.rotation = (self.current_piece.rotation + 1) % len(self.current_piece.shape)
                if not self.valid_space(self.current_piece, self.grid):
                    displacement = self.wall_rotation_check(self.current_piece,self.grid)
                    if not displacement:
                        self.current_piece.rotation = (self.current_piece.rotation - 1) % len(self.current_piece.shape)

            case 3:
                # move shape down
                self.current_piece.y += 1
                if not self.valid_space(self.current_piece, self.grid):
                    self.current_piece.y -= 1
                    # instantly set the piece down
                    if not self.onGround:
                        self.onGround = True
                    else:
                        self.moves_slid = self.settle 
                # else:
                #     self.score += 1
            case 4:
                if self.swap:
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
    
            case 5:
                # handle immediate drop
                distance = 1
                self.current_piece.y += 1
                while self.valid_space(self.current_piece,self.grid):
                    self.current_piece.y += 1
                    distance += 1
                distance -= 1
                self.current_piece.y -= 1
                #self.score += 2*distance
                self.change_piece = True
                self.moves_slid = self.settle
            
            
        # update the format of the piece    
        self.current_piece_format = self.convert_shape_format(self.current_piece)

         # add color of piece to the grid for drawing
        for i in range(len(self.current_piece_format)):
            x, y = self.current_piece_format[i]
            if y > -1: # If we are not above the screen
                self.grid[y][x] = self.current_piece.color

        if self.onGround and self.moves_slid >= self.settle:
            self.change_piece = True

        # IF PIECE HIT GROUND
        if self.change_piece:
            for pos in self.current_piece_format:
                p = (pos[0], pos[1])
                self.locked_positions[p] = self.current_piece.color
            self.current_piece = self.next_piece.pop(0)
            self.next_piece.append(self.get_shape())
            self.change_piece = False

            rows_cleared = self.clear_rows(self.grid,self.locked_positions)
            self.score += self.scoring_func(self.locked_positions,rows_cleared)
            self.swap = False
            self.moves_slid = 0 
            self.onGround = False
        
        self.evaluateBoard()


        next_pieces_ind = [x.index for x in self.next_piece]
        hold_piece_ind = 7 if self.hold_piece is None else self.hold_piece.index
        
        swapped_piece = 1 if self.swap else 0
        # TODO handle the reward function
        # Will depend on the environment i.e 40 lines vs 2 min blitz
        self.create_simple_grid(self.locked_positions)

        
        s, r, isdone, b, d = np.array(self.simple_grid + [self.current_piece.x,self.current_piece.y,self.current_piece.index, self.current_piece.rotation] + next_pieces_ind + [hold_piece_ind,swapped_piece]), self.reward_function(), self.done,False,{}
        
        X = StateActionFeatureVector()
        x = X(s, isdone, action)
        # print(x)
        
        new_s = {'vector': s[230:], 'grid': s[:230].reshape((23,10))}
        return x, r, isdone, b, d
    
    def reward_function(self):
        return 0

    def render(self):
        self.draw_window(self.win,self.grid,self.score,0)
        self.draw_next_shape(self.next_piece, self.win)
        self.draw_hold_shape(self.hold_piece,self.win)
        if self.lost:
            self.draw_text_middle(self.win, "YOU LOST!", 80, (255,255,255))
            pygame.display.update()
            pygame.time.delay(1500)
        else:
            pygame.display.update()

    # same logic as create grid but also populates the simple grid as well
    def create_simple_grid(self,locked_positions={}):
        #self.grid = [[(0,0,0) for _ in range(10)] for _ in range(23)]
        self.simple_grid = []
        for i in range(23):
            for j in range(10):
                if (j,i) in locked_positions:
                    #c = locked_positions[(j,i)]
                    #self.grid[i][j] = c
                    self.simple_grid.append(1)
                else:
                    self.simple_grid.append(0)
    def close(self):
        if self.win is not None:
            pygame.display.quit()
            pygame.quit()
            
# if __name__ == '__main__':
#     game = Base()
#     game.start_game()