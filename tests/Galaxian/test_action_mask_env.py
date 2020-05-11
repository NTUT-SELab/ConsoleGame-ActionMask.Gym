import pytest
import numpy as np

from env.Galaxian.action_mask_env import ActionMaskEnv

def setup_function():
    pytest.env = ActionMaskEnv(high=11, width=11)
    pytest.env.reset()

def test_compute_action_mask():
    left_end = 1
    right_end = pytest.env.map.width - 2
    
    pytest.env.galaxian.position[1] = left_end
    action_mask = pytest.env.compute_action_mask(False)
    np.testing.assert_array_equal(action_mask, [0, 1])

    pytest.env.galaxian.position[1] = right_end
    action_mask = pytest.env.compute_action_mask(False)
    np.testing.assert_array_equal(action_mask, [1, 0])

