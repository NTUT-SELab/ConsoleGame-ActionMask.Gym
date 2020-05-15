import pytest

from env.Galaxian.map_element import *
from env.Galaxian.map import *

def setup_function():
    pytest.map = Map(11, 11)
    pytest.map_result = np.asarray([
            ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'], 
            ['X', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'X'],
            ['X', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'X'],
            ['X', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'X'],
            ['X', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'X'],
            ['X', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'X'],
            ['X', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'X'],
            ['X', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'X'],
            ['X', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'X'],
            ['X', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'X'],
            ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']], dtype=np.str)

def test_generate_data():
    assert pytest.map.data == None
    pytest.map.generate_data()
    np.testing.assert_array_equal(pytest.map.data, pytest.map_result)

def test_add_element():
    assert len(pytest.map.map_elements) == 0
    pytest.map.add_element(Galaxian([9, 4], pytest.map.high, pytest.map.width))
    assert len(pytest.map.map_elements) == 1

def test_add_elements():
    assert len(pytest.map.map_elements) == 0
    elements = [Galaxian([9, 4], pytest.map.high, pytest.map.width), Bullet([9, 4], pytest.map.high, pytest.map.width)]
    pytest.map.add_elements(elements)
    assert len(pytest.map.map_elements) == 2

def test_clear_elements():
    elements = [Galaxian([9, 4], pytest.map.high, pytest.map.width), Bullet([9, 4], pytest.map.high, pytest.map.width)]
    pytest.map.add_elements(elements)
    assert len(pytest.map.map_elements) == 2
    pytest.map.clear_elements()
    assert len(pytest.map.map_elements) == 0

def test_clear_elements():
    elements = [Galaxian([9, 4], pytest.map.high, pytest.map.width), Bullet([9, 4], pytest.map.high, pytest.map.width)]
    pytest.map.add_elements(elements)
    assert len(pytest.map.map_elements) == 2
    pytest.map.clear_elements()
    assert len(pytest.map.map_elements) == 0

def test_refresh():
    pytest.map.generate_data()

    elements = [Galaxian([9, 4], pytest.map.high, pytest.map.width), Bullet([8, 4], pytest.map.high, pytest.map.width)]
    pytest.map.add_elements(elements)
    #BEFORE REFRESH, MAP DATA IS NOT CHANGED
    np.testing.assert_array_equal(pytest.map.data, pytest.map_result)
    
    pytest.map.refresh()
    refresh_result = pytest.map_result = np.asarray([
             ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'], 
            ['X', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'X'],
            ['X', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'X'],
            ['X', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'X'],
            ['X', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'X'],
            ['X', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'X'],
            ['X', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'X'],
            ['X', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'X'],
            ['X', ' ', ' ', ' ', 'o', ' ', ' ', ' ', ' ', ' ', 'X'],
            ['X', ' ', ' ', ' ', 'G', ' ', ' ', ' ', ' ', ' ', 'X'],
            ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']], dtype=np.str)
    #AFTER MAP REFRESH, MAP DATA SHOWS ELEMENTS
    np.testing.assert_array_equal(pytest.map.data, refresh_result)
    