import numpy as np

from env import utils

def test_map_to_obs():
    map_buffer = np.asarray([
        ['X', 'X', 'X', 'X'], 
        ['X', ' ', 'E', 'X'], 
        ['X', 'M', 'F', 'X'], 
        ['X', 'P', 'E', 'X'], 
        ['X', 'X', 'X', 'X']], dtype=str)
    
    obs = np.asarray([
        ['1', '1', '1', '1'], 
        ['1', '0', '2', '1'], 
        ['1', '3', '4', '1'], 
        ['1', '5', '2', '1'], 
        ['1', '1', '1', '1']], dtype=np.float16)

    np.testing.assert_array_equal(utils.map_to_obs(map_buffer), obs)

def test_get_mouse_position():
    map_buffer = np.asarray([
        ['X', 'X', 'X', 'X'], 
        ['X', ' ', 'E', 'X'], 
        ['X', 'M', 'F', 'X'], 
        ['X', 'P', 'E', 'X'], 
        ['X', 'X', 'X', 'X']], dtype=str)

    np.testing.assert_array_equal(utils.get_mouse_position(map_buffer), [2,1])
