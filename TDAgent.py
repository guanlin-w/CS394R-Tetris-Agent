from env import *
from game import *
import gymnasium as gym
import numpy as np


S = [[
    '.00',
    '00.',
    '...'],
    [
    '.0.',
    '.00',
    '..0'],
    [
    '...',
    '.00',
    '00.'],
    [
    '0..',
    '00.',
    '.0.']]

Z = [[
    '00.',
    '.00',
    '...'],
    [
    '..0',
    '.00',
    '.0.'],
    [
    '...',
    '00.',
    '.00'],
    [
    '.0.',
    '00.',
    '0..']]

I = [
        ['....',
        '0000',
        '....',
        '....'],

        ['..0.',
        '..0.',
        '..0.',
        '..0.'],

        ['....',
        '....',
        '0000',
        '....'],

        ['.0..',
        '.0..',
        '.0..',
        '.0..']

    ]

O = [[
    '00',
    '00'
    ]]

J = [[
    '0..',
    '000',
    '...'],
    [
    '.00',
    '.0.',
    '.0.'],
    [
    '...',
    '000',
    '..0'],
    [
    '.0.',
    '.0.',
    '00.']]

L = [[
    '..0',
    '000',
    '...'],
    [
    '.0.',
    '.0.',
    '.00'],
    [
    '...',
    '000',
    '0..'],
    [
    '00.',
    '.0.',
    '.0.']]

T = [[
    '.0.',
    '000',
    '...'],
    [
    '.0.',
    '.00',
    '.0.'],
    [
    '...',
    '000',
    '.0.'],
    [
    '.0.',
    '00.',
    '.0.']]

shapes = [S, Z, I, O, J, L, T]

class StateActionFeatures():
    # def in_bounds(i, j, grid):
            #     return 
    # @staticmethod
    # def bfs(i, j, grid, visited, g2h):
    #     q = list()
    #     q.append((i, j))
        
    #     found_empties = list()
    #     touched_top = False
    #     while q:
    #         e = q.pop(0)

    #         i, j = e

    #         if not (i >= 0 and i < grid.shape[0] and j >= 0 and j < grid.shape[1]):
    #             continue
    #         if i == 0:
    #             touched_top = True
    #         if grid[i][j] == 1:
    #             continue
    #         if visited[i][j] == 1:
    #             continue

    #         found_empties.append((i, j))
    #         visited[i][j] = 1
    #         q.append((i-1, j))
    #         q.append((i+1, j))
    #         q.append((i, j-1))
    #         q.append((i, j+1))

    #     if not touched_top:
    #         g2h[len(g2h)] = found_empties

    # @staticmethod
    # def get_holes(grid):
    #     group_to_holes = dict()

    #     visited = np.zeros_like(grid)

    #     for i in range(len(grid)):
    #         for j in range(len(grid[0])):
    #             StateActionFeatures.bfs(i, j, grid, visited, group_to_holes)

    #     return group_to_holes

    @staticmethod
    def get_holes(grid):
        holes = list()
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == 0:
                    isHole = False
                    for i1 in range(i, -1, -1):
                        if grid[i1, j] == 1:
                            isHole = True
                    if isHole:
                        holes.append((i, j))
        return holes

    @staticmethod
    def num_holes(grid):
        
        # g2h = StateActionFeatures.get_holes(grid)
        # n_holes = 0
        # for k in g2h:
        #     n_holes += len(g2h[k])

        holes = StateActionFeatures.get_holes(grid)
        return len(holes)

    @staticmethod
    def rows_with_holes(grid):
        # g2h = StateActionFeatures.get_holes(grid)
        # rows = set()
        # for k in g2h:
        #     v = g2h[k]
        #     for (i, j) in v:
        #         rows.add(i)

        holes = StateActionFeatures.get_holes(grid)
        rows = set()
        for (i, j) in holes:
            rows.add(i)
        return len(rows)

    def column_transitions(grid):
        n_cts = 0
        for j in range(len(grid[0])):
            if 0 != grid[0][j]:
                n_cts += 1
            for i in range(0, len(grid)-1):
                if grid[i][j] != grid[i+1][j]:
                    n_cts += 1
            if grid[-1][j] != 1:
                n_cts += 1
        return n_cts
    
    def row_transitions(grid):
        n_rts = 0
        for i in range(len(grid)):
            if 1 != grid[i][0]:
                n_rts += 1
            for j in range(0, len(grid[0])-1):
                if grid[i][j] != grid[i][j+1]:
                    n_rts += 1
            if grid[i][-1] != 1:
                n_rts += 1
        return n_rts

    def landing_height(grid, vector):
        j_box = vector[0]
        i_box = vector[1]
        
        shape = shapes[vector[2]][vector[3]]

        height = 0
        for k in range(len(shape)):
            if '0' in shape[k]:
                height += 1
        
        dists = np.zeros(len(shape[0]))
        i_g_mins = np.zeros(len(shape[0]))
        for j_rel in range(len(shape[0])):
            j = j_box + j_rel

            # for i_rel in len(shape):
            #     i = i_box + i_rel
            #     for i1 in range(i, 23):
            #         if grid[i][j] == 1:
            #             lh_bot = 23 - i
            #             break
            i_p_max = -np.inf
            for i_rel in range(len(shape)):
                i = i_box + i_rel
                if shape[i_rel][j_rel] == '0':
                    i_p_max = i
            
            i_g_min = 23
            if i_p_max != -np.inf:
                for i_g in range(len(grid)-1, i_p_max, -1):
                    if grid[i_g][j] == 1:
                        i_g_min = i_g
            
            dists[j_rel] = i_g_min - i_p_max
            i_g_mins[j_rel] = i_g_min

        j_rel_min = np.argmin(dists)
        lh = (23 - i_g_mins[j_rel_min] + 1) + height/2 - 0.5

        return lh

    def cumulative_wells(grid):
        grid_pad = np.ones((grid.shape[0], grid.shape[1]+2))
        grid_pad[:, 1:-1] = grid

        n_cwells = 0
        for i in range(len(grid_pad)):
            for j in range(1, len(grid_pad[0])-1):
                i_curr = i
                while i_curr >= 0 and grid_pad[i_curr][j] == 0 and grid_pad[i_curr][j-1] == 1 and grid_pad[i_curr][j+1] == 1:
                    i_curr -= 1
                    n_cwells += 1

        return n_cwells
    
    def eroded_piece_cells(grid):
        return 0
    
    def hole_depth(grid):
        holes = StateActionFeatures.get_holes(grid)

        j2h = dict()
        for i, j in holes:
            if j not in j2h:
                j2h[j] = list()
            j2h[j].append(i)
        
        depth = 0
        for j in j2h:
            i_max = max(j2h[j])
            for i in range(i_max-1, -1, -1):
                if grid[i][j] == 1:
                    depth += 1
        return depth
        
        

class StateActionFeatureVector():
    def __init__(self):
        self.feature_dims = 8 + 4
        self.num_actions = 6


    def feature_vector_len(self):
        return self.feature_dims * self.num_actions
    
    def __call__(self, s, done, a):
        # s
        #     self.simple_grid 
        #     self.current_piece.x
        #     self.current_piece.y
        #     self.current_piece.index
        #     self.current_piece.rotation
        #     next_pieces_ind
        #     hold_piece_ind
        #     swapped_piece
        # a (0-5)
        # print('HERE')
        # print(len(s))
        # old grid
        # print(type(s))
        # print(len(s))
        simple_grid = s[:230]
        arr_grid = simple_grid.reshape((23,10))

        vector = s[230:]
        # print('vector')
        # print(vector)

        
        n_rows_with_holes = StateActionFeatures.rows_with_holes(arr_grid)
        n_cts = StateActionFeatures.column_transitions(arr_grid)
        n_holes = StateActionFeatures.num_holes(arr_grid)
        lh = StateActionFeatures.landing_height(arr_grid, vector)
        n_cwells = StateActionFeatures.cumulative_wells(arr_grid)
        n_rts = StateActionFeatures.row_transitions(arr_grid)
        n_epcs = StateActionFeatures.eroded_piece_cells(arr_grid)
        hd = StateActionFeatures.hole_depth(arr_grid)

        state_vec = np.array([n_rows_with_holes, n_cts, n_holes, lh, n_cwells, n_rts, n_epcs, hd, vector[0], vector[1], vector[2], vector[3]])
        sa_vec = np.zeros(len(state_vec) * self.num_actions)
        sa_vec[a * len(state_vec) : (a+1) * len(state_vec)] = state_vec

        return sa_vec        


def SarsaLambda(
    env, # openai gym environment
    gamma:float, # discount factor
    lam:float, # decay rate
    alpha:float, # step size
    X:StateActionFeatureVector,
    num_episode:int,
) -> np.array:
    """
    Implement True online Sarsa(\lambda)
    """

    def epsilon_greedy_policy(s,done,w,epsilon=0.1):
        nA = env.action_space.n
        Q = [np.dot(w, X(s,done,a)) for a in range(nA)]

        if np.random.rand() < epsilon:
            return np.random.randint(nA)
        else:
            return np.argmax(Q)

    w = np.zeros((X.feature_vector_len()))

    #TODO: implement this function
    # raise NotImplementedError()
    for e in range(num_episode):
        print(e)
        (state,_), acc_r, done = env.reset(), 0., False

        a = epsilon_greedy_policy(state, done, w)
        x = X(state, done, a)
        # print(x)
        z = np.zeros((X.feature_vector_len()))
        Qold = 0
        while not done:
            state, r, done, _, _ = env.step(a)
            ap = epsilon_greedy_policy(state, done, w)
            xp = X(state, done, ap)
            print('xp')
            print(xp)
            Q = np.dot(w, x)
            Qp = np.dot(w, xp)
            delta = r + gamma*Qp - Q
            z = gamma*lam*z + (1-alpha*gamma*lam*np.dot(z, x))*x
            print('z')
            print(z)
            w = w + alpha*(delta + Q - Qold)*z - alpha*(Q - Qold)*x
            print('w')
            print(w)
            Qold = Qp
            x = xp
            a = ap
    
    return w


def test_sarsa_lamda(env_str):
    env = gym.make(env_str)

    gamma = 1.
    lam = 0.8
    alpha = 0.1

    X = StateActionFeatureVector()

    w = SarsaLambda(env, gamma, lam, alpha, X, 2000)

    def greedy_policy(s,done):
        Q = [np.dot(w, X(s,done,a)) for a in range(env.action_space.n)]
        return np.argmax(Q)

    def _eval(i1, render=False):
        # print(i1)
        (s,_), done = env.reset(), False
        if render: env.render()

        G = 0.
        while not done:
            a = greedy_policy(s,done)
            s,r,done,_,_ = env.step(a)
            if render: env.render()

            G += r
        return G

    Gs = [_eval(i1) for i1 in  range(100)]
    _eval(True)

    assert np.max(Gs) >= -110.0, 'fail to solve mountaincar'

if __name__ == "__main__":
    # test_sarsa_lamda('FortyLine-Tetris-v0')
    test_sarsa_lamda('Blitz-Tetris-v0')
