from enum import Enum

class MapEnum(Enum):
    """
    Define the symbol represented by each object in the map.
    """
    space = ' '
    wall = 'X'
    galaxian = 'G'
    enemy = 'E'
    bullet = 'o'
    bonus = 'B'

class MapObsEnum(Enum):
    """
    Define the symbol represented by each object in the input of the neural network.
    """
    space = 0
    wall = 1
    galaxian = 2
    enemy = 3
    bullet = 4
    bonus = 5