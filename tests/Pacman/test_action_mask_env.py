from env.Pacman.action_mask_env import ActionMaskEnv
from unittest import mock


def test_action_mask(action_mask: ActionMaskEnv):
    assert action_mask is not None


def test_step(action_mask: ActionMaskEnv):
    obs, reward, done, _ = action_mask.step(2)
    assert obs.shape == (47, 15, 6)
    assert reward == 10
    assert not done

    obs, reward, done, mask = action_mask.step(0)
    assert reward == 10
    assert action_mask.state_cache.getPacmanDirection() == 'East'
    assert mask == {'action_mask': [0, 1, 1, 1]}

    obs, reward, done, mask = action_mask.step(3)
    assert reward == 0
    assert action_mask.state_cache.getPacmanDirection() == 'West'
    assert mask == {'action_mask': [0, 0, 1, 1]}


def test_compute_action_mask(action_mask: ActionMaskEnv):
    with mock.patch.object(action_mask.state_cache, "getLegalActions") as mock_get:
        mock_get.return_value = []
        assert action_mask.compute_action_mask() == [1, 1, 1, 1]

    with mock.patch.object(action_mask.state_cache, "getLegalActions") as mock_get:
        mock_get.return_value = ["East"]
        assert action_mask.compute_action_mask() == [0, 0, 1, 0]
