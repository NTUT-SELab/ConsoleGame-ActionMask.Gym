from enum import Enum


class MapEnum(Enum):
    """
    Define the symbol represented by each object in the map.
         % - Wall
         # - Brick
         E - Enemy
         B - Bomberman
    """
    road = ' '
    enemy = 'E'
    wall = '%'
    brick = '#'
    bomberman = 'B'
    bomb3 = 'o'
    bomb2 = '0'
    bomb1 = 'O'
    bomb0 = '*'


class MapObsEnum(Enum):
    """
    Define the symbol represented by each object in the input of the neural network.
    """
    road = 0
    enemy = 1
    wall = 2
    brick = 3
    bomberman = 4
    bomb3 = 5
    bomb2 = 6
    bomb1 = 7
    bomb0 = 8
