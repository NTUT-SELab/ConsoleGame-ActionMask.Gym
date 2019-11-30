from enum import Enum

class MapEnum(Enum):
    road = ' '
    wall = 'X'
    exit = 'E'
    mouse = 'M'
    food = 'F'
    poison = 'P'

class MapObsEnum(Enum):
    road = 0
    wall = 1
    exit = 2
    mouse = 3
    food = 4
    poison = 5
