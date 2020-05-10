import pytest
from env.Pacman.map import Map
from env.Pacman.ghost_agent import GhostAgent, RandomGhost
from env.Pacman.base_env import BaseEnv


@pytest.fixture()
def map():
    return Map("default_map")


@pytest.fixture()
def ghost_agent():
    return GhostAgent(1)


@pytest.fixture()
def random_ghost():
    return RandomGhost(2)


@pytest.fixture(scope="module")
def base_env():
    return BaseEnv()


@pytest.fixture(scope="module")
def state():
    return BaseEnv().state
