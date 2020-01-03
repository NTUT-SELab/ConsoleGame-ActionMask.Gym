import numpy as np

from env.Snake import utils
from env.Snake.map_define import MapEnum, MapObsEnum

def test_init_map():
    map = utils.generate_map(10, 10)
    snake_position = utils.generate_snake()
    map = utils.reflash_map(map, snake_position)

    map_result = np.asarray([
        ['✤', '✤', '✤', '✤', '✤', '✤', '✤', '✤', '✤', '✤'], 
        ['✤', '◉', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '✤'],
        ['✤', '◉', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '✤'],
        ['✤', '❖', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '✤'],
        ['✤', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '✤'],
        ['✤', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '✤'],
        ['✤', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '✤'],
        ['✤', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '✤'],
        ['✤', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '✤'],
        ['✤', '✤', '✤', '✤', '✤', '✤', '✤', '✤', '✤', '✤']], dtype=np.str)

    np.testing.assert_array_equal(map, map_result)

def test_generate_food():
    map = utils.generate_map(10, 10)
    snake_position = utils.generate_snake()
    map = utils.reflash_map(map, snake_position)
    food_position = utils.generate_food(map)
    map = utils.reflash_map(map, snake_position, food_position)

    assert np.count_nonzero(map == '✤') == 36
    assert np.count_nonzero(map == '◉') == 2
    assert np.count_nonzero(map == '❖') == 1
    assert np.count_nonzero(map == '❦') == 1
