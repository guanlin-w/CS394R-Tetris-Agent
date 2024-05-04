import gym
import gym_tetris

from statistics import mean, median
from gym_tetris.ai.QNetwork import QNetwork

import os

def main(args):
    env_name = None
    if args[1] == 'blitz':
        env_name = 'blitz-v1'
    if args[1] == 'forty':
        env_name = 'forty-v1'
    
    reward_hack = args[2] == 'rh'

    load_path = None
    if args[3] == 'blitz':
        load_path = os.path.join('gym_tetris', 'ai', 'weights', 'DQN', 'blitz')
    if args[3] == 'forty':
        load_path = os.path.join('gym_tetris', 'ai', 'weights', 'DQN', 'forty')


    env = gym.make(env_name, action_mode=1, reward_hack)
    network = QNetwork(epsilon_decay=0.4)
    if load_path:
        network.load(load_path)

    running = True
    total_games = 0
    total_steps = 0
    for ij in range(240):
        steps, rewards, scores = network.train(env, episodes=25)
        total_games += len(scores)
        total_steps += steps
        network.save(ij)
        print("==================")
        print("* Total Games: ", total_games)
        print("* Total Steps: ", total_steps)
        print("* Epsilon: ", network.epsilon)
        print("*")
        print("* Average: ", sum(rewards) / len(rewards), "/", sum(scores) / len(scores))
        print("* Median: ", median(rewards), "/", median(scores))
        print("* Mean: ", mean(rewards), "/", mean(scores))
        print("* Min: ", min(rewards), "/", min(scores))
        print("* Max: ", max(rewards), "/", max(scores))
        print("==================")

    env.close()


if __name__ == '__main__':
    main(sys.args)
