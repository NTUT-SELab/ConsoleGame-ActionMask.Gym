from enum import Enum


class MapEnum(Enum):
    """
    Define the symbol represented by each object in the map.
         % - Wall
         . - Food
         o - Capsule
         G - Ghost
         P - Pacman
    """
    road = ' '
    ghost = 'G'
    wall = '%'
    pacman = 'P'
    capsules = 'o'
    food = '.'


class MapObsEnum(Enum):
    """
    Define the symbol represented by each object in the input of the neural network.
    """
    road = 0
    ghost = 1
    wall = 2
    pacman = 3
    capsules = 4
    food = 5
