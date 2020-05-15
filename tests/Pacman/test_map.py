import pytest
from env.Pacman.map import Map, Grid
import numpy as np


def test_copy(map: Map):
    map_copy = map.deepCopy()

    assert map_copy.food == map.food
    assert map_copy.numGhosts == map.numGhosts
    assert map_copy is not map


def test_grid():
    with pytest.raises(Exception) as ex:
        Grid(10, 10, "1213")
    assert "Grids can only contain booleans" in str(ex.value)

    grid = Grid(2, 2, True)

    grid[0][0] = False
    assert not grid[0][0]
    assert str(grid) == "TT\nFT"

    assert not grid == None


def test_grid_as_list(map: Map):
    assert len(map.food.asList()) == str(map).count('.')


def test_grid_copy(map: Map):
    assert map.food.deepCopy().data is not map.food.shallowCopy().data
    assert map.food.data is map.food.shallowCopy().data


def test_grid_count(map: Map):
    assert str(map).count('.') == map.food.count()


def test_map(map: Map):
    assert str(
        map
    ) == """%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%o.........%.......P.........o........%......o%
%.%%.%.%%%.%.%%%%.%.%.%%%%.%%%%%.%.%%.%.%%%%%.%
%....%.....%o.....%.%............%............%
%.%%.%.%.%.%.%%%%.%.%.%%.%.%%%.%.%.%%..%.%%%%.%
%........%.%o.....%o..%%.%....o%.%.o...%......%
%.%%.%.%.%.%.%%%%.%.%.%%.%%%%%.%.%.%%%.%.%%%%.%
%....%.....%o.....%.%.%%.........%.....%...o..%
%.%%.%.%.%.%.%%%%.%.%.%%.%.%%%.%.%.%%..%.%%%%.%
%......%....o.....%o..........o%...o...%......%
%.%%%%.%.%.%%%%%%.%%.%.%.%%%%%.%.%%.%..%.%%%%.%
%..o...%.............%..o.......o...%.........%
%.%%%%.%.%%%%%%.%.%%.%.%.%%  %%.%%%.%.%%%%%.%.%
%o..............%........%GGGG%..............o%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"""


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
    assert 'There are no ghost in the map.' in str(ex.value)

    with pytest.raises(Exception) as ex:
        data = np.array([['%', 'G']])
        map.check_map(data)
    assert 'There are no pacman in the map.' in str(ex.value)

    with pytest.raises(Exception) as ex:
        data = np.array([['%', 'G']])
        map.check_map(data)
    assert 'There are no pacman in the map.' in str(ex.value)

    with pytest.raises(Exception) as ex:
        data = np.array([['%', 'G', 'P'], [' ', 'G', 'P']])
        map.check_map(data)
    assert 'There are holes in the left side of the map.' in str(ex.value)

    with pytest.raises(Exception) as ex:
        data = np.array([['%', 'G', 'P'], ['%', 'G', 'P']])
        map.check_map(data)
    assert 'There are holes in the right side of the map.' in str(ex.value)

    with pytest.raises(Exception) as ex:
        data = np.array([['%', 'G', '%'], ['%', 'P', '%']])
        map.check_map(data)
    assert 'There are holes in the upper side of the map.' in str(ex.value)

    with pytest.raises(Exception) as ex:
        data = np.array([['%', '%', '%'], ['%', 'G', '%'], ['%', 'P', '%']])
        map.check_map(data)
    assert 'There are holes in the lower side of the map.' in str(ex.value)

    data = np.array([['%', '%', '%'], ['%', 'G', '%'], ['%', 'P', '%'], ['%', '%', '%']])

    assert data is map.check_map(data)


def test_map_is_wall(map: Map):
    assert map.isWall((0, 0))
    assert not map.isWall((1, 1))
