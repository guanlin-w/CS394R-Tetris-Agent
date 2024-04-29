import gym
gym.register(
    id='Base-Tetris-v0',
    entry_point='env.BaseEnv:BaseEnv',
    kwargs={}
)

gym.register(
    id='FortyLine-Tetris-v0',
    entry_point='env.FortyEnv:FortyEnv',
    kwargs={}
)


gym.register(
    id='Blitz-Tetris-v0',
    entry_point='env.BlitzEnv:BlitzEnv',
    kwargs={}
)