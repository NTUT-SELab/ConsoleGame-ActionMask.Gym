import gym
import os
import time
import numpy as np

from env.EmptyRooms import utils
from env.EmptyRooms.map_define import MapEnum

class BaseEnv(gym.Env):
    """
    A mouse walking maze environment.

    : param map_name: (str) 要運行的地圖和相關資訊
    : param end_step: (int) 每個回合，最多可運行的步數
    """
    def __init__(self, end_step=1000):
        self.map = utils.load_map('map1')
        self.end_step = end_step
        self.action_space = gym.spaces.Discrete(4)
        self.obs_shape = (self.map.shape[0], self.map.shape[1], 1)
        self.observation_space = gym.spaces.Box(low=0, high=2, shape=self.obs_shape, dtype=np.float16)

    def reset(self):
        """
        Reset environment.
        """
        self.map_cache = np.copy(self.map)
        self.current_step = 0

        return utils.map_to_obs(self.map_cache, self.obs_shape)

    def step(self, action):
        """
        Tell the environment which action to do.

        : param action: (int) 要執行的動作
        """
        target_obj = utils.get_target_obj(self.map_cache, action)
        reward = self.get_reward(target_obj)
        done = self.is_done(target_obj)

        self.walking_maze(action)
        obs = utils.map_to_obs(self.map_cache, self.obs_shape)
        self.current_step += 1

        return obs, reward, done, { }

    def render(self, mode='human', delay_time=0.1):
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

        for rows in self.map_cache:
            print(' '.join(rows))
        time.sleep(delay_time)

    def walking_maze(self, action):
        """
        Move mouse position.

        : param action: (int) 要執行的動作
        """
        if utils.get_target_obj(self.map_cache, action) != MapEnum.wall:
            mouse_position = utils.get_mouse_position(self.map_cache)
            self.map_cache[mouse_position[0]][mouse_position[1]] = MapEnum.road.value
            target_position = utils.get_target_position(mouse_position, action)
            self.map_cache[target_position[0]][target_position[1]] = MapEnum.mouse.value

    def get_reward(self, target_obj):
        """
        Give relative rewards based on mouse actions.

        : param target_obj: (MapEnum) 老鼠前方ㄧ格的物件
        """
        if target_obj == MapEnum.exit:
            return 10
        else:
            return 0

    def is_done(self, target_obj):
        """
        Check if this round is over.

        : param target_obj: (MapEnum) 老鼠前方ㄧ格的物件
        """
        return self.current_step >= self.end_step or target_obj == MapEnum.exit
