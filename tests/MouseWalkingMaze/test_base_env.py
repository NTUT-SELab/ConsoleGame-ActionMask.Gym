import pytest
import numpy as np

from env.MouseWalkingMaze import utils
from env.MouseWalkingMaze.base_env import BaseEnv
from env.MouseWalkingMaze.map_define import MapEnum


def setup_function():
    pytest.env = BaseEnv(map_name='map1', end_step=100)


def test_reset():
    pytest.env.map_cache = None
    pytest.env.current_step = 100
    map_data = utils.load_map('map1')

    np.testing.assert_array_equal(pytest.env.reset(), utils.map_to_obs(map_data, pytest.env.obs_shape))


def test_eat_food():
    pytest.env.reset()
    pytest.env.step(1)
    pytest.env.step(3)
    pytest.env.step(3)
    pytest.env.step(3)
    pytest.env.step(3)
    _, reward, _, _ = pytest.env.step(0)

    assert reward == 2


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


@pytest.mark.parametrize(
    'test_data', [[MapEnum.food, 2], [MapEnum.poison, -1], [MapEnum.exit, 1], [MapEnum.road, 0], [MapEnum.wall, 0]]
)
def test_reward(test_data):
    assert pytest.env.get_reward(test_data[0]) == test_data[1]


@pytest.mark.parametrize('current_step', [5, 100])
@pytest.mark.parametrize(
    'target_obj', [MapEnum.road, MapEnum.wall, MapEnum.exit, MapEnum.mouse, MapEnum.food, MapEnum.poison]
)
def test_is_done(current_step, target_obj):
    pytest.env.current_step = current_step

    if current_step >= 100:
        assert pytest.env.is_done(target_obj)
    elif target_obj == MapEnum.exit:
        assert pytest.env.is_done(target_obj)
    else:
        assert not pytest.env.is_done(target_obj)
