from env.Pacman.base_env import BaseEnv
import gym
import numpy as np
from env.Pacman.game import Directions, Actions


class NewObsEnv(BaseEnv):
    """
    A pacman environment. (For action mask)
    : param map_name: (str) 要運行的地圖和相關資訊
    : param end_step: (int) 每個回合，最多可運行的步數
    """

    def __init__(self, map_name='default_map', end_step=1000):
        super().__init__(map_name=map_name, end_step=end_step)
        self.obs_shape = (self.state.layout.width, self.state.layout.height, 6)
        self.observation_space = gym.spaces.Box(low=0, high=1, shape=self.obs_shape, dtype=np.float16)

    def reset(self):
        """
        Reset environment.
        """
        self.state_cache = self.state.deepCopy()
        self.current_step = 0

        return self.state_cache.toObservationMatrix()

    def step(self, action):
        """
        Tell the environment which action to do.

        : param action: (int) 要執行的動作
        """
        direction = Actions.getActionWithIndex(action)
        self.apply_action(direction)
        reward = self.get_reward()
        done = self.is_done()

        obs = self.state_cache.toObservationMatrix()
        self.current_step += 1

        return obs, reward, done, {}
