import env.BaseEnv
import gym

gym.register(
    id='Base-Tetris-v0',
    entry_point='env.BaseEnv:BaseEnv',
    kwargs={}
)

env = gym.make('Base-Tetris-v0')

env.reset()
done = False
while not done:
    action = env.action_space.sample()
    obs,reward,done,_ = env.step(action)
    env.render()