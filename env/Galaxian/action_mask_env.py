import numpy as np
from env.Galaxian import utils
from env.Galaxian.base_env import BaseEnv
from env.Galaxian.map_define import MapEnum

class ActionMaskEnv(BaseEnv):
    """
    A snake environment. (For action mask)

    : param high:   (int) 地圖高度
    : param width:  (int) 地圖寬度
    : end_step:     (int) 遊戲最長步數
    """
    def __init__(self, high=30, width=30, end_step=10000):
        super().__init__(high, width, end_step)

    def step(self, action):
        """
        Tell the environment which action to do.

        : param action: (int) 要執行的動作
        """
        obs, reward, done, _ = super().step(action)
        action_mask = self.compute_action_mask(done)
        return obs, reward, done, {'action_mask': action_mask}

    def compute_action_mask(self, is_done):
        """
        Compute the set of action masks based on the current state
        """
        action_mask = np.asarray([1, 1])
        right_end = self.map.width - 2
        left_end = 1   
        if is_done:
            return action_mask

        if self.galaxian.get_position()[1] == left_end:
            action_mask[0] = 0
        if self.galaxian.get_position()[1] == right_end:
            action_mask[1] = 0

        if np.count_nonzero(action_mask == 0) == 2:
            del action_mask
            action_mask = np.asarray([1, 1])

        return action_mask