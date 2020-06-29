import pytest

from unittest import mock
from env.MagicKey.base_env import BaseEnv
from env.MagicKey import base_env as base_env_py
from env.MagicKey.map_element import *
from env.MagicKey.map import *

def setup_function():
    pytest.env = BaseEnv()
    pytest.env.reset()

def test_map_too_small():
    with pytest.raises(Exception) as ex:
        BaseEnv(high=10, width=9)

    assert '地圖的高度必須大於25，與寬度必須大於15' in str(ex.value)

def test_reset():
    pytest.env.current_step = 100
    pytest.env.score = 3
    obs = pytest.env.reset()

    assert pytest.env.current_step == 0
    assert pytest.env.score == 0

def test_get_reward():
    assert pytest.env.get_reward() == 0
    pytest.env.done = True
    assert pytest.env.get_reward() == -500

def test_step():
    key = pytest.env.map.elements[0].texts[0][0]
    action = ord(key) - 65
    assert pytest.env.current_step == 0
    assert pytest.env.get_reward() == 0
    obs, reward, done, _ = pytest.env.step(action)
    assert reward > 0
    assert pytest.env.current_step == 1

def test_render():
    with mock.patch.object(base_env_py.time, "sleep") as mock_sleep:
        pytest.env.render(10000)

    assert mock_sleep.call_args[0][0] == 10000

def test_map_to_string():
    state = pytest.env.map_to_string()
    assert state.count('#') == 96
    assert state.count('^') == 17
    assert state.count('@') == 1
    assert state.count('-') > 1
    assert state.count('|') > 1

    