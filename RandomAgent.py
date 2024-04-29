import env.BaseEnv
import env.FortyEnv
import gym

env = gym.make('FortyLine-Tetris-v0')

env.reset()
done = False
i = 0
while not done:
    action = env.action_space.sample()
    obs,reward,done,_ = env.step(action)
    env.render()