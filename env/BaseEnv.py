import gym
from gym import spaces
from game import Base

class BaseEnv(gym.Env):
    def __init__(self):
        super(BaseEnv,self).__init__()
        self.game = Base()

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
        self.observation_space = spaces.Discrete(23*10 + 4 + 4 + 1+1)
        self.game.setup()

    def step(self,action):
        return self.game.action(action)

    def reset(self):
        self.game.setup()
    def render(self):
        self.game.render()
    
    def close(self):
        self.game.close()
        