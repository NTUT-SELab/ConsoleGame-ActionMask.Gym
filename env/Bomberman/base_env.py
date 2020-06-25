import gym
import os
import time
import numpy as np
from env.Bomberman.game import GameState, Actions
from env.Bomberman.map import Map
from env.Bomberman.enemy import EnemyAgents


class BaseEnv(gym.Env):
    """
    A bomberman environment.

    : param map_name: (str) 要運行的地圖和相關資訊
    : param end_step: (int) 每個回合，最多可運行的步數
    """

    def __init__(self, map_name='default_map', end_step=1000):
        self.map = Map(map_name)
        self.state = GameState(self.map)
        self.end_step = end_step
        self.action_space = gym.spaces.Discrete(6)
        # for to_observation()
        # self.obs_shape = (self.map.width, self.map.height, 8)
        # for to_observation_(shape)
        self.obs_shape = (self.map.shape[0], self.map.shape[1], 1)
        self.observation_space = gym.spaces.Box(low=0, high=8, shape=self.obs_shape, dtype=np.int8)
        self.reset()

    def reset(self):
        """
        Reset environment.
        """
        self.state.reset()
        self.current_step = 0

        return self.state.to_observation_(self.obs_shape)

    def step(self, action_index):
        """
        Tell the environment which action to do.

        : param action: (int) 要執行的動作
        """
        action = Actions.get_action_with_index(action_index)
        self.apply_action(action)
        reward = self.get_reward()
        if action == 'Bomb':
            reward = 0.01
        done = self.is_done()

        obs = self.state.to_observation_(self.obs_shape)
        self.current_step += 1

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

        print(self.state)
        print('score: {}'.format(self.state.score) if not pause else "Pause")
        time.sleep(delay_time)

    def get_reward(self):
        """
        Give rewards based on actions state.

        """
        _reward = 0

        for reward in self.state.score_item:
            if reward == 10:
                _reward += 10.  # Blow up brick

            elif reward == 200:
                _reward += 20.  # Kill enemy

            elif reward < -10:
                _reward += -50.  # Dead  (Ouch!) -500

            elif reward == 500:
                _reward += 50.  # Win kill all enemies

        if _reward == 0:
            _reward = -0.01  # Punish time (Pff..)

        return _reward

    def apply_action(self, action):
        if action != 'Bomb':
            for index in range(1, len(self.state.agent_states)):
                if not self.is_done():
                    self.state.generate_successor(index, EnemyAgents.get_action(index, self.state))

        if not self.is_done():
            self.state.generate_successor(0, action)

    def is_done(self):
        """
        Check if this round is over.

        """
        return self.current_step >= self.end_step or self.state.is_win() or self.state.is_lose()
