import gym
import numpy as np
from .map import Map
from .game import GhostRules, GameState
from .ghost_agent import DirectionalGhost


class BaseEnv(gym.Env):
    """
    A pacman environment.

    : param map_name: (str) 要運行的地圖和相關資訊
    : param end_step: (int) 每個回合，最多可運行的步數
    """
    def __init__(self, map_name='default_map', end_step=10000):
        self.map = Map(map_name)
        self.end_step = end_step
        self.state = GameState(self.map)
        self.ghostAgents = [
            DirectionalGhost(i)
            for i in range(1, len(self.state.getNumAgents()))
        ]
        self.action_space = gym.spaces.Discrete(4)
        self.obs_shape = (self.map.shape[0], self.map.shape[1], 1)
        self.observation_space = gym.spaces.Box(low=0,
                                                high=5,
                                                shape=self.obs_shape,
                                                dtype=np.float16)

    def reset(self):
        """
        Reset environment.
        """
        self.state_cache = self.state.deepCopy()
        self.current_step = 0
        return Map.toObservation(self.map_cache, self.obs_shape)

    def step(self, action):
        """
        Tell the environment which action to do.

        : param action: (int) 要執行的動作
        """
        direction = Actions.getActionWithIndex(action)
        reward = self.get_reward(direction)
        done = self.is_done()

        obs = self.state_cache.toObservation(self.obs_shape)
        self.current_step += 1

        return obs, reward, done, {}

    def render(self, delay_time=1):
        """
        Print environment.

        : param delay_time: (float) 每次打印要延遲的時間
        """
        pass

    def get_reward(self, action):
        """
        Give rewards based on actions state.

        """
        self.state_cache.scoreChange = 0

        for ghost in self.ghostAgents:
            GhostRules.applyAction(ghost.getAction(self.state_cache))
            GhostRules.decrementTimer(
                self.state_cache.getGhostState(ghost.index))

        self.state_cache = self.state_cache.generateSuccessor(0, action)
        return self.state_cache.scoreChange

    def is_done(self):
        """
        Check if this round is over.

        : param target_obj: (MapEnum) 老鼠前方ㄧ格的物件
        """
        return self.current_step >= self.end_step or self.state_cache.isWin(
        ) or self.state_cache.isLose()
