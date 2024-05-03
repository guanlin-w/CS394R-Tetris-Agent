from env import *
from game import *
import gymnasium as gym

from stable_baselines3 import DQN
from stable_baselines3.common.env_checker import check_env

# look at env/__init__.py for the gym names
env = gym.make('Blitz-Tetris-v0')
env.reset()

# check_env(env)

models_dir = "./models/DQN_heur_mlp_custom"
log_dir = './logs'


import torch as th
import torch.nn as nn
from stable_baselines3.common.torch_layers import BaseFeaturesExtractor
from stable_baselines3.common.policies import BasePolicy
from stable_baselines3.dqn.policies import DQNPolicy
from copy import deepcopy

class TetrisCNNExtractor(BaseFeaturesExtractor):
    def __init__(self, observation_space, features_dim: int):
        super(TetrisCNNExtractor, self).__init__(observation_space, features_dim)

        self.cnn = nn.Sequential(
            nn.Conv2d(1, 16, kernel_size=(3, 3), stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=(2, 1), stride=(2, 1)),  # Output: 16 x 11 x 10
            nn.Conv2d(16, 32, kernel_size=(3, 3), stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=(2, 1), stride=(2, 1)),  # Output: 32 x 5 x 10
            nn.Flatten()
        )
        # Flatten output dimensions: 32 * 5 * 10 = 1600
        self.fc = nn.Linear(1600, features_dim)
    
    def forward(self, x):
        return self.fc(self.cnn(x.float()))

class MultiInputFeaturesExtractor(BaseFeaturesExtractor):
    def __init__(self, observation_space, features_dim: int):
        super(MultiInputFeaturesExtractor, self).__init__(observation_space, features_dim)

        # Define the CNN extractor for the Tetris grid
        self.cnn_extractor = TetrisCNNExtractor(observation_space.spaces['grid'], features_dim=256)

        # Define a linear extractor for the additional vector input
        self.linear_extractor = nn.Sequential(
            nn.Linear(observation_space.spaces['vector'].shape[0], 16),
            nn.ReLU()
        )

        # Combining CNN and linear outputs into a single output of dimension features_dim
        self.combined_fc = nn.Linear(256 + 16, features_dim)

    def forward(self, observations):
        cnn_input = observations['grid'].unsqueeze(1)  # Adding channel dimension
        vector_input = observations['vector']

        cnn_features = self.cnn_extractor(cnn_input)
        vector_features = self.linear_extractor(vector_input.float())

        combined_features = th.cat((cnn_features, vector_features), dim=1)
        return self.combined_fc(combined_features)

class CustomNetwork(nn.Module):
    def __init__(self, features_extractor, action_dim):
        super(CustomNetwork, self).__init__()
        self.features_extractor = features_extractor
        self.network = nn.Sequential(
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, action_dim)
        )

    def forward(self, x):
        features = self.features_extractor(x)
        return self.network(features)
    
    def set_training_mode(self, mode: bool):
        self.train(mode)
    
    def _predict(self, obs, deterministic=False):
        # Assuming you want to run the network in evaluation mode when predicting
        self.eval()  # Set the network to evaluation mode
        with th.no_grad():
            outputs = self.forward(obs)
            if deterministic:
                # Return the maximum probability action (most likely action)
                return outputs.argmax(dim=1), None
            else:
                # Sample an action from the distribution (stochastic)
                probabilities = th.softmax(outputs, dim=1)
                return th.multinomial(probabilities, 1).squeeze(-1)

class CustomDQNPolicy(DQNPolicy):
    def __init__(self, observation_space, action_space, lr_schedule, **kwargs):
        super(CustomDQNPolicy, self).__init__(observation_space, action_space, lr_schedule, **kwargs)

        # Override the features extractor in DQNPolicy
        self.features_extractor = MultiInputFeaturesExtractor(self.observation_space, features_dim=64)

        # Redefine the network to incorporate the features extractor
        self.q_net = CustomNetwork(self.features_extractor, action_space.n)
        self.q_net_target = deepcopy(self.q_net)




# import torch
# import torch.nn as nn
# from stable_baselines3.common.torch_layers import BaseFeaturesExtractor

class CustomMLP(nn.Module):
    def __init__(self, observation_space, features_dim):
        super(CustomMLP, self).__init__()

        # Assuming observation_space is a Box space with shape (n_features,)
        n_input_features = observation_space.shape[0]

        # Define a simple MLP architecture
        self.net = nn.Sequential(
            nn.Linear(n_input_features, 64),  # First hidden layer
            nn.ReLU(),
            nn.Linear(64, 64),               # Second hidden layer
            nn.ReLU(),
            nn.Linear(64, features_dim)      # Output layer
        )

    def forward(self, x):
        return self.net(x)

class CustomDQNPolicy2(DQNPolicy):
    def __init__(self, observation_space, action_space, lr_schedule, **kwargs):
        super(CustomDQNPolicy2, self).__init__(observation_space, action_space, lr_schedule, **kwargs)

        # Replace the features extractor with your custom MLP
        self.features_extractor = CustomMLP(observation_space, features_dim=32)
        self.net_arch = []  # Not using any additional layers in the policy head

        # Redefine the Q-network to utilize the custom features extractor
        self.q_net = self.make_q_net()
        self.q_net_target = self.make_q_net()

# You would use the CustomDQNPolicy with your DQN model as shown previously
model = DQN(policy=CustomDQNPolicy2, env=env, verbose=1,tensorboard_log=log_dir, exploration_fraction=0.5, exploration_final_eps=0.1)

# saves every TIMESTEPS steps
TIMESTEPS = 10000
for i in range(1,300):
    model.learn(total_timesteps=TIMESTEPS,reset_num_timesteps=False, tb_log_name="DQN")
    model.save(f'{models_dir}/{TIMESTEPS*i}')
    print(f'Timestep: {i*TIMESTEPS}')