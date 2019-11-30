import gym
import os
import numpy as np

from env import utils

class BaseEnv(gym.Env):
    ''' mouse walking maze environment '''

    def __init__(self, map_name='default_map', end_step=100):
        
        self.map = utils.load_map(map_name)
        self.end_step = end_step
        self.action_space = gym.spaces.Discrete(4)
        self.obs_shape = self.map.shape
        self.observation_space = gym.spaces.Box(low=0, high=5, shape=self.obs_shape, dtype=np.float16)

    def reset(self):

        self.map_cache = np.copy(self.map)
        self.current_step = 0

        return utils.map_to_obs(self.map_cache)

    def step(self, action):
        pass

    def render(self):
        pass

    def walking_maze(self, action):

        # Up
        if action == 0:
            pass

        # Down
        if action == 1:
            pass

        # Left
        if action == 2:
            pass

        # Right
        if action == 3:
            pass

    def get_reward(self, target_obj):
        pass

    def is_done(self, target_obj):
        pass
