from gym.envs.registration import register

register(
    id='tetris-v1',
    entry_point='gym_tetris.envs:TetrisEnv',
)

register(
    id='blitz-v1',
    entry_point='gym_tetris.envs:TetrisEnv',
)

register(
    id='forty-v1',
    entry_point='gym_tetris.envs:TetrisEnv',
)
