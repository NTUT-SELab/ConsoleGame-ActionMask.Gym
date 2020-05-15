import numpy as np
import random as rnd

from env.Galaxian.map_define import MapEnum, MapObsEnum
from env.Galaxian.map_element import *

def generate_galaxian(map):
    """
    The starting position of the galaxian.
    """
    high = map.high
    width = map.width

    map_bottom = high - 2
    map_center = int(width / 2)
    position = [map_bottom, map_center]
    galaxian = Galaxian(position, high, width)

    return galaxian

def generate_enemies(map):
    """
    Random produce enemy locations.

    : param map_data:  (list)  地圖
    """
    high = map.high
    width = map.width

    rows_of_enimies = int((high - 2) / 3)
    columns_of_enimies = width - 4
    enemies = []
    for row in range(rows_of_enimies):
        for column in range(columns_of_enimies):
            enemies.append(Enemy([row + 3, column + 2], high, width))

    return enemies

def generate_bonus(map):
    return Bonus([2, rnd.randint(1, map.width - 2)], map.high, map.width)

def disable_rewarded_enemies_and_bullets(bullets, enemies, map_data):
    enemies_position = np.array(np.where(map_data == MapEnum.enemy.value)).T.tolist()
    for bullet in bullets:
        calibrated_bullet_position = bullet.get_position().copy()
        calibrated_bullet_position[0] += 1
        if calibrated_bullet_position in enemies_position:
            disable_enemy(enemies, calibrated_bullet_position)
            bullet.disable()
        if bullet.get_position() in enemies_position and bullet.is_active():
            disable_enemy(enemies, bullet.get_position())
            bullet.disable()

def disable_enemy(enemies, position):
    for enemy in enemies:
        if enemy.get_position() == position:
            enemy.disable()

def disable_rewarded_bonus_and_bullet(bullets, bonus):
    for bullet in bullets:
        if bonus.is_active() and bullet.get_position() == bonus.get_position():
            bonus.disable()
            bullet.disable()

def remove_disable_elements(elements):
    while any([element.is_active() == False for element in elements]):
        for element in elements:
            if not element.is_active():
                elements.remove(element)

def map_to_obs(map_data, shape):
    """
    Convert map data to neural network input formate.

    : param map_data:   (list)      整張地圖的集合
    : param shape:      (obs_shape) 神經網路輸入的形狀
    """
    map_data = map_data.copy()
    map_data[map_data == MapEnum.space.value] = MapObsEnum.space.value
    map_data[map_data == MapEnum.wall.value] = MapObsEnum.wall.value
    map_data[map_data == MapEnum.galaxian.value] = MapObsEnum.galaxian.value
    map_data[map_data == MapEnum.enemy.value] = MapObsEnum.enemy.value
    map_data[map_data == MapEnum.bullet.value] = MapObsEnum.bullet.value
    map_data[map_data == MapEnum.bonus.value] = MapObsEnum.bonus.value

    return np.reshape(map_data.astype(np.float16), shape)


