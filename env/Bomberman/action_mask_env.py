from env.Bomberman.base_env import BaseEnv
from env.Bomberman.game import Directions


class ActionMaskEnv(BaseEnv):
    """
    A bomberman environment. (For action mask)
    : param map_name: (str) 要運行的地圖和相關資訊
    : param end_step: (int) 每個回合，最多可運行的步數
    """

    def __init__(self, map_name='default_map', end_step=1000):
        super().__init__(map_name=map_name, end_step=end_step)

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
        action_mask = [1, 1, 1, 1, 1, 1]
        legal = self.state.get_legal_actions(0, True)

        if Directions.NORTH not in legal:
            action_mask[0] = 0

        if Directions.SOUTH not in legal:
            action_mask[1] = 0

        if Directions.EAST not in legal:
            action_mask[2] = 0

        if Directions.WEST not in legal:
            action_mask[3] = 0

        if Directions.STOP not in legal:
            action_mask[4] = 0

        if 'Bomb' not in legal:
            action_mask[5] = 0

        if 1 not in action_mask:
            action_mask = [1, 1, 1, 1, 1, 1]

        return action_mask
