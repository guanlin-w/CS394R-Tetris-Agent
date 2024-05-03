from env import *
from game import *
import gymnasium as gym
import time
from stable_baselines3 import DQN


# import ale_py

# from ale_py import ALEInterface

# # Create ALEInterface instance
# ale = ALEInterface()

# # Set the ROM path
# rom_path = '/Users/VaishnavBipin/Documents/RLhomeworks/final/venv/lib/python3.11/site-packages/AutoROM/roms/tetris.bin'  # Update this with the actual path to your ROMs
# # ale.setInt('rom_path', rom_path)

# # Initialize ALE (optional, but recommended)
# ale.loadROM(rom_path)


# env = gym.make("ALE/Tetris-v5")

env = gym.make('Blitz-Tetris-v0')



models_dir = "./models/DQN_heur_mlp_custom"
log_dir = './logs'
model_path = f'{models_dir}/1680000.zip'
model = DQN.load(model_path,env=env)

# vec_env = model.get_env()
# obs = vec_env.reset()
obs,_ =env.reset()
done = False
i = 0
rew = 0
c = 0
while not done:    
    env.render()
    action,_ = model.predict(obs)
    obs,reward,done,_,_ = env.step(action)
    rew += reward
    time.sleep(.01)
    c += 1
    print(action)
print(c)
print(rew)
env.close()