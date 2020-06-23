from env.Bomberman import utils


def test_nearestPoint():
    assert (1, 1) == utils.nearestPoint((1, 1))
    assert (2, 2) == utils.nearestPoint((1.5, 1.5))


def test_manhattanDistance():
    assert utils.manhattanDistance((-1, 1), (0, 0)) == 2
    assert utils.manhattanDistance((2, -1), (0, -3)) == 4
