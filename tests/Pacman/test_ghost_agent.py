from unittest import mock
from env.Pacman import utils
from env.Pacman.game import GameState
from env.Pacman.ghost_agent import DirectionalGhost


class TestState:

    def getLegalActions(self, i: int):
        return [1, 2, 3, 4, 5, i]


class TestState2:

    def getLegalActions(self, i: int):
        return []


def test_ghost(ghost_agent):
    with mock.patch.object(utils.sys, "exit") as mock_exit:
        ghost_agent.getDistribution([1, 2, 3])
    assert mock_exit.called


def test_random_ghost(random_ghost):
    state = TestState()
    assert isinstance(random_ghost.getAction(state), int)

    state2 = TestState2()
    assert random_ghost.getAction(state2) == 'Stop'


def test_directional_ghost(state: GameState):
    ghost = DirectionalGhost(1, 1, 1)
    state.getGhostState(1).scaredTimer = 30
    assert ghost.getAction(state) == 'East'
