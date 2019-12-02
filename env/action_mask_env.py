from env import utils
from env.base_env import BaseEnv
from env.map_define import MapEnum

class ActionMaskEnv(BaseEnv):
    def __init__(self, map_name='default_map', end_step=1000):
        super().__init__(map_name=map_name, end_step=end_step)

    def step(self, action):
        obs, reward, done, _ = super().step(action)
        action_mask = self.compute_action_mask()
        return obs, reward, done, {'action_mask': action_mask}

    def compute_action_mask(self):
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
