import mock
from env.Pacman import utils


class TestState:

    def getLegalActions(self, i: int):
        return [1, 2, 3, 4, 5, i]


def test_ghost(ghost_agent):
    with mock.patch.object(utils.sys, "exit") as mock_exit:
        ghost_agent.getDistribution([1, 2, 3])
    assert mock_exit.called


def test_random_ghost(random_ghost):
    state = TestState()
    assert isinstance(random_ghost.getAction(state), int)
