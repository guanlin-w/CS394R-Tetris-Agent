import os
import random

import gym
import numpy as np
import pygame
from gym import spaces

from gym_tetris.board import Board
from gym_tetris.game import Game
from gym_tetris.view import View

WIN_WIDTH = 480
WIN_HEIGHT = 526


class EvalFortyEnv(gym.Env):
    metadata = {
        'render.modes': ['human']
    }

    def __init__(self, reward_hack, action_mode=0):
        self.view = None
        self.game = None
        self.reward_hack = reward_hack
        self.action_mode = action_mode
        self.line_count = 0
        self.frame_count = 0
        if action_mode == 0:
            # Nothing, Left, Right, Rotate left, Rotate right, Drop, Full Drop, Hold
            self.action_space = gym.spaces.Discrete(8)
        elif action_mode == 1:
            self.action_space = gym.spaces.Tuple((
                gym.spaces.Discrete(10),  # X
                gym.spaces.Discrete(4),  # Rotation
            ))
        self.observation_space = spaces.Box(low=-100000,high=100000, shape=(9,),dtype=np.float64)


    def step(self, action):
        """Performs one step/frame in the game and returns the observation, reward and if the game is over."""
        if self.action_mode == 0:
            if action == 1:  # Left
                self.game.board.move_piece(-1)
            elif action == 2:  # Right
                self.game.board.move_piece(1)
            elif action == 3:  # Rotate left
                self.game.board.rotate_piece(-1)
            elif action == 4:  # Rotate right
                self.game.board.rotate_piece(1)
            elif action == 5:  # Drop
                self.game.board.drop_piece()
                self.game.drop_time = self.game.get_drop_speed()
            elif action == 6:  # Full drop
                self.game.board.drop_piece_fully()
            elif action == 7:  # Hold
                self.game.board.hold_piece()
        elif self.action_mode == 1:
            x, rotation = action
            self.game.board.move_and_drop(x, rotation)

        rows = self.game.tick()
        rows_count = len(rows)
        done = self.game.board.is_game_over()

        reward = 1 if self.reward_hack else -1
        
        if rows_count == 1:
            reward += 40
        elif rows_count == 2:
            reward += 80
        elif rows_count == 3:
            reward += 120
        elif rows_count == 4:
            reward += 160

        if done:
            reward -= 500

        self.line_count += rows_count
        self.frame_count += 1
        if self.line_count >= 40:
            done = True
        seconds = self.view.seconds if self.view else 0
        return np.array(self.game.board.get_possible_states()), reward, done, {"score":self.game.score,"frames":self.frame_count,"lines":self.line_count}

    def reset(self):
        """Starts a new game."""
        self.game = Game(Board(10, 20))
        self.line_count = 0
        a = self.game.board.get_possible_states()
        self.frame_count = 0
        if self.view:
            self.view.seconds = 0
            self.view.reset_timer()
        # [print(x) for x in a]
        # [print(x) for x in self.game.board.get_possible_states()]
        return np.array(a)

    def close(self):
        """Closes the window."""
        if self.view is not None:
            self.view = None
            pygame.quit()

    def render(self, mode='human', close=False, width=WIN_WIDTH, height=WIN_HEIGHT):
        """Renders the game."""
        if self.view is None:
            pygame.init()
            win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
            font = pygame.font.Font(os.path.join(os.path.dirname(__file__), '..', 'assets', 'font.ttf'), 20)
            pygame.display.set_caption("Tetris")
            self.view = View(win, font)

        self.view.draw(self.game)

    def seed(self, seed=None):
        """Set the random seed for the game."""
        random.seed(seed)
        return [seed]
