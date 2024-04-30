from env import *
from game import *
import gymnasium as gym

from stable_baselines3 import DQN
from stable_baselines3.common.env_checker import check_env

# look at env/__init__.py for the gym names
env = gym.make('Blitz-Tetris-v0')
env.reset()

check_env(env)

models_dir = "./models/DQN"
log_dir = './logs'
model = DQN(policy="MlpPolicy", env=env, verbose=1,tensorboard_log=log_dir)

# saves every TIMESTEPS steps
TIMESTEPS = 10000
for i in range(1,30):
    model.learn(total_timesteps=TIMESTEPS,reset_num_timesteps=False, tb_log_name="DQN")
    model.save(f'{models_dir}/{TIMESTEPS*i}')
    print(f'Timestep: {i*TIMESTEPS}')

# vec_env = model.get_env()
# obs = vec_env.reset()

# done = False
# i = 0
# while not done:
#     action = env.action_space.sample()
#     obs,reward,done,_ = env.step(action)
#     env.render()