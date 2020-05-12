import pytest

from env.MouseWalkingMaze.negative_reward_env import NegativeRewardEnv
from env.MouseWalkingMaze.map_define import MapEnum


def setup_function():
    pytest.env = NegativeRewardEnv(map_name='map1')


def test_invalid_action_reward():
    pytest.env.reset()
    _, reward, _, _ = pytest.env.step(0)
    assert reward == -5
    _, reward, _, _ = pytest.env.step(2)
    assert reward == -5


@pytest.mark.parametrize(
    'test_data', [[MapEnum.food, 2], [MapEnum.poison, -1], [MapEnum.exit, 1], [MapEnum.road, 0], [MapEnum.wall, -5]]
)
def test_reward(test_data):
    assert pytest.env.get_reward(test_data[0]) == test_data[1]
