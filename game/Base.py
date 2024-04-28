import pygame
import random

# sourced from https://www.techwithtim.net/tutorials/game-development-with-python/tetris-pygame/tutorial-1


pygame.font.init()

# screen global var
s_width = 800
s_height = 700

# play area global var
play_width = 300
play_height = 600 
block_size = 30

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height

# Additional Game settings
look_ahead = 4 # denotes the number of pieces you can look ahead for


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

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]

# the x offset is 3 blocks except for the O piece 
shape_start = [(3,0),(3,0),(3,0),(4,0),(3,0),(3,0),(3,0)]
# index 0 - 6 represent shape


class Piece(object):
    rows = 20
    columns = 10
    def __init__(self,shape):
        index = shapes.index(shape)
        self.start_pos = shape_start[index]

        self.x = self.start_pos[0]
        self.y = self.start_pos[1]
        self.shape = shape
        self.color = shape_colors[index]
        self.rotation = 0 # 0-3 determines the rotation

    def reset_position(self):
        self.x = self.start_pos[0]
        self.y = self.start_pos[1]

# determines how to draw the grid
def create_grid(locked_positions={}):
     grid = [[(0,0,0) for _ in range(10)] for _ in range(20)]

     for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j,i) in locked_positions:
                c = locked_positions[(j,i)]
                grid[i][j] = c
     return grid

# Conver the format into game space coordinates
def convert_shape_format(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]
 
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))
    return positions

def valid_space(shape, grid):

    # check for empty spaces
    accepted_positions = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
    accepted_positions = [j for sub in accepted_positions for j in sub]
    formatted = convert_shape_format(shape)
    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False
 
    return True

# handles special instance of rotation
# in Tetr.io the frame containing the piece is shifted one right/left
# if the rotation would make a collision with the sides
# returns the x offset needed for the correction (0 if none is needed)
def wall_rotation_check(shape,grid):
    


    # left wall check
    shape.x += 1
    if valid_space(shape,grid):
        return True
    shape.x -= 1

    shape.x -= 1
    # right wall check
    if valid_space(shape,grid):
        return True
    shape.x += 1


    # need to do this for the long pieces
    # one side will protrude by 2
    shape.x += 2
    if valid_space(shape,grid):
        return True
    shape.x -= 2

    shape.x -= 2
    # right wall check
    if valid_space(shape,grid):
        return True
    shape.x += 2

    return False

def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False

def get_shape():
    global shapes, shape_colors
    return Piece(shapes[2])

def draw_text_middle(surface, text, size, color):
    font = pygame.font.SysFont("comicsans", size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (top_left_x + play_width /2 - (label.get_width()/2), top_left_y + play_height/2 - label.get_height()/2))
   
def draw_grid(surface, grid):
# This function draws the grey grid lines that we see
    sx = top_left_x
    sy = top_left_y
    for i in range(len(grid)):
        pygame.draw.line(surface, (128,128,128), (sx, sy+ i*30), (sx + play_width, sy + i * 30))  # horizontal lines
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (128,128,128), (sx + j * 30, sy), (sx + j * 30, sy + play_height))  # vertical lines

def clear_rows(grid, locked):
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
    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)
    return inc

def draw_next_shape(shapes, surface):
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Next Shapes', 1, (255,255,255))
    for ind,shape in enumerate(shapes):
        sx = top_left_x + play_width + 50
        sy = top_left_y + play_height/2 - 100 + ind*100
        format = shape.shape[0]

        for i, line in enumerate(format):
            row = list(line)
            for j, column in enumerate(row):
                if column == '0':
                    pygame.draw.rect(surface, shape.color, (sx + j*30, sy + i*30, 30, 30), 0)

    surface.blit(label, (top_left_x + play_width + 25, top_left_y + play_height/2 - 100 - 50))

def draw_hold_shape(shape, surface):
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Holding', 1, (255,255,255))
    sx = top_left_x - 150
    sy = top_left_y + play_height/2 -200
    if shape:

        format = shape.shape[0]
        for i, line in enumerate(format):
            row = list(line)
            for j, column in enumerate(row):
                if column == '0':
                    pygame.draw.rect(surface, shape.color, (sx + j*30, sy + i*30, 30, 30), 0)

    # sx = top_left_x + play_width + 25
    # sy = top_left_y + play_height/2 - 400

    # surface.blit(label, (sx + 20, sy + 160))
    surface.blit(label, (sx, top_left_y + play_height/2 - 260))


def draw_window(surface, grid, score=0, last_score = 0):
    surface.fill((0, 0, 0))

    pygame.font.init()
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('Tetris', 1, (255, 255, 255))

    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 30))

    # current score
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Score: ' + str(score), 1, (255,255,255))

    sx = top_left_x + play_width + 25
    sy = top_left_y + play_height/2 - 400

    surface.blit(label, (sx + 20, sy + 160))
    # last score
    label = font.render('High Score: ' + str(last_score), 1, (255,255,255))

    sx = top_left_x - 200
    sy = top_left_y + 200

    surface.blit(label, (sx + 20, sy + 160))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j*block_size, top_left_y + i*block_size, block_size, block_size), 0)

    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 5)

    draw_grid(surface, grid)

def main(win):
    global grid
 
    locked_positions = {}  # (x,y):(255,0,0)
    grid = create_grid(locked_positions)
    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = [get_shape() for _ in range(look_ahead)]
    hold_piece = None
    clock = pygame.time.Clock()
    fall_time = 0
    level_time = 0
    score = 0

    # can only initiate swap if a piece has been placed
    swap = False
    while run:

        level_time += clock.get_rawtime()
        if level_time/1000 > 5:
            level_time = 0
            if level_time > 0.12:
                level_time -= 0.005
        fall_speed = 0.27
        
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()
    
        # PIECE FALLING CODE
        if fall_time/1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()
 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1
 
                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                elif event.key == pygame.K_UP:
                    # rotate shape
                    current_piece.rotation = current_piece.rotation + 1 % len(current_piece.shape)
                    if not valid_space(current_piece, grid):
                        displacement = wall_rotation_check(current_piece,grid)
                        if not displacement:
                            current_piece.rotation = current_piece.rotation - 1 % len(current_piece.shape)
 
                elif event.key == pygame.K_DOWN:
                    # move shape down
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1
                if event.key == pygame.K_c and not swap:
                    # handle piece change if necessary
                    # handle the first swap
                    temp_piece = hold_piece
                    hold_piece = current_piece
                    if temp_piece is not None:
                        current_piece = temp_piece
                    else:
                        current_piece = next_piece.pop(0)
                        next_piece.append(get_shape())
                    hold_piece.reset_position() #reset to top
                    swap = True
        shape_pos = convert_shape_format(current_piece)

        # add color of piece to the grid for drawing
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1: # If we are not above the screen
                grid[y][x] = current_piece.color



        # IF PIECE HIT GROUND
        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece.pop(0)
            next_piece.append(get_shape())
            change_piece = False
            score += clear_rows(grid,locked_positions)*10
            swap = False


        draw_window(win,grid,score,0)
        draw_next_shape(next_piece, win)
        draw_hold_shape(hold_piece,win)
        pygame.display.update()
        if check_lost(locked_positions):
            draw_text_middle(win, "YOU LOST!", 80, (255,255,255))
            pygame.display.update()
            pygame.time.delay(1500)
            run = False

def main_menu(win):  # *
    run = True
    while run:
        win.fill((0,0,0))
        draw_text_middle(win, 'Press Any Key To Play', 60, (255,255,255))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main(win)

    pygame.display.quit()



win = pygame.display.set_mode((s_width, s_height))
main_menu(win)  # start game
pygame.display.set_caption('Tetris')
main()