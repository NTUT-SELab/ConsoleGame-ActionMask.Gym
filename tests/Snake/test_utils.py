import pytest
import numpy as np

from env.Snake import utils
from env.Snake.map_define import MapEnum, MapObsEnum

def setup_function():
    pytest.map_result = np.asarray([
            ['✤', '✤', '✤', '✤', '✤', '✤', '✤', '✤', '✤', '✤'], 
            ['✤', '◉', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '✤'],
            ['✤', '◉', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '✤'],
            ['✤', '❖', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '✤'],
            ['✤', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '✤'],
            ['✤', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '✤'],
            ['✤', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '✤'],
            ['✤', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '✤'],
            ['✤', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '✤'],
            ['✤', '✤', '✤', '✤', '✤', '✤', '✤', '✤', '✤', '✤']], dtype=np.str)

def test_init_map():
    map_data = utils.generate_map(10, 10)
    snake_position = utils.generate_snake()
    map_data = utils.reflash_map(map_data, snake_position)

    np.testing.assert_array_equal(map_data, pytest.map_result)

def test_generate_food():
    map_data = utils.generate_map(10, 10)
    snake_position = utils.generate_snake()
    map_data = utils.reflash_map(map_data, snake_position)
    food_position = utils.generate_food(map_data)
    map_data = utils.reflash_map(map_data, snake_position, food_position)

    assert np.count_nonzero(map_data == '✤') == 36
    assert np.count_nonzero(map_data == '◉') == 2
    assert np.count_nonzero(map_data == '❖') == 1
    assert np.count_nonzero(map_data == '❦') == 1

def test_map_to_obs():
    obs_shape = (pytest.map_result.shape[0], pytest.map_result.shape[1], 1)
    obs = np.asarray([
            ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1'], 
            ['1', '3', '0', '0', '0', '0', '0', '0', '0', '1'],
            ['1', '3', '0', '0', '0', '0', '0', '0', '0', '1'],
            ['1', '2', '0', '0', '0', '0', '0', '0', '0', '1'],
            ['1', '0', '0', '0', '0', '0', '0', '0', '0', '1'],
            ['1', '0', '0', '0', '0', '0', '0', '0', '0', '1'],
            ['1', '0', '0', '0', '0', '0', '0', '0', '0', '1'],
            ['1', '0', '0', '0', '0', '0', '0', '0', '0', '1'],
            ['1', '0', '0', '0', '0', '0', '0', '0', '0', '1'],
            ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1']], dtype=np.float16)

    np.testing.assert_array_equal(utils.map_to_obs(pytest.map_result, obs_shape), np.reshape(obs, obs_shape))

def test_get_snake_head_position():
    np.testing.assert_array_equal(utils.get_snake_head_position(pytest.map_result), [3, 1])

@pytest.mark.parametrize('test_data', [[0, MapEnum.body], [1, MapEnum.road], [2, MapEnum.wall], [3, MapEnum.road]])
def test_get_target_obj(test_data):
    assert utils.get_target_obj(pytest.map_result, test_data[0]) == test_data[1]

@pytest.mark.parametrize('action', [[0, [2, 1]], [1, [4, 1]], [2, [3, 0]], [3, [3, 2]]])
def test_get_target_position(action):
    snake_head_position = utils.get_snake_head_position(pytest.map_result)
    np.testing.assert_array_equal(utils.get_target_position(snake_head_position, action[0]), action[1])
