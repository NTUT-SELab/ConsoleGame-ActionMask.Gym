import numpy as np
import random as rnd

from env.MagicKey.map_define import MapEnum, MapObsEnum
from env.MagicKey.map_element import *

def generate_texts_to_map(map):
    """
    The starting position of the galaxian.
    """
    
    for _ in range(5):
        map.refresh()
        #Random choose starting point for max size of 3x3 texts, -1 = right end, 3 = space
        start_point = rnd.randint(1, map.width - 1 - 3)
        high = width = rnd.randint(1, 3)
        text_ele = None
        #Generate text ballon
        if is_enough_space(start_point, width, high, map):
            text_ele = TextBallon([1, start_point], (1, high, width))
        #Not enough space for text ballon, generate bonus or weapon
        elif is_enough_space(start_point, 3, 1, map):
            size = (1, 1, 3)
            left_texts_quantity = sum([ele.left_reward for ele in map.elements])
            #Generate text weapon or not
            if left_texts_quantity > 0.3*map.high and \
                len(np.where(map.data == MapEnum.weapon_edge.value)[0]) < 4:
                text_ele = TextWeapon([1, start_point], size)
            #Generate text bonus or not
            elif len(np.where(map.data == MapEnum.bonus_edge.value)[0]) < 2:    
                text_ele = TextBonus([1, start_point], size)

        if text_ele is not None:
            map.add_element(text_ele)
            map.refresh()

def is_enough_space(start_point, width, high, map):
    return (map.data[1:1 + high + 2, start_point - 1:start_point + width + 2] == ' ').all()

def apply_action(map, action):
    if action < 26:
        remove_key(map, action)
    elif action == 26:
        map.eliminate_texts_by_weapon()
    map.wizard.shoot(action)

def remove_key(map, action):
    #agent action sapce: 0~26
    if action > 25:
        return
    key = chr(action+65)
    [ballon.remove(key) for ballon in map.elements]
    

def move_text_elements(map, score):
    max_steps = int(score/200) + 1
    max_steps = 3 if max_steps > 3 else max_steps
    steps = rnd.randint(1, max_steps)
    [element.move(steps) for element in map.elements]

def map_to_obs(map_data, shape):
    """
    Convert map data to neural network input formate.

    : param map_data:   (list)      整張地圖的集合
    : param shape:      (obs_shape) 神經網路輸入的形狀
    """
    map_data = map_data.copy().astype('<U3')
    text_pos =  (np.where(np.char.isalpha(map_data)))
    for i in range(len(text_pos[0])):
        map_data[text_pos[0][i], text_pos[1][i]] = ord(map_data[text_pos[0][i], text_pos[1][i]]) - 65
    
    map_data[map_data == MapEnum.space.value] = MapObsEnum.space.value
    map_data[map_data == MapEnum.wall.value] = MapObsEnum.wall.value
    map_data[map_data == MapEnum.ballon_vedge.value] = MapObsEnum.ballon_vedge.value
    map_data[map_data == MapEnum.ballon_hedge.value] = MapObsEnum.ballon_hedge.value
    map_data[map_data == MapEnum.bonus_edge.value] = MapObsEnum.bonus_edge.value
    map_data[map_data == MapEnum.weapon_edge.value] = MapObsEnum.weapon_edge.value
    map_data[map_data == MapEnum.line_of_defense.value] = MapObsEnum.line_of_defense.value
    map_data[map_data == MapEnum.wizard.value] = MapObsEnum.wizard.value

    for power in range(1, 7):
        map_data[map_data == str(power)] = int(power) + 34

    return np.reshape(map_data.astype(np.float16), shape)


