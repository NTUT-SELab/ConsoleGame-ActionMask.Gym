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
