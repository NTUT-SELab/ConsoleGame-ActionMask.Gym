import pytest
import numpy as np

from env import utils
from env.base_env import BaseEnv
from env.map_define import MapEnum

def setup_function():
    pytest.env = BaseEnv()

def test_reset():
    pytest.env.map_cache = None
    pytest.env.current_step = 100
    map_data = utils.load_map('default_map')

    np.testing.assert_array_equal(pytest.env.reset(), utils.map_to_obs(map_data))

def test_eat_food():
    pytest.env.reset()
    pytest.env.step(1)
    pytest.env.step(3)
    pytest.env.step(3)
    pytest.env.step(3)
    pytest.env.step(3)
    _, reward, _, _ = pytest.env.step(0)

    assert reward == 1

def test_eat_poison():
    pytest.env.reset()
    pytest.env.step(1)
    pytest.env.step(3)
    pytest.env.step(3)
    pytest.env.step(3)
    pytest.env.step(1)
    pytest.env.step(1)
    pytest.env.step(1)
    pytest.env.step(3)
    pytest.env.step(3)
    pytest.env.step(3)
    pytest.env.step(3)
    pytest.env.step(3)
    pytest.env.step(3)
    _, reward, _, _ = pytest.env.step(3)

    assert reward == -1

def test_invalid_action():
    pytest.env.reset()
    pytest.env.step(0)
    pytest.env.step(2)

    np.testing.assert_array_equal(pytest.env.map_cache, pytest.env.map)

@pytest.mark.parametrize('test_data', [[MapEnum.food, 1], [MapEnum.poison, -1], [MapEnum.exit, 2], [MapEnum.road, 0], [MapEnum.wall, 0]])
def test_reward(test_data):
    assert pytest.env.get_reward(test_data[0]) == test_data[1]

@pytest.mark.parametrize('current_step', [5, 100])
@pytest.mark.parametrize('target_obj', [MapEnum.road, MapEnum.wall, MapEnum.exit, MapEnum.mouse, MapEnum.food, MapEnum.poison])
def test_is_done(current_step, target_obj):
    pytest.env.current_step = current_step

    if current_step >= 100:
        assert pytest.env.is_done(target_obj) == True
    elif target_obj == MapEnum.exit:
        assert pytest.env.is_done(target_obj) == True
    else:
        assert pytest.env.is_done(target_obj) == False
