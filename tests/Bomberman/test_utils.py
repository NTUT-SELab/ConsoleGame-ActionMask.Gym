from env.Bomberman import utils


def test_manhattanDistance():
    assert utils.manhattanDistance((-1, 1), (0, 0)) == 2
    assert utils.manhattanDistance((2, -1), (0, -3)) == 4
