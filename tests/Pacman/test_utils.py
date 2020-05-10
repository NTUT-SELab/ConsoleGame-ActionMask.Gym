from env.Pacman import utils


def test_nearestPoint():
    assert (1, 1) == utils.nearestPoint((1, 1))
    assert (2, 2) == utils.nearestPoint((1.5, 1.5))


def test_manhattanDistance():
    assert utils.manhattanDistance((-1, 1), (0, 0)) == 2
    assert utils.manhattanDistance((2, -1), (0, -3)) == 4


def test_counter():
    dist = utils.Counter()
    actions = [1, 2, 3, 4]
    for a in actions:
        dist[a] = 1.0
    dist.normalize()
    assert utils.chooseFromDistribution(dist) in actions

    assert utils.sample([8, 9], [6, 4]) in [6, 4]
