import pytest
import numpy as np

from env.MouseWalkingMaze import utils


def test_load_map():
    map_data = utils.load_map('default_map')
    assert map_data is not None


def test_check_map_shape():
    map_buffer = np.asarray(['X', ' ', 'X'], dtype=str)
    with pytest.raises(Exception) as ex:
        utils.check_map(map_buffer)
    assert 'The map shape must be a rectangle.' in str(ex.value)


def test_check_map_size():
    map_buffer = np.asarray([['X', ' ', 'X'], ['X', ' ', 'X'], ['X', 'X', 'X']], dtype=str)
    with pytest.raises(Exception) as ex:
        utils.check_map(map_buffer)
    assert 'The movable area of ​​the rat must be bigger than 2.' in str(ex.value)


def test_check_mouse():
    map_buffer = np.asarray([['X', 'X', 'X', 'X'], ['X', ' ', 'E', 'X'], ['X', 'X', 'X', 'X']], dtype=str)
    with pytest.raises(Exception) as ex:
        utils.check_map(map_buffer)
    assert 'The map must contain 1 mouse and 1 exit.' in str(ex.value)


def test_check_exit():
    map_buffer = np.asarray([['X', 'X', 'X', 'X'], ['X', 'M', ' ', 'X'], ['X', 'X', 'X', 'X']], dtype=str)
    with pytest.raises(Exception) as ex:
        utils.check_map(map_buffer)
    assert 'The map must contain 1 mouse and 1 exit.' in str(ex.value)


def test_check_holes_upper_side():
    map_buffer = np.asarray([['X', 'X', ' ', 'X'], ['X', 'M', 'E', 'X'], ['X', 'X', 'X', 'X']], dtype=str)
    with pytest.raises(Exception) as ex:
        utils.check_map(map_buffer)
    assert 'There are holes in the upper side of the map.' in str(ex.value)


def test_check_holes_lower_side():
    map_buffer = np.asarray([['X', 'X', 'X', 'X'], ['X', 'M', 'E', 'X'], ['X', ' ', 'X', 'X']], dtype=str)
    with pytest.raises(Exception) as ex:
        utils.check_map(map_buffer)
    assert 'There are holes in the lower side of the map.' in str(ex.value)


def test_check_holes_left_side():
    map_buffer = np.asarray([['X', 'X', 'X', 'X'], [' ', 'M', 'E', 'X'], ['X', 'X', 'X', 'X']], dtype=str)
    with pytest.raises(Exception) as ex:
        utils.check_map(map_buffer)
    assert 'There are holes in the left side of the map.' in str(ex.value)


def test_check_holes_right_side():
    map_buffer = np.asarray([['X', 'X', 'X', 'X'], ['X', 'M', 'E', ' '], ['X', 'X', 'X', 'X']], dtype=str)
    with pytest.raises(Exception) as ex:
        utils.check_map(map_buffer)
    assert 'There are holes in the right side of the map.' in str(ex.value)
