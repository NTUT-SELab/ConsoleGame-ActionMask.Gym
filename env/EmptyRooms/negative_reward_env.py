from env.MouseWalkingMaze.base_env import BaseEnv
from env.MouseWalkingMaze.map_define import MapEnum

class NegativeRewardEnv(BaseEnv):
    """
    A mouse walking maze environment. (For negative reward)

    : param map_name: (str) 要運行的地圖和相關資訊
    : param end_step: (int) 每個回合，最多可運行的步數
    """
    def __init__(self, map_name='default_map', end_step=1000):
        super().__init__(map_name=map_name, end_step=end_step)

    def get_reward(self, target_obj):
        """
        Give relative rewards based on mouse actions.

        : param target_obj: (MapEnum) 老鼠前方ㄧ格的物件
        """
        if target_obj == MapEnum.food:
            return 2
        elif target_obj == MapEnum.poison:
            return -1
        elif target_obj == MapEnum.exit:
            return 1
        elif target_obj == MapEnum.wall:
            return -5
        else:
            return 0
