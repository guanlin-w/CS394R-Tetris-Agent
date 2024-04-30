from env import *
from game import *
import gymnasium as gym

from stable_baselines3 import DQN




env = gym.make('Blitz-Tetris-v0')



models_dir = "./models/DQN"
log_dir = './logs'
model_path = f'{models_dir}/290000.zip'
model = DQN.load(model_path,env=env)

# vec_env = model.get_env()
# obs = vec_env.reset()
obs,_ =env.reset()
done = False
i = 0
while not done:    
    env.render()
    action,_ = model.predict(obs)
    obs,reward,done,_,_ = env.step(action)
env.close()