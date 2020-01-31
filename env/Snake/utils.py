import numpy as np
import random as rnd

from env.Snake.map_define import MapEnum, MapObsEnum

def generate_map(high, width):
    """
    Generate map wall.

    : param high:   (int)   地圖高度
    : param width:  (int)   地圖寬度
    """
    map_data = np.full((high, width), MapEnum.road.value)
    map_data[0] = MapEnum.wall.value
    map_data[high - 1] = MapEnum.wall.value
    map_data[:, 0] = MapEnum.wall.value
    map_data[:, width - 1] = MapEnum.wall.value

    return map_data

def generate_snake():
    """
    The starting position of the snake.
    """
    snake_position = [[3, 1], [2, 1], [1, 1]]
    return snake_position

def generate_food(map_data):
    """
    Random produce food locations.

    : param map_data:  (list)  地圖
    """
    road_coordinate = np.where(map_data == MapEnum.road.value)
    food_position = rnd.randint(0, len(road_coordinate[0]) - 1)
    return [road_coordinate[0][food_position], road_coordinate[1][food_position]]

def reflash_map(map_data, snake_position, food_position=None):
    """
    Merge map data.

    : param map_data:           (list)          地圖
    : param snake_position:     (list)          蛇的位置(全身)
    : param food_position:      (int array)     食物的位置
    """
    if food_position is not None:
        map_data[food_position[0], food_position[1]] = MapEnum.food.value
        return map_data

    map_data[map_data == MapEnum.head.value ] = ' '
    map_data[map_data == MapEnum.body.value ] = ' '
    map_data[snake_position[0][0]][snake_position[0][1]] = MapEnum.head.value
    for body_index in range(1, len(snake_position)):
        map_data[snake_position[body_index][0]][snake_position[body_index][1]] = MapEnum.body.value

    return map_data

def map_to_obs(map_data, shape):
    """
    Convert map data to neural network input formate.

    : param map_data:   (list)      整張地圖的集合
    : param shape:      (obs_shape) 神經網路輸入的形狀
    """
    map_data = map_data.copy()
    map_data[map_data == MapEnum.road.value] = MapObsEnum.road.value
    map_data[map_data == MapEnum.wall.value] = MapObsEnum.wall.value
    map_data[map_data == MapEnum.head.value] = MapObsEnum.head.value
    map_data[map_data == MapEnum.body.value] = MapObsEnum.body.value
    map_data[map_data == MapEnum.food.value] = MapObsEnum.food.value

    return np.reshape(map_data.astype(np.float16), shape)

def get_target_obj(map_data, action):
    """
    Get the objects that the snake will encounter after moving.

    : param action: (int) 要執行的動作
    """
    snake_head_position = get_snake_head_position(map_data)
    target_position = get_target_position(snake_head_position, action)

    return MapEnum(map_data[target_position[0]][target_position[1]])

def get_snake_head_position(map_data):
    """
    Get the current coordinate of the snake.

    : param map_data: (list) 整張地圖的集合
    """
    position = np.where(map_data == MapEnum.head.value)
    position = np.asarray(position)
    
    return position.ravel()

def get_target_position(snake_head_position, action):
    """
    Get the target coordinate of the snake to be moved.

    : param action: (int) 要執行的動作
    """
    # Up
    if action == 0:
        target_position = [snake_head_position[0] - 1, snake_head_position[1]]
    # Down
    if action == 1:
        target_position = [snake_head_position[0] + 1, snake_head_position[1]]
    # Left
    if action == 2:
        target_position = [snake_head_position[0], snake_head_position[1] - 1]
    # Right
    if action == 3:
        target_position = [snake_head_position[0], snake_head_position[1] + 1]

    return target_position
