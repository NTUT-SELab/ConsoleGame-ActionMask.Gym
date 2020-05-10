import mock
from env.Pacman import base_env as base_env_py
from env.Pacman.base_env import BaseEnv


def test_base_env(base_env: BaseEnv):
    assert base_env is not None


def test_reset(base_env: BaseEnv):
    assert base_env.reset().shape == (47, 15, 6)


def test_step(base_env: BaseEnv):
    obs, reward, done, _ = base_env.step(2)
    assert obs.shape == (47, 15, 6)
    assert reward == 10
    assert not done

    obs, reward, done, _ = base_env.step(0)
    assert reward == 10
    assert base_env.state_cache.getPacmanDirection() == 'East'

    obs, reward, done, _ = base_env.step(3)
    assert reward == -1
    assert base_env.state_cache.getPacmanDirection() == 'West'


def test_render(base_env: BaseEnv):
    with mock.patch.object(base_env_py.time, "sleep") as mock_sleep:
        base_env.render(10000)

    assert mock_sleep.call_args[0][0] == 10000


def test_get_reward(base_env: BaseEnv):
    obs, reward, done, _ = base_env.step(3)
    assert reward == -1
    assert base_env.get_reward() == -1
