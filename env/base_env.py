import gym
import numpy as np
import os

class BaseEnv(gym.Env):
    ''' mouse walking maze environment '''

    def __init__(self, map_name='default_map'):
        
        self.map = load_map(map_name)

    @staticmethod
    def load_map(map_name):
        maps_path = os.path.join(os.getcwd(), 'maps')
        map_file = os.path.join(maps_path, map_name)

        map_buffer = None
        with open(map_file, 'r') as file:
            map_buffer = np.asarray(file.read().splitlines(), dtype='c')
            map_buffer = map_buffer.astype(str)

        return BaseEnv.check_map(map_buffer)
        
    @staticmethod
    def check_map(map_buffer):
        if len(map_buffer.shape) != 2:
            raise Exception('The map shape must be a rectangle.')

        if len(map_buffer) * len(map_buffer[0]) < 12:
            raise Exception('The movable area of ​​the rat must be bigger than 2.')

        if np.count_nonzero(map_buffer == 'M') != 1 or np.count_nonzero(map_buffer == 'E') != 1:
            raise Exception('The map must contain 1 mouse and 1 exit.')

        if np.count_nonzero(map_buffer[0] == 'X') != map_buffer.shape[1]:
            raise Exception('There are holes in the upper side of the map.')

        if np.count_nonzero(map_buffer[map_buffer.shape[0] - 1] == 'X') != map_buffer.shape[1]:
            raise Exception('There are holes in the lower side of the map.')

        if np.count_nonzero(map_buffer.T[0] == 'X') != map_buffer.shape[0]:
            raise Exception('There are holes in the left side of the map.')

        if np.count_nonzero(map_buffer.T[map_buffer.shape[1] - 1] == 'X') != map_buffer.shape[0]:
            raise Exception('There are holes in the right side of the map.')

        return map_buffer
