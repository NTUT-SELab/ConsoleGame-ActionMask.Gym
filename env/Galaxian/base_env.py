import gym
import os
import time
import numpy as np
import threading

from env.Galaxian import utils
from env.Galaxian.map_define import *
from env.Galaxian.map import Map

class BaseEnv(gym.Env):
    """
    A snake environment.

    : param high:   (int) 地圖高度
    : param width:  (int) 地圖寬度
    : end_step:     (int) 遊戲最長步數
    """
    def __init__(self, high=30, width=30, end_step=10000):
        self.map = Map(high, width)
        self.end_step = end_step

        if high < 10 or width < 10 :
            raise Exception('地圖的高度與寬度必須 > 10')
        
        self.action_space = gym.spaces.Discrete(2)
        self.obs_shape = (high, width, 1)
        self.observation_space = gym.spaces.Box(low=0, high=5, shape=self.obs_shape, dtype=np.float16)

    def reset(self):
        """
        Reset environment.
        """
        self.map.generate_data()
        self.galaxian = utils.generate_galaxian(self.map)
        self.bonus = utils.generate_bonus(self.map)
        self.enemies = utils.generate_enemies(self.map)
        self.bullets = []
        self.map.add_element(self.galaxian)
        self.map.add_element(self.bonus)
        self.map.add_elements(self.enemies)
        self.previous_enemy_numbers = len(self.enemies)
        self.refresh_map()
        self.current_step = 0
        self.score = 0

        return utils.map_to_obs(self.map.data, self.obs_shape)

    def step(self, action):
        """
        Tell the environment which action to do.

        : param action: (int) 要執行的動作
        """

        reward = self.get_reward()
        done = self.is_done()
        self.previous_enemy_numbers = len(self.enemies)
        self.galaxian.move(action)
        self.bonus.reactivate()
        self.bonus.move()
        self.bullets.append(self.galaxian.fire())
        self.move_enemies()
        self.move_bullets()
        self.refresh_map()
        obs = utils.map_to_obs(self.map.data, self.obs_shape)
        self.current_step += 1
        self.score += self.get_reward()

        return obs, reward, done, {}

    def render(self, delay_time=0.5, pause=False):
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
        bonus_reward = 0
        catch_reward = 0
        enemies_reward = self.previous_enemy_numbers - len(self.enemies)
        
        if not self.bonus.is_active():
            bonus_reward = 5
        
        if self.is_enemy_catch_galaxian():
            catch_reward = -10
            
        reward = bonus_reward + catch_reward + enemies_reward
        return reward

    def is_done(self):
        """
        Check if this round is over.

        : param target_obj: (MapEnum) 老鼠前方ㄧ格的物件
        """

        return self.current_step >= self.end_step or self.is_enemy_catch_galaxian()\
                    or len(self.enemies) == 0

    def refresh_map(self):
        """
        Refresh the map.

        : param generate_food: (bool) 刷新地圖時是否產生食物
        """
        self.map.refresh()
        utils.disable_rewarded_enemies_and_bullets(self.bullets, self.enemies, self.map.data)
        utils.disable_rewarded_bonus_and_bullet(self.bullets, self.bonus)
        utils.remove_disable_elements(self.bullets)
        utils.remove_disable_elements(self.enemies)

        self.map.clear_elements()
        self.map.add_element(self.galaxian)
        self.map.add_element(self.bonus)
        self.map.add_elements(self.bullets)
        self.map.add_elements(self.enemies)
        self.map.refresh()
        
    def move_bullets(self):
        for bullet in self.bullets:
            bullet.move()
    
    def move_enemies(self):
        for enemy in self.enemies:
            enemy.move()

    def is_enemy_catch_galaxian(self):
        for enemy in self.enemies:
            if enemy.get_position()[0] == self.galaxian.get_position()[0]:
                return True
        return False

    def map_to_string(self):
        state = ''
        for rows in self.map.data:
            state += ' '.join(rows) + '\n'
        return state