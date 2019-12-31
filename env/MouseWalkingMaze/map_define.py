from enum import Enum

class MapEnum(Enum):
    """
    Define the symbol represented by each object in the map.
    """
    road = ' '
    wall = 'X'
    exit = 'E'
    mouse = 'M'
    food = 'F'
    poison = 'P'

class MapObsEnum(Enum):
    """
    Define the symbol represented by each object in the input of the neural network.
    """
    road = 0
    wall = 1
    exit = 2
    mouse = 3
    food = 4
    poison = 5
