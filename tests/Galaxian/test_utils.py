import pytest

from env.Galaxian.map_element import *
from env.Galaxian.map import *
from env.Galaxian import utils

def setup_function():
    pytest.map = Map(11, 11)

def test_generate_galaxian():
    galaxian = utils.generate_galaxian(pytest.map)
    assert galaxian.get_position() == [9, 5]

def test_generate_enemies():
    enemies = utils.generate_enemies(pytest.map)
    assert len(enemies) == 21

def test_generate_bonus():
    bonus = utils.generate_bonus(pytest.map)
    assert bonus.get_symbol() == 'B'

def test_disable_rewarded_enemies_and_bullets():
    enemies = utils.generate_enemies(pytest.map)
    bullets = []
    bullets.append(Bullet(enemies[8].get_position().copy(), pytest.map.high, pytest.map.width))
    bullets.append(Bullet(enemies[16].get_position().copy(), pytest.map.high, pytest.map.width))

    pytest.map.add_elements(enemies)
    pytest.map.refresh()

    #15TH ENEMEY IS IN FRONT OF 8TH ENEMY
    assert enemies[15].is_active()
    assert enemies[16].is_active()
    assert bullets[0].is_active()
    assert bullets[1].is_active()
    utils.disable_rewarded_enemies_and_bullets(bullets, enemies, pytest.map.data)
    assert enemies[15].is_active() == False
    assert enemies[16].is_active() == False
    assert bullets[0].is_active() == False
    assert bullets[1].is_active() == False

def test_remove_disable_elements():
    enemies = utils.generate_enemies(pytest.map)
    enemies[0].disable()
    enemies[1].disable()

    assert len(enemies) == 21
    assert enemies[0].get_position() == [3, 2]
    assert enemies[1].get_position() == [3, 3]

    utils.remove_disable_elements(enemies)
    assert len(enemies) == 19

    assert enemies[0].get_position() == [3, 4]
    assert enemies[1].get_position() == [3, 5]


def test_disable_rewarded_bonus_and_bullet():
    bonus = Bonus([1, 5], pytest.map.high, pytest.map.width)
    bullets = []
    bullets.append(Bullet([1, 5], pytest.map.high, pytest.map.width))
    
    assert bonus.is_active()
    assert bullets[0].is_active()
    utils.disable_rewarded_bonus_and_bullet(bullets, bonus)
    assert bonus.is_active() == False
    assert bullets[0].is_active() == False