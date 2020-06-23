import pytest
import numpy as np

from env.MagicKey.action_mask_env import ActionMaskEnv
from env.MagicKey.map_element import *

def setup_function():
    pytest.env = ActionMaskEnv()
    pytest.env.reset()
    
def test_compute_action_mask():
    pytest.env.map.elements = []
    pytest.env.map.add_element(TextBallon([1, 3], (1, 2, 2)))
    pytest.env.map.refresh()
    action_mask = pytest.env.compute_action_mask(False)
    texts = pytest.env.map.elements[0].texts
    assert action_mask[ord(texts[0,0]) - 65] == 1 
    assert action_mask[ord(texts[0,1]) - 65] == 1 
    assert action_mask[ord(texts[1,0]) - 65] == 1 
    assert action_mask[ord(texts[0,1]) - 65] == 1 
    assert np.count_nonzero(action_mask == 0) >= 23
    pytest.env.map.wizard.receive_weapon(Weapon(2))
    pytest.env.map.refresh()
    action_mask = pytest.env.compute_action_mask(False)
    assert action_mask[26] == 1 
    assert np.count_nonzero(action_mask == 0) >= 22

