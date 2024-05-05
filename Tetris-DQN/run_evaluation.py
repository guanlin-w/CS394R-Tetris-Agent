import gym
import gym_tetris

from statistics import mean, median
from gym_tetris.ai.QNetwork import QNetwork
import pygame
import os
import sys
import time
import numpy as np
def main(args):
    env_name = None

    load_path = None
    if args[1] == 'blitz':
        load_path = os.path.join('gym_tetris', 'ai', 'weights', 'DQN', 'blitz', 'final' + '.weights.h5')
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
        load_path = os.path.join('gym_tetris', 'ai', 'weights', 'DQN', 'blitz2', '97' + '.weights.h5')
        env_name = 'eval-blitz-v1'
    if args[1] == 'forty2':
        load_path = os.path.join('gym_tetris', 'ai', 'weights', 'DQN', 'forty2', '100' + '.weights.h5')
        env_name = 'eval-forty-v1'
    if args[1] == 'blitz3':
        load_path = os.path.join('gym_tetris', 'ai', 'weights', 'DQN', 'blitz3', '239' + '.weights.h5')
        env_name = 'eval-blitz-v1'
    if args[1] == 'blitz-blitz3':
        load_path = os.path.join('gym_tetris', 'ai', 'weights', 'DQN', 'blitz-blitz3', '239' + '.weights.h5')
        env_name = 'eval-blitz-v1'
    if args[1] == 'forty-forty3':
        load_path = os.path.join('gym_tetris', 'ai', 'weights', 'DQN', 'forty-forty3', '79' + '.weights.h5')
        env_name = 'eval-forty-v1'
    if args[1] == 'forty3':
        load_path = os.path.join('gym_tetris', 'ai', 'weights', 'DQN', 'forty3', '73' + '.weights.h5')
        env_name = 'eval-forty-v1'
    if args[1] == 'forty2-blitz2':
        load_path = os.path.join('gym_tetris', 'ai', 'weights', 'DQN', 'forty2-blitz2', 'final' + '.weights.h5')
        env_name = 'eval-blitz-v1'
    if args[1] == 'blitz2-forty2':
        load_path = os.path.join('gym_tetris', 'ai', 'weights', 'DQN', 'blitz2-forty2', 'final' + '.weights.h5')
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
    # frames_arr = np.zeros(num_trials)
    # lines_arr = np.zeros(num_trials)
    # score_arr = np.zeros(num_trials)

    frames_list = []
    lines_list = []
    score_list = []

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
                frames_per_game = info['frames']
                average_line_cleared += info['lines']
                time_taken += frames_per_game
                average_score += info['score']

                if info['lines'] >= 40 or info['frames'] >= 1990:
                    frames_list.append(info['frames'])
                    lines_list.append(info['lines'])
                    score_list.append(info['score'])

                # frames_arr[i] = info['frames']
                # lines_arr[i] = info['lines']
                # score_arr[i] = info['score']
                

                obs = env.reset()

    env.close()

    frames_arr = np.array(frames_list)
    lines_arr = np.array(lines_list)
    score_arr = np.array(score_list)


    print(f'Average games frames per game {(np.mean(frames_arr), np.std(frames_arr), len(frames_arr)/num_trials)}')
    print(f'Average lines cleared per game {(np.mean(lines_arr), np.std(lines_arr), len(lines_arr)/num_trials)}')
    print(f'Average Score per game {(np.mean(score_arr), np.std(score_arr), len(score_arr)/num_trials)}')


if __name__ == '__main__':
    main(sys.argv)
