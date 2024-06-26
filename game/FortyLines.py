from game import Base
import pygame
class FortyLines(Base):
    def __init__(self):
        super().__init__()
        self.lines_cleared = 0
        self.prev_cleared = 0
        self.won = False


    # override clear_rows to track the number of lines we have cleared
    # same exact logic with the additional effect of tracking self.lines_cleared
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
        self.lines_cleared += inc
        return inc


    # override to update the win condition
    def evaluateBoard(self):
        # evaluate the board to see if we have won or loss
        # in this case, check if we have lost or have reached 40 lines
        if self.check_lost(self.locked_positions):
            self.done = True
            self.lost  =True

        # new component here
        if self.lines_cleared >= 40:
            self.done = True
            self.won = True

    # override to output the number of lines cleared instead of the score
    def draw_window(self,surface, grid, score=0, last_score = 0):
        
        surface.fill((0, 0, 0))

        pygame.font.init()
        font = pygame.font.SysFont('comicsans', 60)
        label = font.render('Tetris', 1, (255, 255, 255))

        surface.blit(label, (self.top_left_x + self.play_width / 2 - (label.get_width() / 2), 30))

        # current score
        font = pygame.font.SysFont('comicsans', 30)
        label = font.render('Lines:' + str(self.lines_cleared), 1, (255,255,255))

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


    # Functions for the ENVS

    # override the reward_function for the 
    def reward_function(self):
       
       #  Current reward function:
       # -1 for every action
       # +100 for each line cleared
       # -4000 for game loss
        
        reward = -1 + 100*(self.lines_cleared  - self.prev_cleared)

        if self.lost:
            reward += -4000

        self.prev_cleared = self.lines_cleared
        return reward
    
    
# if __name__ == '__main__':
#     game = FortyLines()
#     game.start_game()
        