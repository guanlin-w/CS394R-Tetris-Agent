import gym
from gym import spaces
from game import Base

class BaseEnv(gym.Env):
    def __init__(self):
        super(BaseEnv,self).__init__()
        self.game = Base()
        self.action_space = spaces.Discrete(6)
        self.observation_space = spaces.Discrete(23*10+4+4+1)
        self.game.setup()

    def step(self,action):
        return self.game.action(action)

    def reset(self):
        self.game.setup()
    def render(self):
        self.game.render()
    
    def close(self):
        self.game.close()
        