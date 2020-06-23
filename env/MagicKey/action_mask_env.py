import numpy as np

from env.MagicKey import utils
from env.MagicKey.base_env import BaseEnv
from env.MagicKey.map_define import MapEnum

class ActionMaskEnv(BaseEnv):
    """
    A snake environment. (For action mask)

    : param high:   (int) 地圖高度
    : param width:  (int) 地圖寬度
    : end_step:     (int) 遊戲最長步數
    """
    def __init__(self, high=30, width=20, end_step=10000):
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
        action_mask = np.zeros(27)
        
        if is_done:
            return np.ones(27)

        active_action = []
        for i in range(65,91):
            [active_action.append(i-65) if (chr(i) in element.texts) & (element.is_game_end()) \
                                        else None for element in self.map.elements]
        
        if self.map.data[self.map.high-2, 1] != ' ':
            active_action.append(26)

        for action in active_action:
            action_mask[action] = 1

        if np.count_nonzero(action_mask == 0) == 27:
            del action_mask
            action_mask = np.ones(27)
        action_mask = np.asarray(action_mask)
        return action_mask