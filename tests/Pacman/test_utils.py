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
    dist[5] = 2.0
    assert dist.argMax() == 5
    assert dist.sortedKeys() == [5, 1, 2, 3, 4]

    dist = utils.Counter()
    assert dist == utils.normalize(dist)
    assert utils.normalize([1, -1]) == [1, -1]
    assert dist.normalize() is None
    assert not dist.argMax()

    actions = [1, 2, 3, 4]
    for a in actions:
        dist[a] = 1.0
    dist.normalize()
    y = utils.normalize(dist)

    assert dist == y

    for a in actions:
        dist[a] = 1.0

    dist.divideAll(2)
    assert dist == {1: 0.5, 2: 0.5, 3: 0.5, 4: 0.5}

    assert dist.copy() == dist

    dist2 = utils.Counter()

    actions = [1, 2, 3, 4, 5]
    for a in actions:
        dist2[a] = 2.0

    dist[6] = 1.
    assert dist2 * dist == 4

    dist += dist2
    assert dist == {1: 2.5, 2: 2.5, 3: 2.5, 4: 2.5, 5: 2., 6: 1.}

    dist = utils.Counter()
    actions = [1, 2, 3, 4]
    for a in actions:
        dist[a] = 1.0
    dist[6] = 1.
    dist3 = dist + dist2

    assert dist3 == {1: 3., 2: 3., 3: 3., 4: 3., 5: 2., 6: 1.}

    dist.incrementAll(actions, 1)
    assert dist == {1: 2., 2: 2., 3: 2., 4: 2., 6: 1.}

    dist3 = dist - dist2

    assert dist3 == {1: 0, 2: 0, 3: 0, 4: 0, 5: -2., 6: 1.}
