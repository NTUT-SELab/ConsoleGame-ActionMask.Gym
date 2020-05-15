import os
import numpy as np
from env.Pacman.map_define import MapEnum


class Grid:

    def __init__(self, width, height, initialValue=False):
        if initialValue not in [False, True]:
            raise Exception('Grids can only contain booleans')
        self.width = width
        self.height = height
        self.data = np.array([[initialValue for y in range(height)] for x in range(width)])

    def __getitem__(self, i):
        return self.data[i]

    def __setitem__(self, key, item):
        self.data[key] = item

    def __str__(self):
        out = [[str(self.data[x][y])[0] for x in range(self.width)] for y in range(self.height)]
        out.reverse()
        return '\n'.join([''.join(x) for x in out])

    def __eq__(self, other):
        if other is None:
            return False
        return (self.data == other.data).all()

    def copy(self):
        g = Grid(self.width, self.height)
        g.data = np.array([x[:] for x in self.data])
        return g

    def deepCopy(self):
        return self.copy()

    def shallowCopy(self):
        g = Grid(self.width, self.height)
        g.data = self.data
        return g

    def count(self, item=True):
        return self.data.sum()

    def asList(self, key=True):
        list = []
        for x in range(self.width):
            for y in range(self.height):
                if self[x][y] == key:
                    list.append((x, y))
        return list


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
        self.data = self.check_map(map_buffer)
        self.shape = self.data.shape
        self.map_name = map_name
        self.width = len(self.data[0])
        self.height = len(self.data)
        self.agentPositions = []
        self.pacmanPositions = []
        self.capsules = []
        self.numGhosts = 0
        self.food = Grid(self.width, self.height)
        self.walls = Grid(self.width, self.height)
        self.processLayoutText(self.data)

    def deepCopy(self):
        map = Map(self.map_name)
        map.data = np.copy(self.data)
        map.shape = self.shape
        map.agentPositions = [(i, pos) for i, pos in self.agentPositions]
        map.capsules = [(x, y) for x, y in self.capsules]
        map.numGhosts = self.numGhosts
        map.food = self.food.deepCopy()
        return map

    def processLayoutText(self, layoutText):
        """
        Coordinates are flipped from the input format to the (x,y) convention here
        The shape of the maze.  Each character
        represents a different type of object.
         % - Wall
         . - Food
         o - Capsule
         G - Ghost
         P - Pacman
        Other characters are ignored.
        """
        maxY = self.height - 1
        for y in range(self.height):
            for x in range(self.width):
                layoutChar = layoutText[maxY - y][x]
                self.processLayoutChar(x, y, layoutChar)

        self.agentPositions.append(self.pacmanPositions[np.random.choice(np.arange(len(self.pacmanPositions)))])
        self.agentPositions.sort()
        self.agentPositions = [(i == 0, pos) for i, pos in self.agentPositions]
        x, y = self.agentPositions[0][1]
        self.food[x][y] = False

    def processLayoutChar(self, x, y, layoutChar):
        if layoutChar == '%':
            self.walls[x][y] = True
        elif layoutChar == '.':
            self.food[x][y] = True
        elif layoutChar == 'o':
            self.capsules.append((x, y))
        elif layoutChar == 'P':
            self.food[x][y] = True
            self.pacmanPositions.append((0, (x, y)))
        elif layoutChar in ['G']:
            self.agentPositions.append((1, (x, y)))
            self.numGhosts += 1

    def __str__(self):
        out = [[str(self.data[y][x])[0] for x in range(self.width)] for y in range(self.height)]
        return '\n'.join([''.join(x) for x in out])

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

        if np.count_nonzero(map_data.T[0] == MapEnum.wall.value) != map_data.shape[0]:
            raise Exception('There are holes in the left side of the map.')
        if np.count_nonzero(map_data.T[-1] == MapEnum.wall.value) != map_data.shape[0]:
            raise Exception('There are holes in the right side of the map.')
        if np.count_nonzero(map_data[0] == MapEnum.wall.value) != map_data.shape[1]:
            raise Exception('There are holes in the upper side of the map.')
        if np.count_nonzero(map_data[-1] == MapEnum.wall.value) != map_data.shape[1]:
            raise Exception('There are holes in the lower side of the map.')

        return map_data

    def isWall(self, pos):
        x, col = pos
        return self.walls[x][col]

    def reset(self):
        """
        Reset map.
        """
        map_cache = np.copy(self.data)
        self.get_map(self.map_name)
        return map_cache
