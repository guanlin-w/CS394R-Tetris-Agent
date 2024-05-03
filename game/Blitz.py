from game import Base
import pygame
import numpy as np
# 2 minute blitz
class Blitz(Base):
    def __init__(self):
        super().__init__()
        
        # limit the number of actions that can occur
        # for the interactive mode with gravity, one gravity tick counts as an action
        self.action_limit = 2000
        self.action_count = 0
        self.prev_score = 0
        self.prev_num_holes = 0
        self.prev_bumpiness = 0
        self.won = False

        self.max_height = 0
    
    def initialize_game(self):
        super().initialize_game()
        self.action_count = 0
        self.action_limit = 2000
        self.action_count = 0
        self.prev_score = 0
        self.prev_num_holes = 0
        self.prev_bumpiness = 0
        self.won = False

        self.max_height = 0
    # same main logic except it tracks the number of actions taken
    # actions include any of the key presses (and gravity for the interactive mode)
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
                self.action_count += 1
                if not (self.valid_space(self.current_piece, self.grid)) and self.current_piece.y > 0:
                    self.current_piece.y -= 1
                    self.action_count -= 1
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
                        self.action_count += 1
                        if not self.valid_space(self.current_piece, self.grid):
                            self.action_count -= 1
                            self.current_piece.x += 1
                        elif self.onGround:
                            self.moves_slid += 1
    
                    elif event.key == pygame.K_RIGHT:
                        self.current_piece.x += 1
                        self.action_count += 1
                        if not self.valid_space(self.current_piece, self.grid):
                            self.action_count -= 1
                            self.current_piece.x -= 1
                        elif self.onGround:
                            self.moves_slid += 1
                    elif event.key == pygame.K_UP:
                        # rotate shape
                        self.current_piece.rotation = self.current_piece.rotation + 1 % len(self.current_piece.shape)
                        #self.action_count += 1
                        if not self.valid_space(self.current_piece, self.grid):
                            #self.action_count -= 1
                            displacement = self.wall_rotation_check(self.current_piece,self.grid)
                            if not displacement:
                                self.current_piece.rotation = self.current_piece.rotation - 1 % len(self.current_piece.shape)
    
                    elif event.key == pygame.K_DOWN:
                        # move shape down
                        self.current_piece.y += 1
                        self.action_count += 1
                        if not self.valid_space(self.current_piece, self.grid):
                            self.action_count -= 1
                            self.current_piece.y -= 1
                            # instantly set the piece down
                            self.moves_slid = self.settle 
                        # else:
                        #     self.score += 1
                    elif event.key == pygame.K_c and not self.swap:
                        # handle piece change if necessary
                        # handle the first swap
                        self.action_count += 1
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
                        self.action_count += 1
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
            if self.lost or self.won:
                self.draw_text_middle(self.win, f'Final Score {self.score}', 80, (255,255,255))
                pygame.display.update()
                pygame.time.delay(1500)
            else:
                pygame.display.update()
                #pygame.time.delay(1500)





    # override to update the win condition
    def evaluateBoard(self):
        # evaluate the board to see if we have won or loss
        # in this case, check if we have lost or have reached 40 lines
        if self.check_lost(self.locked_positions):
            self.done = True
            self.lost  =True

        # new component here
        if self.action_count >= self.action_limit:
            self.done = True
            self.lost = True # not really a lost but we're done

    # override to output the number of lines cleared instead of the score
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
        label = font.render('Actions: ' + str(self.action_count), 1, (255,255,255))

        sx = self.top_left_x - 200
        sy = self.top_left_y + 200

        surface.blit(label, (sx + 20, sy + 160))

        for i in range(len(grid)):
            for j in range(len(grid[i])):
                pygame.draw.rect(surface, grid[i][j], (self.top_left_x + j*self.block_size, self.top_left_y + i*self.block_size, self.block_size, self.block_size), 0)

        pygame.draw.rect(surface, (255, 0, 0), (self.top_left_x, self.top_left_y+90, self.play_width, self.play_height), 5)

        self.draw_grid(surface, grid)


    # Functions for the ENVS

    # override the reward_function for the 
    def reward_function(self):
       
       # for now, the reward is the point differential for the action taken
        
        reward = self.score - self.prev_score

        self.prev_score = self.score

        # num_holes = self.num_holes()
        # reward += -10 * (num_holes - self.prev_num_holes)
        # self.prev_num_holes = num_holes

        # if self.lost:
            # reward += -(self.action_limit-self.action_count)

        # penalize stacking randomly also rewards line clearing
        # _, max_height = self.getHeights()
        # reward += -100*(max_height-self.max_height)
        # self.max_height = max_height

        bumpiness = self.get_bumpiness()
        reward += -100*(bumpiness - self.prev_bumpiness)
        self.prev_bumpiness = bumpiness

        return reward
    
    def get_bumpiness(self):
        arr = np.array(self.simple_grid)
        grid = arr.reshape((23,10))

        heights = list()
        for j in range(len(grid[0])):
            height = 23
            for i in range(len(grid)):
                if grid[i][j] == 1:
                    height = i
                    break
            heights.append(height)

        bumpiness = 0
        for i in range(len(heights)-1):
            bumpiness += abs(heights[i+1] - heights[i])
        return bumpiness


    
    def get_holes(self):
        arr = np.array(self.simple_grid)
        grid = arr.reshape((23,10))

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

    def num_holes(self):
        
        # g2h = StateActionFeatures.get_holes(grid)
        # n_holes = 0
        # for k in g2h:
        #     n_holes += len(g2h[k])
        holes = self.get_holes()
        return len(holes)

    def getHeights(self):
        min_height = 23 
        max_height = 0
        # self.grid = [[(0,0,0) for _ in range(10)] for _ in range(23)]
        #self.simple_grid = []
        for i in range(len(self.grid)):
            has_one = False
            for j in range(len(self.grid[i])):
                if self.simple_grid[i*10+j] == 1: 
                    has_one = True
                    break
            if has_one:
                height = 23 - i
                max_height = height if height > max_height else max_height
                min_height = height if height < min_height else min_height
        return min_height, max_height
# if __name__ == '__main__':
#     game = Blitz()
#     game.start_game()
        