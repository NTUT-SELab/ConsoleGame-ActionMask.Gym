from env.EmptyRooms import utils
from env.EmptyRooms.base_env import BaseEnv
from env.EmptyRooms.map_define import MapEnum

class ActionMaskEnv(BaseEnv):
    """
    A mouse walking maze environment. (For action mask)

    : param map_name: (str) 要運行的地圖和相關資訊
    : param end_step: (int) 每個回合，最多可運行的步數
    """
    def __init__(self, end_step=1000):
        super().__init__(end_step=end_step)

    def step(self, action):
        """
        Tell the environment which action to do.

        : param action: (int) 要執行的動作
        """
        obs, reward, done, _ = super().step(action)
        action_mask = self.compute_action_mask()
        return obs, reward, done, {'action_mask': action_mask}

    def compute_action_mask(self):
        """
        Compute the set of action masks based on the current state
        """
        action_mask = [1, 1, 1, 1]
        
        if utils.get_target_obj(self.map_cache, 0) == MapEnum.wall:
            action_mask[0] = 0
        if utils.get_target_obj(self.map_cache, 1) == MapEnum.wall:
            action_mask[1] = 0
        if utils.get_target_obj(self.map_cache, 2) == MapEnum.wall:
            action_mask[2] = 0
        if utils.get_target_obj(self.map_cache, 3) == MapEnum.wall:
            action_mask[3] = 0

        return action_mask
