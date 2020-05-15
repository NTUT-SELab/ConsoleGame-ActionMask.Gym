import pytest

from env.Galaxian.map_element import *
from env.Galaxian.map import *

def setup_function():
    pytest.map = Map(11, 11)
    pytest.galaxian = Galaxian([7,6], pytest.map.high, pytest.map.width)
    pytest.enemy = Enemy([3,6], pytest.map.high, pytest.map.width)
    pytest.bullet = Bullet([4,4], pytest.map.high, pytest.map.width)
    pytest.bonus = Bonus([1,5], pytest.map.high, pytest.map.width)

def test_get_position():
    assert pytest.galaxian.get_position() == [7,6]
    assert pytest.enemy.get_position() == [3,6]
    assert pytest.bullet.get_position() == [4,4]
    assert pytest.bonus.get_position() == [1,5]

def test_galaxian_move():
    #LEFT
    pytest.galaxian.move(0)
    assert pytest.galaxian.get_position() == [7,5]

    #RIGHT
    pytest.galaxian.move(1)
    assert pytest.galaxian.get_position() == [7,6]

def test_galaxian_fire():
    test_bullet = Bullet(pytest.galaxian.get_position(), pytest.map.high, pytest.map.width)
    fired_bullet = pytest.galaxian.fire()
    assert type(fired_bullet) == type(test_bullet)
    assert fired_bullet.get_position() == test_bullet.get_position()

def test_enemy_cal_approach_steps():
    steps = int(pytest.map.high / 2.5)
    assert pytest.enemy.approach_complete_steps == steps

def test_move_enemy():
    for i in range(pytest.enemy.approach_complete_steps + 1):
        pytest.enemy.move()
    assert pytest.enemy.get_position() == [4,6]
    assert pytest.enemy.approach_progress == 0
    pytest.enemy.move()
    assert pytest.enemy.get_position() == [4,6]
    assert pytest.enemy.approach_progress == 1

def test_move_bullet():
    pytest.bullet.move()
    assert pytest.bullet.get_position() == [3,4]
    assert pytest.bullet.is_active()

    pytest.bullet.position[0] = 1
    pytest.bullet.move()
    assert not pytest.bullet.is_active()
    
def test_move_bonus():
    pytest.bonus.move()
    if pytest.bonus.direction == -1:
        assert pytest.bonus.get_position() == [1, 4]
    elif pytest.bonus.direction == 1:
        assert pytest.bonus.get_position() == [1, 6]

    pytest.bonus.disable()
    assert pytest.bonus.position == [1, 4] or pytest.bonus.position == [1, 6]

def test_bonus_change_direction():
    left_end = 1
    right_end = pytest.map.width - 2

    #AT THE END OF MAP, CHANGE DIRECTION
    pytest.bonus.direction = -1
    pytest.bonus.position = [1, left_end]
    original_direction = pytest.bonus.direction
    pytest.bonus.change_direction()
    assert pytest.bonus.direction != original_direction

    pytest.bonus.position = [1, right_end]
    original_direction = pytest.bonus.direction
    pytest.bonus.change_direction()
    assert pytest.bonus.direction != original_direction

    #NOT AT THE END OF MAP, DO NOT CHANGE DIRECTION
    pytest.bonus.position = [1, 6]
    original_direction = pytest.bonus.direction
    pytest.bonus.change_direction()
    assert pytest.bonus.direction == original_direction

def test_is_active():
    assert pytest.galaxian.is_active()
    assert pytest.enemy.is_active()
    assert pytest.bullet.is_active()
    assert pytest.bonus.is_active()

def test_disable():
    pytest.galaxian.disable()
    pytest.enemy.disable()
    pytest.bullet.disable()
    pytest.bonus.disable()
    assert pytest.galaxian.is_active() == False
    assert pytest.enemy.is_active() == False
    assert pytest.bullet.is_active() == False
    assert pytest.bonus.is_active() == False

def test_bonus_reactivate():
    pytest.bonus.disable()
    assert pytest.bonus.is_active() == False
    pytest.bonus.reactivate() 
    assert pytest.bonus.is_active()
