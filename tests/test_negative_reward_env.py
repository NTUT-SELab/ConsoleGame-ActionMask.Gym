import pytest

from env.negative_reward_env import NegativeRewardEnv
from env.map_define import MapEnum

def setup_function():
    pytest.env = NegativeRewardEnv()

def test_invalid_action_reward():
    pytest.env.reset()
    _, reward, _, _ = pytest.env.step(0)
    assert reward == -5
    _, reward, _, _ = pytest.env.step(2)
    assert reward == -5

@pytest.mark.parametrize('test_data', [[MapEnum.food, 1], [MapEnum.poison, -1], [MapEnum.exit, 2], [MapEnum.road, 0], [MapEnum.wall, -5]])
def test_reward(test_data):
    assert pytest.env.get_reward(test_data[0]) == test_data[1]
