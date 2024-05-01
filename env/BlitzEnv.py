import gymnasium as gym
from gymnasium import spaces
from game import Blitz
import numpy as np
class BlitzEnv(gym.Env):
    def __init__(self):
        super(BlitzEnv,self).__init__()
        self.game = Blitz()

        # 0 - Left
        # 1 - Right
        # 2 - Up (rotate)
        # 3 - Down
        # 4 - C (swap)
        # 5 - space
        self.action_space = spaces.Discrete(6)


        # return the initial start state
        # State includes the following:
        # grid - 23*10
        # the current piece (x,y) of the bounding box. The current shape index and the rotation index - 4
        # the list of the next 4 pieces (in terms of index in the shapes list) - 4
        # the hold piece index - 1


        self.observation_space = spaces.Box(low=-1,high=23, shape=(240,),dtype=np.int64)
        # self.observation_space = spaces.Dict({
        #     'grid': spaces.Box(low=0, high=1, shape=(23, 10), dtype=np.uint8),  # Binary grid
        #     'vector': spaces.Box(low=-1, high=23, shape=(10,), dtype=np.float32)  # Additional vector features
        # })
        self.game.setup()

    def step(self,action):
        return self.game.action(action)

    def reset(self,seed=None):
        return self.game.setup(), {}
    def render(self):
        self.game.render()
    
    def close(self):
        self.game.close()
        