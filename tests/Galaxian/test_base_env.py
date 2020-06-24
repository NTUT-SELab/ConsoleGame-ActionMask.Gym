import pytest

from unittest import mock
from env.Galaxian.base_env import BaseEnv
from env.Galaxian import base_env as base_env_py
from env.Galaxian.map_element import *
from env.Galaxian.map import *

def setup_function():
    pytest.env = BaseEnv(high=11, width=11)
    pytest.env.reset()

def test_map_too_small():
    with pytest.raises(Exception) as ex:
        BaseEnv(high=10, width=9)

    assert '地圖的高度與寬度必須 > 10' in str(ex.value)

def test_reset():
    pytest.env.current_step = 100
    pytest.env.previous_enemy_numbers = 3
    obs = pytest.env.reset()
    
    enemy_numbers = len(pytest.env.enemies)
    wall_numbers = 11*4 - 4

    #SPACE = TOTAL SPACE - ENEMIES - GALAXIAN - BONUS
    space_numbers = 81 - enemy_numbers - 2

    assert pytest.env.current_step == 0
    assert pytest.env.previous_enemy_numbers == enemy_numbers
    assert np.count_nonzero(obs == 0) == space_numbers
    assert np.count_nonzero(obs == 1) == wall_numbers
    assert np.count_nonzero(obs == 2) == 1
    assert np.count_nonzero(obs == 3) == enemy_numbers
    assert np.count_nonzero(obs == 4) == 0
    assert np.count_nonzero(obs == 5) == 1

def test_move_bullets():
    pytest.env.bullets.append(Bullet([3, 3], pytest.env.map.high, pytest.env.map.width))
    pytest.env.bullets.append(Bullet([5, 6], pytest.env.map.high, pytest.env.map.width))
    assert pytest.env.bullets[0].get_position() == [3, 3]
    assert pytest.env.bullets[1].get_position() == [5, 6]
    pytest.env.move_bullets()  
    assert pytest.env.bullets[0].get_position() == [2, 3]
    assert pytest.env.bullets[1].get_position() == [4, 6]

def test_move_enemies():        
    original_position = [enemy.get_position().copy() for enemy in pytest.env.enemies]
    approach_steps = 5 

    for i in range(approach_steps):
        pytest.env.move_enemies()

    new_position = [enemy.get_position() for enemy in pytest.env.enemies]
    expected_position = np.array(original_position)
    expected_position[:,0] += 1

    np.testing.assert_array_equal(new_position, expected_position)

def test_is_enemy_catch_galaxian():
    assert pytest.env.is_enemy_catch_galaxian() == False
    pytest.env.enemies[0].position = pytest.env.galaxian.position
    assert pytest.env.is_enemy_catch_galaxian()

def test_get_reward():
    pytest.env.previous_enemy_numbers = 31
    assert pytest.env.get_reward() == 10
    pytest.env.bonus.disable()
    assert pytest.env.get_reward() == 15
    pytest.env.enemies[0].position = pytest.env.galaxian.position
    assert pytest.env.get_reward() == 5

def test_step():
    #Galaxian = 2, Bullet = 4, Bonus = 5
    original_obs = pytest.env.reset()
    original_enemy_approach_progress = pytest.env.enemies[0].approach_progress
    number_of_bullets = len(pytest.env.bullets)
    original_steps = pytest.env.current_step
    
    new_obs, _, _, _ = pytest.env.step(1)
    galaxain_step_result = np.array(np.where(new_obs == 2)) - np.array(np.where(original_obs == 2))
    bullet_step_result = np.array(np.where(new_obs == 4)) - np.array(np.where(new_obs == 2))
    bonus_step_result = np.array(np.where(new_obs == 5)) - np.array(np.where(original_obs == 5))

    np.testing.assert_array_equal(galaxain_step_result, np.array([[0], [1], [0]]))
    np.testing.assert_array_equal(bullet_step_result, np.array([[-1], [0], [0]]))
    
    #BONUS MOVE TOWARD RANDOM DIRECTION, RESULT MIGHT BE 1 OR -1
    assert np.array_equal(bonus_step_result, np.array([[0], [1], [0]])) or np.array_equal(bonus_step_result, np.array([[0], [-1], [0]]))
    
    assert len(pytest.env.bullets) - number_of_bullets == 1
    assert pytest.env.current_step - original_steps == 1
    assert pytest.env.enemies[0].approach_progress - original_enemy_approach_progress == 1

def test_render():
    with mock.patch.object(base_env_py.time, "sleep") as mock_sleep:
        pytest.env.render(10000)

    assert mock_sleep.call_args[0][0] == 10000