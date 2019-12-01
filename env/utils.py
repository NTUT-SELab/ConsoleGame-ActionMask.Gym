import os
import numpy as np

from env.map_define import MapEnum, MapObsEnum

def load_map(map_name):
    maps_path = os.path.join(os.getcwd(), 'maps')
    map_file = os.path.join(maps_path, map_name)

    map_buffer = None
    with open(map_file, 'r') as file:
        map_buffer = np.asarray(file.read().splitlines(), dtype='c')
        map_buffer = map_buffer.astype(str)

    return check_map(map_buffer)
    

def check_map(map_buffer):
    if len(map_buffer.shape) != 2:
        raise Exception('The map shape must be a rectangle.')

    if len(map_buffer) * len(map_buffer[0]) < 12:
        raise Exception('The movable area of ​​the rat must be bigger than 2.')

    if np.count_nonzero(map_buffer == MapEnum.mouse.value) != 1 or np.count_nonzero(map_buffer == MapEnum.exit.value) != 1:
        raise Exception('The map must contain 1 mouse and 1 exit.')

    if np.count_nonzero(map_buffer[0] == MapEnum.wall.value) != map_buffer.shape[1]:
        raise Exception('There are holes in the upper side of the map.')

    if np.count_nonzero(map_buffer[map_buffer.shape[0] - 1] == MapEnum.wall.value) != map_buffer.shape[1]:
        raise Exception('There are holes in the lower side of the map.')

    if np.count_nonzero(map_buffer.T[0] == MapEnum.wall.value) != map_buffer.shape[0]:
        raise Exception('There are holes in the left side of the map.')

    if np.count_nonzero(map_buffer.T[map_buffer.shape[1] - 1] == MapEnum.wall.value) != map_buffer.shape[0]:
        raise Exception('There are holes in the right side of the map.')

    return map_buffer

def map_to_obs(map_data):
    map_data = map_data.copy()
    map_data[map_data == MapEnum.road.value] = MapObsEnum.road.value
    map_data[map_data == MapEnum.wall.value] = MapObsEnum.wall.value
    map_data[map_data == MapEnum.exit.value] = MapObsEnum.exit.value
    map_data[map_data == MapEnum.mouse.value] = MapObsEnum.mouse.value
    map_data[map_data == MapEnum.food.value] = MapObsEnum.food.value
    map_data[map_data == MapEnum.poison.value] = MapObsEnum.poison.value

    return map_data.astype(np.float16)

def get_target_obj(map_data, action):
    mouse_position = get_mouse_position(map_data)
    target_position = get_target_position(mouse_position, action)

    return MapEnum(map_data[target_position[0]][target_position[1]])

def get_mouse_position(map_data):
    position = np.where(map_data == MapEnum.mouse.value)
    position = np.asarray(position)
    
    return position.ravel()

def get_target_position(mouse_position, action):
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
