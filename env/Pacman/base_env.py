import gym
import numpy as np


class BaseEnv(gym.Env):
    """
    A pacman environment.

    : param map_name: (str) 要運行的地圖和相關資訊
    """
    def __init__(self, map_name='default_map'):
        pass