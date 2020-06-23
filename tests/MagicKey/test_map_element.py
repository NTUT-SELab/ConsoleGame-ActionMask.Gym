import pytest

from env.MagicKey.map_element import *
from env.MagicKey.map import *

def setup_function():
    pytest.map = Map(30, 25)
    pytest.text_ballon = TextBallon([1, 1], (1,2,2))
    pytest.text_bonus = TextBonus([1, 4], (1, 1, 1))
    pytest.text_weapon = TextWeapon([1, 8], (1, 1, 1))
    pytest.wizard = Wizard([28, 12])

def test_get_position():
    assert pytest.text_ballon.position == [1,1]
    assert pytest.text_bonus.position == [1,4]
    assert pytest.text_weapon.position == [1,8]
    assert pytest.wizard.position == [28,12]


def test_text_element_move():
    assert pytest.text_ballon.position == [1,1]
    assert pytest.text_bonus.position == [1,4]
    assert pytest.text_weapon.position == [1,8]
    pytest.text_ballon.move(1) 
    pytest.text_bonus.move(1) 
    pytest.text_weapon.move(1) 
    assert pytest.text_ballon.position == [2,1]
    assert pytest.text_bonus.position == [2,4]
    assert pytest.text_weapon.position == [2,8]

def test_ballon_texts():
    assert pytest.text_ballon.texts.shape == (2, 2)

def test_ballon_remove():
    assert len(np.where(pytest.text_ballon.texts != ' ')[0]) == 4
    key = pytest.text_ballon.texts[0][0]
    pytest.text_ballon.remove(key)
    assert len(np.where(pytest.text_ballon.texts != ' ')[0]) < 4
    pytest.text_ballon.texts[pytest.text_ballon.texts != ' '] = ' '
    pytest.text_ballon.remove(key)
    assert not pytest.text_ballon.status
    assert len(np.where(pytest.text_ballon.texts != ' ')[0]) == 0

def test_ballon_remove():
    assert len(np.where(pytest.text_ballon.texts != ' ')[0]) == 4
    key = pytest.text_ballon.texts[0][0]
    pytest.text_ballon.remove(key)
    assert len(np.where(pytest.text_ballon.texts != ' ')[0]) < 4
    pytest.text_ballon.texts[pytest.text_ballon.texts != ' '] = ' '
    pytest.text_ballon.remove(key)
    assert not pytest.text_ballon.status
    assert len(np.where(pytest.text_ballon.texts != ' ')[0]) == 0

def test_ballon_eliminate_by_weapon():
    assert pytest.text_ballon.reward == 0
    pytest.text_ballon.eliminate_by_weapon()
    assert pytest.text_ballon.reward == 4 

def test_ballon_to_graph():
    pytest.text_ballon.to_graph()
    assert pytest.text_ballon.texts.shape == (2, 2)
    assert pytest.text_ballon.graph.shape == (4, 4)
    assert len(np.where(pytest.text_ballon.graph == '-')[0]) == 8
    assert len(np.where(pytest.text_ballon.graph == '|')[0]) == 4

def test_bonus_remove():
    original_texts = pytest.text_bonus.texts.copy()
    pytest.text_bonus.remove(original_texts[0])
    assert len(original_texts) - len(pytest.text_bonus.texts) == 1
    pytest.text_bonus.texts = []
    pytest.text_bonus.remove(original_texts[0])
    assert not pytest.text_bonus.status
    assert pytest.text_bonus.reward == len(original_texts)*2

def test_bonus_to_graph():
    pytest.text_bonus.to_graph()
    assert pytest.text_bonus.graph.shape == (1, 3)
    assert pytest.text_bonus.graph[0, 0] == '$'
    assert pytest.text_bonus.graph[0, 2] == '$'

def test_weapon_remove():
    original_texts = pytest.text_weapon.texts.copy()
    pytest.text_weapon.remove(original_texts[0])
    assert len(original_texts) - len(pytest.text_weapon.texts) == 1
    pytest.text_weapon.texts = []
    pytest.text_weapon.remove(original_texts[0])
    assert not pytest.text_weapon.status

def test_weapon_to_graph():
    pytest.text_weapon.to_graph()
    assert pytest.text_weapon.graph.shape == (1, 3)
    assert pytest.text_weapon.graph[0, 0] == '*'
    assert pytest.text_weapon.graph[0, 2] == '*'

def test_get_weapon_from_text_weapon():
    assert pytest.text_weapon.get_weapon() == None
    pytest.text_weapon.texts = []
    weapon = Weapon(int(pytest.text_weapon.quantity*0.5) + 1)
    assert weapon.power == pytest.text_weapon.get_weapon().power

def test_wizard_receive_weapon():
    pytest.wizard.receive_weapon(None)
    assert len(pytest.wizard.weapons) == 0
    pytest.wizard.receive_weapon(Weapon(3))
    assert pytest.wizard.weapons[0].power == 3
    for _ in range(10):
        pytest.wizard.receive_weapon(Weapon(3))
    assert len(pytest.wizard.weapons) == 6

def test_wizard_use_weapon():
    assert pytest.wizard.use_weapon() == 0
    pytest.wizard.receive_weapon(Weapon(3))
    assert pytest.wizard.use_weapon() == 3

def test_wizard_shoot():
    assert pytest.wizard.key == ' '
    pytest.wizard.shoot(0)
    assert pytest.wizard.key == 'A'