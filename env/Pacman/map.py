import os
import numpy as np
from env.Pacman.map_define import MapEnum


class Map:
    """
    A map environment.

    Load map from maps folder.
         % - Wall
         . - Food
         o - Capsule
         G - Ghost
         P - Pacman
    : param map_name: (str) 地圖檔案名稱
    : param ghost_num: (int) 鬼的數量
    """
    def __init__(self, map_name):
        self.get_map(map_name)

    def get_map(self, map_name):
        maps_path = os.path.join(os.getcwd(), 'maps', 'PacmanMaze')
        map_file = os.path.join(maps_path, map_name)

        map_buffer = None
        with open(map_file, 'r') as f:
            map_buffer = np.asarray(f.read().splitlines(), dtype='c')
            map_buffer = map_buffer.astype(str)
        self._map = self.check_map(map_buffer)
        self.width = len(self.map[0])
        self.height = len(self.map)

    def check_map(self, map_data):
        """
        Check map file integrity.

        : param map_data: (list) 整張地圖的集合
        """
        if len(map_data.shape) != 2:
            raise Exception('The map shape must be a rectangle.')
        if np.count_nonzero(map_data == MapEnum.wall.value) == 0:
            raise Exception('There are no wall in the map.')
        if np.count_nonzero(map_data == MapEnum.ghost.value) == 0:
            raise Exception('There are no ghost in the map.')
        if np.count_nonzero(map_data == MapEnum.pacman.value) == 0:
            raise Exception('There are no pacman in the map.')

        if np.count_nonzero(
                map_data.T[0] == MapEnum.wall.value) != map_data.shape[0]:
            raise Exception('There are holes in the left side of the map.')
        if np.count_nonzero(
                map_data.T[-1] == MapEnum.wall.value) != map_data.shape[0]:
            raise Exception('There are holes in the left side of the map.')
        if np.count_nonzero(
                map_data[0] == MapEnum.wall.value) != map_data.shape[1]:
            raise Exception('There are holes in the upper side of the map.')
        if np.count_nonzero(
                map_data[-1] == MapEnum.wall.value) != map_data.shape[1]:
            raise Exception('There are holes in the lower side of the map.')

        return map_data

    def reset(self):
        """
        Reset map.
        """
        self.map_cache = np.copy(self._map)
