import pytest
from env.Bomberman.map import Map
from env.Bomberman.base_env import BaseEnv
from env.Bomberman.action_mask_env import ActionMaskEnv


@pytest.fixture()
def map():
    return Map("test_map")


@pytest.fixture(scope="module")
def base_env():
    return BaseEnv('test_map')


@pytest.fixture(scope="module")
def state():
    return BaseEnv('test_map').state


@pytest.fixture(scope="module")
def action_mask():
    return ActionMaskEnv('test_map')
