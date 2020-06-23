import pytest

from env.MagicKey.map_element import *
from env.MagicKey.map import *
from env.MagicKey import utils

def setup_function():
    pytest.map = Map(30, 20)
    
def test_generate_texts_to_map():
    assert len(pytest.map.elements) == 0
    utils.generate_texts_to_map(pytest.map)
    assert len(pytest.map.elements) > 0

def test_is_enough_space():
    assert not utils.is_enough_space(2, 50, 40, pytest.map)
    assert utils.is_enough_space(2, 3 ,3, pytest.map)

def test_apply_action():
    pytest.map.add_element(TextBallon([1, 3], (1, 3, 3)))
    pytest.map.refresh()
    assert len(np.where(np.char.isalpha(pytest.map.data))[0]) == 9
    [utils.apply_action(pytest.map, action) for action in range(26)]
    pytest.map.refresh()
    assert len(np.where(np.char.isalpha(pytest.map.data))[0]) == 1
    pytest.map.add_element(TextBallon([1, 3], (1, 3, 3)))
    pytest.map.refresh()
    assert len(np.where(np.char.isalpha(pytest.map.data))[0]) == 10
    pytest.map.wizard.receive_weapon(Weapon(3))
    utils.apply_action(pytest.map, 26)
    pytest.map.refresh()
    assert len(np.where(np.char.isalpha(pytest.map.data))[0]) == 0

def test_remove_key():
    pytest.map.add_element(TextBallon([1, 3], (1, 3, 3)))
    pytest.map.refresh()
    assert len(np.where(np.char.isalpha(pytest.map.data))[0]) == 9
    utils.remove_key(pytest.map, 26)
    assert len(np.where(np.char.isalpha(pytest.map.data))[0]) == 9

def test_move_text_elements():
    pytest.map.add_element(TextBallon([1, 3], (1, 3, 3)))
    pytest.map.refresh()
    utils.move_text_elements(pytest.map, 600)
    pytest.map.refresh()
    assert pytest.map.elements[0].position[0] - 1 >= 1
