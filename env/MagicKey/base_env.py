import gym
import os
import time
import numpy as np
import threading

from env.MagicKey import utils
from env.MagicKey.map_define import *
from env.MagicKey.map import Map
from env.MagicKey.map_element import *

class BaseEnv(gym.Env):
    """
    A snake environment.

    : param high:   (int) 地圖高度
    : param width:  (int) 地圖寬度
    : end_step:     (int) 遊戲最長步數
    """
    def __init__(self, high=30, width=20, end_step=10000):
        self.map = Map(high, width)
        self.end_step = end_step

        if high < 25 or width < 15 :
            raise Exception('地圖的高度必須大於25，與寬度必須大於15')
        
        self.action_space = gym.spaces.Discrete(27)
        self.obs_shape = (high, width, 1)
        self.observation_space = gym.spaces.Box(low=0, high=34, shape=self.obs_shape, dtype=np.float16)

    def reset(self):
        """
        Reset environment.
        """
        self.map.generate_data()
        utils.generate_texts_to_map(self.map)
        self.refresh_map()
        self.current_step = 0
        self.score = 0
        self.done = False
        return utils.map_to_obs(self.map.data, self.obs_shape)

    def step(self, action):
        """
        Tell the environment which action to do.

        : param action: (int) 要執行的動作
        """

        utils.apply_action(self.map, action)
        utils.move_text_elements(self.map, self.score)
        self.done = self.is_done()
        reward = self.get_reward()
        self.score += reward
        self.refresh_map()
        obs = utils.map_to_obs(self.map.data, self.obs_shape)
        self.current_step += 1
        return obs, reward, self.done, {}

    def render(self, delay_time=0.2, pause=False):
        """
        Print environment.

        : param delay_time: (float) 每次打印要延遲的時間
        """
        # for windows 
        if os.name == 'nt':
            _ = os.system('cls')
        # for mac and linux(here, os.name is 'posix') 
        else:
            _ = os.system('clear') 
        
        for rows in self.map.data:
            print(' '.join(rows))
        print('score: {}'.format(self.score) if not pause else "Pause")

        time.sleep(delay_time)


    def get_reward(self):
        """
        Give relative rewards based on mouse actions.

        : param target_obj: (MapEnum) 蛇前方ㄧ格的物件
        """
        reward = 0
        for element in self.map.elements:
            reward += element.reward
        if self.done:
            reward -= 500
        return reward

    def is_done(self):
        """
        Check if this round is over.

        : param target_obj: (MapEnum) 老鼠前方ㄧ格的物件
        """

        return self.current_step >= self.end_step or self.map.is_end()

    def refresh_map(self):
        """
        Refresh the map.

        : param generate_food: (bool) 刷新地圖時是否產生食物
        """
        self.map.refresh()
        utils.generate_texts_to_map(self.map)


    def map_to_string(self):
        state = ''
        for rows in self.map.data:
            state += ' '.join(rows) + '\n'
        return state
