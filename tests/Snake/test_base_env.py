import pytest
import numpy as np

from env.Snake import utils
from env.Snake.base_env import BaseEnv
from env.Snake.map_define import MapEnum

def setup_function():
    pytest.env = BaseEnv(high=10, width=10)
    pytest.env.reset()
    pytest.env.snake_position = [[5, 1], [4, 1], [3, 1], [2, 1], [1, 1]]
    pytest.env.food_position = [6, 2]
    pytest.env.reflash_map()

def test_map_too_small():
    with pytest.raises(Exception) as ex:
        BaseEnv(high=10, width=9)

    assert '地圖的高度與寬度必須 > 10' in str(ex.value)

def test_reset():
    pytest.env.current_step = 100
    pytest.env.previous_action = 3

    obs = pytest.env.reset()

    assert pytest.env.current_step == 0
    assert pytest.env.previous_action == 1
    assert np.count_nonzero(obs == 0) == 60
    assert np.count_nonzero(obs == 1) == 36
    assert np.count_nonzero(obs == 2) == 1
    assert np.count_nonzero(obs == 3) == 2
    assert np.count_nonzero(obs == 4) == 1

@pytest.mark.parametrize('test_data', [ [0, [[6, 1], [5, 1], [4, 1], [3, 1], [2, 1]]], \
                                        [1, [[6, 1], [5, 1], [4, 1], [3, 1], [2, 1]]], \
                                        [2, [[5, 0], [5, 1], [4, 1], [3, 1], [2, 1]]], \
                                        [3, [[5, 2], [5, 1], [4, 1], [3, 1], [2, 1]]]])
def test_move_snake(test_data):
    obs, _, _, _ = pytest.env.step(test_data[0])

    np.testing.assert_array_equal(pytest.env.snake_position, test_data[1])
    assert np.count_nonzero(obs == 4) == 1
    np.testing.assert_array_equal(pytest.env.food_position, [6, 2])

def test_eat_food():
    pytest.env.step(1)
    obs, reward, _, _ = pytest.env.step(3)

    assert reward == 1
    assert np.count_nonzero(obs == 4) == 1
    assert str(pytest.env.food_position).strip('[]') != str([6, 2]).strip('[]')

@pytest.mark.parametrize('test_data', [[[0], 0], [[1], 0], [[2], -1], [[1, 3], 1], [[3, 0, 2], -1]])
def test_reward(test_data):
    for action in test_data[0]:
        _, reward, _, _ = pytest.env.step(action)

    assert reward == test_data[1]

@pytest.mark.parametrize('test_data', [[[1, 0], [7, 1]], \
                                        [[3, 2], [5, 3]], \
                                        [[3, 0, 1], [3, 2]], \
                                        [[3, 3, 3, 0, 2, 3], [4, 2]]])
def test_go_back(test_data):
    for action in test_data[0]:
        pytest.env.step(action)

    snake_head_position = utils.get_snake_head_position(pytest.env.map_data)
    np.testing.assert_array_equal(snake_head_position, test_data[1])

@pytest.mark.parametrize('actions', [[2], [3, 0, 2]])
def test_is_done(actions):
    for action in actions:
        _, _, is_done, _ = pytest.env.step(action)

    assert is_done
