import pytest
import numpy as np

from env import utils
from env.map_define import MapEnum, MapObsEnum

def setup_function():
    pytest.map_buffer = np.asarray([
            ['X', 'X', 'X', 'X'], 
            ['X', ' ', 'E', 'X'], 
            ['X', 'M', 'F', 'X'], 
            ['X', 'P', 'E', 'X'], 
            ['X', 'X', 'X', 'X']], dtype=str)

def test_map_to_obs():
    obs = np.asarray([
        ['1', '1', '1', '1'], 
        ['1', '0', '2', '1'], 
        ['1', '3', '4', '1'], 
        ['1', '5', '2', '1'], 
        ['1', '1', '1', '1']], dtype=np.float16)

    np.testing.assert_array_equal(utils.map_to_obs(pytest.map_buffer), obs)

@pytest.mark.parametrize('test_data', [[0, MapEnum.road], [1, MapEnum.poison], [2, MapEnum.wall], [3, MapEnum.food]])
def test_get_target_obj(test_data):
    assert utils.get_target_obj(pytest.map_buffer, test_data[0]) == test_data[1]

def test_get_mouse_position():
    np.testing.assert_array_equal(utils.get_mouse_position(pytest.map_buffer), [2,1])
