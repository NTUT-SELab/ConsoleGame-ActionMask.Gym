import gym
import os
import time
import numpy as np

from env.Snake import utils
from env.Snake.map_define import MapEnum

class BaseEnv(gym.Env):
    """
    A snake environment.

    : param high:   (int) 地圖高度
    : param width:  (int) 地圖寬度
    : end_step:     (int) 遊戲最長步數
    """
    def __init__(self, high=50, width=40, end_step=10000):
        self.high = high
        self.width = width
        self.end_step = end_step
        if high < 10 or width < 10 :
            raise Exception('地圖的高度與寬度必須 > 10')

        self.action_space = gym.spaces.Discrete(4)
        self.obs_shape = (high, width, 1)
        self.observation_space = gym.spaces.Box(low=0, high=4, shape=self.obs_shape, dtype=np.float16)

    def reset(self):
        """
        Reset environment.
        """
        self.snake_position = utils.generate_snake()
        self.reflash_map(generate_food=True)
        self.current_step = 0
        self.previous_action = 1

        return utils.map_to_obs(self.map_data, self.obs_shape)

    def step(self, action):
        """
        Tell the environment which action to do.

        : param action: (int) 要執行的動作
        """
        odopa = self.compute_opposite_direction_of_previous_action()

        if action == odopa:
            action = self.previous_action

        target_obj = utils.get_target_obj(self.map_data, action)
        reward = self.get_reward(target_obj)
        done = self.is_done(target_obj)

        self.move_snake(action, target_obj)
        obs = utils.map_to_obs(self.map_data, self.obs_shape)
        self.previous_action = action
        self.current_step += 1

        return obs, reward, done, { }

    def render(self, delay_time=0.5):
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
        
        for rows in self.map_data:
            print(' '.join(rows))

        time.sleep(delay_time)

    def move_snake(self, action, target_obj):
        """
        Move snake position.

        : param action
        """
        snake_head_position = utils.get_snake_head_position(self.map_data)
        target_position = utils.get_target_position(snake_head_position, action)
        self.snake_position.insert(0, target_position)
        
        if target_obj != MapEnum.food:
            del self.snake_position[len(self.snake_position) - 1]
            self.reflash_map()
        else:
            self.reflash_map(generate_food=True)

    def get_reward(self, target_obj):
        """
        Give relative rewards based on mouse actions.

        : param target_obj: (MapEnum) 蛇前方ㄧ格的物件
        """
        if target_obj == MapEnum.body:
            return -1
        elif target_obj == MapEnum.wall:
            return -1
        elif target_obj == MapEnum.food:
            return 1
        else:
            return 0

    def is_done(self, target_obj):
        """
        Check if this round is over.

        : param target_obj: (MapEnum) 老鼠前方ㄧ格的物件
        """
        return self.current_step >= self.end_step or target_obj == MapEnum.body or \
            target_obj == MapEnum.wall or np.count_nonzero(self.map_data == ' ') < 5

    def compute_opposite_direction_of_previous_action(self):
        """
        Compute opposite direction of previous action.
        Snake game cannot move backwards.
        """
        if self.previous_action == 0:
            return 1
        elif self.previous_action == 1:
            return 0
        elif self.previous_action == 2:
            return 3
        elif self.previous_action == 3:
            return 2

    def reflash_map(self, generate_food=False):
        """
        Refresh the map.

        : param generate_food: (bool) 刷新地圖時是否產生食物
        """
        if 'map_data' in self.__dict__:
            del self.map_data
        self.map_data = utils.generate_map(self.high, self.width)
        self.map_data = utils.reflash_map(self.map_data, self.snake_position)
        if generate_food:
            self.food_position = utils.generate_food(self.map_data)
        self.map_data = utils.reflash_map(self.map_data, self.snake_position, self.food_position)
