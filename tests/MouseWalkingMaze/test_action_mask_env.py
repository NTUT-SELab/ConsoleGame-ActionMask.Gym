import pytest
import numpy as np

from env.MouseWalkingMaze.action_mask_env import ActionMaskEnv


def setup_function():
    pytest.env = ActionMaskEnv(map_name='map1', end_step=100)


def test_eat_food():
    pytest.env.reset()
    pytest.env.step(3)
    pytest.env.step(3)
    pytest.env.step(1)
    pytest.env.step(3)
    pytest.env.step(3)
    _, reward, _, info = pytest.env.step(0)

    assert reward == 2
    np.testing.assert_array_equal(info.get('action_mask'), [0, 1, 0, 1])
