import pytest
import numpy as np

from env.base_env import BaseEnv
from env import utils

def setup_function():
    pytest.env = BaseEnv()

def test_reset():
    pytest.env.map_cache = None
    pytest.env.current_step = 100
    map_data = utils.load_map('default_map')

    np.testing.assert_array_equal(pytest.env.reset(), utils.map_to_obs(map_data))
