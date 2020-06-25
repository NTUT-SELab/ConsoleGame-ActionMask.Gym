from env.Bomberman.action_mask_env import ActionMaskEnv
from env.Bomberman.game import Bomb
from unittest import mock


def test_action_mask(action_mask: ActionMaskEnv):
    assert action_mask is not None


def test_step(action_mask: ActionMaskEnv):
    action_mask.reset()
    obs, reward, done, _ = action_mask.step(5)
    assert reward == 0.01
    assert not done

    obs, reward, done, mask = action_mask.step(2)
    assert reward == -0.01
    assert action_mask.state.get_bomberman().get_direction() == 'East'
    assert mask == {'action_mask': [0, 0, 1, 0, 1, 1]}

    obs, reward, done, mask = action_mask.step(2)
    assert reward == -0.01
    assert action_mask.state.get_bomberman().get_direction() == 'East'
    assert mask == {'action_mask': [0, 0, 1, 1, 1, 1]}

    obs, reward, done, mask = action_mask.step(2)
    assert reward == -0.01
    assert action_mask.state.get_bomberman().get_direction() == 'East'
    assert mask == {'action_mask': [0, 0, 1, 1, 1, 1]}

    obs, reward, done, mask = action_mask.step(2)
    assert reward == -0.01
    assert action_mask.state.get_bomberman().get_direction() == 'East'
    assert mask == {'action_mask': [1, 0, 0, 1, 1, 1]}

    obs, reward, done, mask = action_mask.step(0)
    assert reward == 10
    assert action_mask.state.get_bomberman().get_direction() == 'North'
    assert mask == {'action_mask': [1, 1, 0, 0, 1, 1]}

    bomb = Bomb((3, 3))
    bomb.countdown = 1
    action_mask.state.get_bombs().append(bomb)

    obs, reward, done, mask = action_mask.step(4)
    assert reward == 80
    assert done


def test_compute_action_mask(action_mask: ActionMaskEnv):
    with mock.patch.object(action_mask.state, "get_legal_actions") as mock_get:
        mock_get.return_value = []
        assert action_mask.compute_action_mask() == [1, 1, 1, 1, 1, 1]

    with mock.patch.object(action_mask.state, "get_legal_actions") as mock_get:
        mock_get.return_value = ["East"]
        assert action_mask.compute_action_mask() == [0, 0, 1, 0, 0, 0]
