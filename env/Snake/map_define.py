from enum import Enum

class MapEnum(Enum):
    """
    Define the symbol represented by each object in the map.
    """
    road = ' '
    wall = '✤'
    head = '❖'
    body = '◉'
    food = '❦'

class MapObsEnum(Enum):
    """
    Define the symbol represented by each object in the input of the neural network.
    """
    road = 0
    wall = 1
    head = 2
    body = 3
    food = 4
