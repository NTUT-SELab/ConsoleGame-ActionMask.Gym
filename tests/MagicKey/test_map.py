import pytest

from env.MagicKey.map_element import *
from env.MagicKey.map import *

def setup_function():
    pytest.map = Map(30, 20)

def test_generate_data():
    pytest.map.generate_data()
    assert len(np.where(pytest.map.data == '@')[0]) == 1
    assert len(np.where(pytest.map.data == '#')[0]) == 96
    assert len(np.where(pytest.map.data == '^')[0]) == 18
    assert len(np.where(pytest.map.data == ' ')[0]) == 485
    
def test_add_element():
    assert len(pytest.map.elements) == 0
    pytest.map.add_element(TextBallon([1, 1], (1,2,2)))
    assert len(pytest.map.elements) == 1

def test_add_elements():
    assert len(pytest.map.elements) == 0
    elements = [TextBallon([1, 1], (1,2,2)), TextBallon([1, 4], (1,2,2))]
    pytest.map.add_elements(elements)
    assert len(pytest.map.elements) == 2

def test_remove_elements():
    elements = [TextBallon([1, 1], (1,2,2)), TextBallon([1, 4], (1,2,2))]
    pytest.map.add_elements(elements)
    assert len(pytest.map.elements) == 2
    pytest.map.elements[0].disable()
    pytest.map.remove_elements()
    assert len(pytest.map.elements) == 1

def test_eliminate_texts_by_weapon():
    pytest.map.wizard.receive_weapon(Weapon(4))
    elements = [TextBallon([1, 1], (1,2,2)), TextBallon([1, 4], (1,2,2))]
    pytest.map.add_elements(elements)
    assert len(pytest.map.elements) == 2
    assert pytest.map.elements[0].status == True
    assert pytest.map.elements[1].status == True
    pytest.map.eliminate_texts_by_weapon()
    assert pytest.map.elements[0].status == False
    assert pytest.map.elements[1].status == False

def test_is_end():
    elements = [TextBallon([1, 1], (1,2,2)), TextBallon([1, 4], (1,2,2))]
    pytest.map.add_elements(elements)
    assert not pytest.map.is_end()
    assert pytest.map.elements[0].status
    pytest.map.elements[0].position[0] = pytest.map.high - 3
    assert pytest.map.is_end()
    assert not pytest.map.elements[0].status



def test_refresh():
    pytest.map.generate_data()
    pytest.map.add_element(TextBallon([1, 1], (1,2,2)))

    assert len(np.where(pytest.map.data == '@')[0]) == 1
    assert len(np.where(pytest.map.data == '#')[0]) == 96
    assert len(np.where(pytest.map.data == '^')[0]) == 18
    assert len(np.where(pytest.map.data == ' ')[0]) == 485
    pytest.map.refresh()
    assert len(np.where(pytest.map.data == '@')[0]) == 1
    assert len(np.where(pytest.map.data == '#')[0]) == 96
    assert len(np.where(pytest.map.data == '^')[0]) == 17
    assert len(np.where(pytest.map.data == '|')[0]) == 4
    assert len(np.where(pytest.map.data == '-')[0]) == 8
    assert len(np.where(np.char.isalpha(pytest.map.data))[0]) == 4
    assert len(np.where(pytest.map.data == ' ')[0]) == 470