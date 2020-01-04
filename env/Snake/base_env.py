import gym
import os
import time
import numpy as np

from env.Snake import utils

class BaseEnv(gym.Env):
    """
    A snake environment.
    """
    def __init__(self, high=50, width=40):
        self.high = high
        self.width = width
        if high < 10 or width < 10 :
            raise Exception('地圖的高度與寬度必須 > 10')

        self.action_space = gym.spaces.Discrete(4)
        self.obs_shape = (high, width, 1)
        self.observation_space = gym.spaces.Box(low=0, high=4, shape=self.obs_shape, dtype=np.float16)

    def reset(self):
        self.map_data = utils.generate_map(self.high, self.width)
        self.snake_position = utils.generate_snake()
        self.map_data = utils.reflash_map(self.map_data, self.snake_position)
        self.food_position = utils.generate_food(self.map_data)
        self.map_data = utils.reflash_map(self.map_data, self.snake_position, self.food_position)

        return utils.map_to_obs(self.map_data, self.obs_shape)

    def step(self, action):
        pass

    def render(self, delay_time=1):

        # for windows 
        if os.name == 'nt':
            _ = os.system('cls')
        # for mac and linux(here, os.name is 'posix') 
        else:
            _ = os.system('clear') 
        
        for rows in self.map_data:
            print(' '.join(rows))

        time.sleep(delay_time)
