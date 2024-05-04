import gym
import gym_tetris

from statistics import mean, median
from gym_tetris.ai.QNetwork import QNetwork
import pygame
import os
import sys
import time
def main(args):
    env_name = None

    load_path = None
    if args[1] == 'blitz':
        load_path = os.path.join('gym_tetris', 'ai', 'weights', 'DQN', 'blitz', '97' + '.weights.h5')
        env_name = 'eval-blitz-v1'
    if args[1] == 'forty':
        load_path = os.path.join('gym_tetris', 'ai', 'weights', 'DQN', 'forty', '117' + '.weights.h5')
        env_name = 'eval-forty-v1'
    if args[1] == 'blitz-blitz2':
        load_path = os.path.join('gym_tetris', 'ai', 'weights', 'DQN', 'blitz-blitz2', 'final' + '.weights.h5')
        env_name = 'eval-blitz-v1'
    if args[1] == 'forty-forty2':
        load_path = os.path.join('gym_tetris', 'ai', 'weights', 'DQN', 'forty-forty2', 'final' + '.weights.h5')
        env_name = 'eval-forty-v1'
    if args[1] == 'blitz2':
        load_path = os.path.join('gym_tetris', 'ai', 'weights', 'DQN', 'blitz2', 'final' + '.weights.h5')
        env_name = 'eval-blitz-v1'
    if args[1] == 'forty2':
        load_path = os.path.join('gym_tetris', 'ai', 'weights', 'DQN', 'forty2', '100' + '.weights.h5')
        env_name = 'eval-forty-v1'

    env = gym.make(env_name, reward_hack=True,action_mode=1)
    network = QNetwork(discount=1, epsilon=0, epsilon_min=0, epsilon_decay=0)
    if load_path:
        network.load(load_path)
    else:
        print("No network loaded")

    obs = env.reset()
    running = True
    display = True

    average_line_cleared = 0
    time_taken = 0
    average_score = 0

    num_trials = 20
    for i in range(num_trials):
        done = False
        

        while not done:
            sa = network.act(obs)
            action = sa[:2]
            state = sa[2:]
            obs, reward, done, info = env.step(action)
            if display:
                env.render()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        display = not display
            if done:
                line_count = info['lines']
                frames_per_game = info['frames']
                average_line_cleared += line_count
                time_taken += frames_per_game
                average_score += info['score']
                obs = env.reset()

    env.close()

    print(f'Average games frames per game {time_taken/num_trials}')
    print(f'Average lines cleared per game {average_line_cleared/num_trials}')
    print(f'Average Score per game {average_score/num_trials}')


if __name__ == '__main__':
    main(sys.argv)
