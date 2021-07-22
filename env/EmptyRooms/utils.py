import os
import numpy as np
import random as rnd

from env.EmptyRooms.map_define import MapEnum, MapObsEnum

def load_map(map_name):
    """
    Load map from maps folder.

    : param map_name: (str) 地圖檔案名稱
    """
    maps_path = os.path.join(os.getcwd(), 'maps/EmptyRooms')
    map_file = os.path.join(maps_path, map_name)

    map_buffer = None
    with open(map_file, 'r') as file:
        map_buffer = np.asarray(file.read().splitlines(), dtype='c')
        map_buffer = map_buffer.astype(str)
    empty_spaces = np.where(map_buffer == MapEnum.road.value)
    goal = rnd.randint(0,len(empty_spaces[0])-1)
    map_buffer[empty_spaces[0][goal], empty_spaces[1][goal]] = MapEnum.exit.value
    return check_map(map_buffer)

def check_map(map_data):
    """
    Check map file integrity.

    : param map_data: (list) 整張地圖的集合
    """
    if len(map_data.shape) != 2:
        raise Exception('The map shape must be a rectangle.')

    if len(map_data) * len(map_data[0]) < 12:
        raise Exception('The movable area of ​​the rat must be bigger than 2.')

    if np.count_nonzero(map_data == MapEnum.mouse.value) != 1 or np.count_nonzero(map_data == MapEnum.exit.value) != 1:
        raise Exception('The map must contain 1 mouse and 1 exit.')

    if np.count_nonzero(map_data[0] == MapEnum.wall.value) != map_data.shape[1]:
        raise Exception('There are holes in the upper side of the map.')

    if np.count_nonzero(map_data[map_data.shape[0] - 1] == MapEnum.wall.value) != map_data.shape[1]:
        raise Exception('There are holes in the lower side of the map.')

    if np.count_nonzero(map_data.T[0] == MapEnum.wall.value) != map_data.shape[0]:
        raise Exception('There are holes in the left side of the map.')

    if np.count_nonzero(map_data.T[map_data.shape[1] - 1] == MapEnum.wall.value) != map_data.shape[0]:
        raise Exception('There are holes in the right side of the map.')

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
    map_data[map_data == MapEnum.mouse.value] = MapObsEnum.mouse.value
    map_data[map_data == MapEnum.exit.value] = MapObsEnum.road.value

    return np.reshape(map_data.astype(np.float16), shape)

def get_target_obj(map_data, action):
    """
    Get the objects that the mouse will encounter after moving.

    : param action: (int) 要執行的動作
    """
    mouse_position = get_mouse_position(map_data)
    target_position = get_target_position(mouse_position, action)
    # print (map_data)
    return MapEnum(map_data[target_position[0]][target_position[1]])

def get_mouse_position(map_data):
    """
    Get the current coordinate of the mouse.

    : param map_data: (list) 整張地圖的集合
    """
    position = np.where(map_data == MapEnum.mouse.value)
    position = np.asarray(position)
    
    return position.ravel()

def get_target_position(mouse_position, action):
    """
    Get the target coordinate of the mouse to be moved.

    : param action: (int) 要執行的動作
    """
    # Up
    if action == 0:
        target_position = [mouse_position[0] - 1, mouse_position[1]]
    # Down
    if action == 1:
        target_position = [mouse_position[0] + 1, mouse_position[1]]
    # Left
    if action == 2:
        target_position = [mouse_position[0], mouse_position[1] - 1]
    # Right
    if action == 3:
        target_position = [mouse_position[0], mouse_position[1] + 1]

    return target_position
