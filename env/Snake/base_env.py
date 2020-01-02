import gym
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

    def reset(self):
        self.map = utils.generate_map(self.high, self.width)
        self.snake_position = utils.generate_snake()
        self.map = utils.reflash_map(self.map, self.snake_position)
        self.food_position = utils.generate_food(self.map)
        self.map = utils.reflash_map(self.map, self.snake_position, self.food_position)

    def render(self):
        for rows in self.map:
            print(' '.join(rows))
