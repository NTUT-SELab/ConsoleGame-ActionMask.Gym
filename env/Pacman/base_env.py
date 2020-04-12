import gym
import numpy as np
import os, time
from env.Pacman.map import Map
from env.Pacman.game import GhostRules, GameState, Actions
from env.Pacman.ghost_agent import DirectionalGhost, RandomGhost
import threading


class BaseEnv(gym.Env):
    """
    A pacman environment.

    : param map_name: (str) 要運行的地圖和相關資訊
    : param end_step: (int) 每個回合，最多可運行的步數
    """
    def __init__(self, map_name='default_map', end_step=1000):
        self.map = Map(map_name)
        self.end_step = end_step
        self.state = GameState(self.map)
        self.ghostAgents = [DirectionalGhost(i) for i in range(1, self.state.getNumAgents())]
        self.action_space = gym.spaces.Discrete(4)
        self.obs_shape = (self.map.shape[0], self.map.shape[1], 1)
        self.observation_space = gym.spaces.Box(low=0, high=6, shape=self.obs_shape, dtype=np.float16)
        self.reset()

    def reset(self):
        """
        Reset environment.
        """
        self.state_cache = self.state.deepCopy()
        self.current_step = 0

        return self.state_cache.toObservation(self.obs_shape)

    def step(self, action):
        """
        Tell the environment which action to do.

        : param action: (int) 要執行的動作
        """
        direction = Actions.getActionWithIndex(action)
        self.apply_action(direction)
        reward = self.get_reward()
        done = self.is_done()

        obs = self.state_cache.toObservation(self.obs_shape)
        self.current_step += 1

        return obs, reward, done, {}

    def render(self, delay_time=0.5):
        """
        Print environment.

        : param delay_time: (float) 每次打印要延遲的時間
        """
        # for windows
        if os.name == 'nt':
            _ = os.system('cls')
        # for mac and linux(here, os.name is 'posix')
        else:
            _ = os.system('clear')

        print(self.state_cache)
        print('score: {}'.format(self.state_cache.score))
        time.sleep(delay_time)

    def get_reward(self):
        """
        Give rewards based on actions state.

        """
        return self.state_cache.scoreChange

    def apply_action(self, action):
        self.state_cache.scoreChange = 0

        self.state_cache = self.state_cache.generateSuccessor(0, action)

        for ghost in self.ghostAgents:
            if not self.is_done():
                self.state_cache = self.state_cache.generateSuccessor(ghost.index, ghost.getAction(self.state_cache))

    def is_done(self):
        """
        Check if this round is over.

        """
        return self.current_step >= self.end_step or self.state_cache.isWin() or self.state_cache.isLose()

    def play(self):
        from pynput import keyboard
        from pynput.keyboard import Listener
        self.action = 3

        t = threading.Thread(target=self.listener)
        t.daemon = True
        t.start()

        while (True):
            self.reset()
            while (not self.is_done()):
                self.step(self.action)
                self.render()
            print("Your score: {}".format(self.state_cache.score))
            time.sleep(5)

    def listener(self):
        def on_press(key):
            global currently_pressed_key
            if key == Key.up:
                self.action = 0
            elif key == Key.down:
                self.action = 1
            elif key == Key.right:
                self.action = 2
            elif key == Key.left:
                self.action = 3

        with Listener(on_press=on_press) as l:
            l.join()
