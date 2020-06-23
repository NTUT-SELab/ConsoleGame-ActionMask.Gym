from enum import Enum

class MapEnum(Enum):
    """
    Define the symbol represented by each object in the map.
    """
    space = ' '
    wall = '#'
    ballon_vedge = '|'
    ballon_hedge = '-'
    bonus_edge = '$'
    weapon_edge = '*'
    line_of_defense = '^'
    wizard = '@'




class MapObsEnum(Enum):
    """
    Define the symbol represented by each object in the input of the neural network.
    """
    space = 26
    wall = 27
    ballon_vedge = 28
    ballon_hedge = 29
    bullet = 30
    bonus_edge = 31
    weapon_edge = 32
    line_of_defense = 33
    wizard = 34