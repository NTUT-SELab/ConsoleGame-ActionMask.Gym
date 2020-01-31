import numpy as np

from env.Snake import utils
from env.Snake.base_env import BaseEnv
from env.Snake.map_define import MapEnum

class ActionMaskEnv(BaseEnv):
    """
    A snake environment. (For action mask)

    : param high:   (int) 地圖高度
    : param width:  (int) 地圖寬度
    : end_step:     (int) 遊戲最長步數
    """
    def __init__(self, high=50, width=40, end_step=10000):
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
        action_mask = np.asarray([1, 1, 1, 1])

        if is_done:
            return action_mask

        # 這次動作的相反動作屬於無效動作
        odopa = self.compute_opposite_direction_of_previous_action()
        action_mask[odopa] = 0

        if utils.get_target_obj(self.map_data, 0) == MapEnum.wall or utils.get_target_obj(self.map_data, 0) == MapEnum.body:
            action_mask[0] = 0
        if utils.get_target_obj(self.map_data, 1) == MapEnum.wall or utils.get_target_obj(self.map_data, 1) == MapEnum.body:
            action_mask[1] = 0
        if utils.get_target_obj(self.map_data, 2) == MapEnum.wall or utils.get_target_obj(self.map_data, 2) == MapEnum.body:
            action_mask[2] = 0
        if utils.get_target_obj(self.map_data, 3) == MapEnum.wall or utils.get_target_obj(self.map_data, 3) == MapEnum.body:
            action_mask[3] = 0

        if np.count_nonzero(action_mask == 0) == 4:
            del action_mask
            action_mask = np.asarray([1, 1, 1, 1])
            action_mask[odopa] = 0

        return action_mask
