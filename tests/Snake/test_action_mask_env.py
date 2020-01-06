import pytest
import numpy as np

from env.Snake import utils
from env.Snake.action_mask_env import ActionMaskEnv
from env.Snake.map_define import MapEnum

def setup_function():
    pytest.env = ActionMaskEnv(high=10, width=10)
    pytest.env.reset()
    pytest.env.snake_position = [[6,1], [5, 1], [4, 1], [3, 1], [2, 1], [1, 1]]
    pytest.env.food_position = [7, 7]
    pytest.env.reflash_map()

@pytest.mark.parametrize('test_data', [[[1], [0, 1, 0, 1]], \
                                        [[3, 0], [1, 0, 0, 1]], \
                                        [[3, 0, 2], [1, 1, 1, 1]], \
                                        [[3, 1, 1, 2, 0], [1, 0, 1, 1]]])
def test_action_mask(test_data):
    for action in test_data[0]:
        _, _, _, info = pytest.env.step(action)

    np.testing.assert_array_equal(info.get('action_mask'), test_data[1])
