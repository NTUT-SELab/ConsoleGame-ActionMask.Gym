import pytest
from env.Bomberman.map import Map, Grid
import numpy as np


def test_grid():
    with pytest.raises(Exception) as ex:
        Grid(10, 10, "1213")
    assert "Grids can only contain booleans" in str(ex.value)

    grid = Grid(2, 2, True)

    grid[0][0] = False
    assert not grid[0][0]
    assert str(grid) == "TT\nFT"

    assert grid


def test_grid_as_list(map: Map):
    assert len(map.bricks.asList()) == str(map).count('#')


def test_grid_copy(map: Map):
    assert map.bricks.deepCopy().data is not map.bricks.shallowCopy().data
    assert map.bricks.data is map.bricks.shallowCopy().data


def test_grid_count(map: Map):
    assert str(map).count('#') == map.bricks.count()


def test_map(map: Map):
    assert str(map) == """%%%%%%%%%
%   E#  %
% %#%#% %
%  B    %
%%%%%%%%%"""


def test_check_map(map: Map):
    with pytest.raises(Exception) as ex:
        data = np.array(['%'])
        map.check_map(data)
    assert 'The map shape must be a rectangle.' in str(ex.value)

    with pytest.raises(Exception) as ex:
        data = np.array([[' ', ' ']])
        map.check_map(data)
    assert 'There are no wall in the map.' in str(ex.value)

    with pytest.raises(Exception) as ex:
        data = np.array([['%', ' ']])
        map.check_map(data)
    assert 'There are no enemy in the map.' in str(ex.value)

    with pytest.raises(Exception) as ex:
        data = np.array([['%', 'E']])
        map.check_map(data)
    assert 'There are no bomberman in the map.' in str(ex.value)

    with pytest.raises(Exception) as ex:
        data = np.array([['%', 'B']])
        map.check_map(data)
    assert 'There are no enemy in the map.' in str(ex.value)

    with pytest.raises(Exception) as ex:
        data = np.array([['%', 'E', 'B'], [' ', 'E', 'B']])
        map.check_map(data)
    assert 'There are holes in the left side of the map.' in str(ex.value)

    with pytest.raises(Exception) as ex:
        data = np.array([['%', 'E', 'B'], ['%', 'E', 'B']])
        map.check_map(data)
    assert 'There are holes in the right side of the map.' in str(ex.value)

    with pytest.raises(Exception) as ex:
        data = np.array([['%', 'E', '%'], ['%', 'B', '%']])
        map.check_map(data)
    assert 'There are holes in the upper side of the map.' in str(ex.value)

    with pytest.raises(Exception) as ex:
        data = np.array([['%', '%', '%'], ['%', 'E', '%'], ['%', 'B', '%']])
        map.check_map(data)
    assert 'There are holes in the lower side of the map.' in str(ex.value)

    data = np.array([['%', '%', '%'], ['%', 'E', '%'], ['%', 'B', '%'], ['%', '%', '%']])

    assert data is map.check_map(data)


def test_map_is_wall(map: Map):
    assert map.is_wall((0, 0))
    assert not map.is_wall((1, 1))
