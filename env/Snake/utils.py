import numpy as np
import random as rnd

from env.Snake.map_define import MapEnum, MapObsEnum

def generate_map(high, width):
    map = np.full((high, width), MapEnum.road.value)
    map[0] = MapEnum.wall.value
    map[high - 1] = MapEnum.wall.value
    map[:, 0] = MapEnum.wall.value
    map[:, width - 1] = MapEnum.wall.value

    return map

def generate_snake():
    snake_position = [[3, 1], [2, 1], [1, 1]]
    return snake_position

def generate_food(map):
    road_coordinate = np.where(map == MapEnum.road.value)
    food_position = rnd.randint(0, len(road_coordinate[0]) - 1)
    return [road_coordinate[0][food_position], road_coordinate[1][food_position]]

def reflash_map(map, snake_position, food_position=None):
    map[map == MapEnum.head.value ] = ' '
    map[map == MapEnum.body.value ] = ' '
    map[snake_position[0][0]][snake_position[0][1]] = MapEnum.head.value
    for body_index in range(1, len(snake_position)):
        map[snake_position[body_index][0]][snake_position[body_index][1]] = MapEnum.body.value

    if food_position is not None:
        map[food_position[0], food_position[1]] = MapEnum.food.value

    return map