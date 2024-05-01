from env import *
from game import *
import gymnasium as gym
import time

# look at env/__init__.py for the gym names
env = gym.make('Blitz-Tetris-v0')

env.reset()
done = False
i = 0
while not done:
    action = env.action_space.sample()
    obs,reward,done,_,_ = env.step(action)
    env.render()
    time.sleep(2)

env.exit()