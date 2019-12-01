from env.base_env import BaseEnv
from env.map_define import MapEnum

class NegativeRewardEnv(BaseEnv):

    def __init__(self, map_name='default_map', end_step=1000):
        super().__init__(map_name=map_name, end_step=end_step)

    def get_reward(self, target_obj):

        if target_obj == MapEnum.food:
            return 1
        elif target_obj == MapEnum.poison:
            return -1
        elif target_obj == MapEnum.exit:
            return 2
        elif target_obj == MapEnum.wall:
            return -5
        else:
            return 0
