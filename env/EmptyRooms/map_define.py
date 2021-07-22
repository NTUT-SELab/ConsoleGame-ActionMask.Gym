from enum import Enum

class MapEnum(Enum):
    """
    Define the symbol represented by each object in the map.
    """
    road = ' '
    wall = 'X'
    mouse = 'M'
    exit = 'E'

class MapObsEnum(Enum):
    """
    Define the symbol represented by each object in the input of the neural network.
    """
    road = 0
    wall = 1
    mouse = 2
    exit = 3

