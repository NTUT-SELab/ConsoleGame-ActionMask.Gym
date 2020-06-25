from unittest import mock
from env.Bomberman import base_env as base_env_py
from env.Bomberman.game import Bomb
from env.Bomberman.base_env import BaseEnv


def test_base_env(base_env: BaseEnv):
    assert base_env is not None


def test_reset(base_env: BaseEnv):
    base_env.current_step = 1
    base_env.reset()
    assert base_env.current_step == 0


def test_step(base_env: BaseEnv):
    base_env.reset()
    obs, reward, done, _ = base_env.step(5)
    assert reward == 0.01
    assert not done

    obs, reward, done, _ = base_env.step(2)
    assert reward == -0.01
    assert base_env.state.get_bomberman().get_direction() == 'East'

    obs, reward, done, _ = base_env.step(2)
    assert reward == -0.01
    assert base_env.state.get_bomberman().get_direction() == 'East'

    obs, reward, done, _ = base_env.step(2)
    assert reward == -0.01
    assert base_env.state.get_bomberman().get_direction() == 'East'

    obs, reward, done, _ = base_env.step(4)
    assert reward == -0.01

    obs, reward, done, _ = base_env.step(4)
    assert reward == 10

    bomb = Bomb((3, 3))
    bomb.countdown = 1
    base_env.state.get_bombs().append(bomb)

    obs, reward, done, _ = base_env.step(4)
    assert reward == 80
    assert done


def test_render(base_env: BaseEnv):
    with mock.patch.object(base_env_py.time, "sleep") as mock_sleep:
        base_env.render(10000)

    assert mock_sleep.call_args[0][0] == 10000

    with mock.patch.object(base_env_py.os, "system") as mock_system:
        base_env.render(0)

    assert mock_system.called


def test_get_reward(base_env: BaseEnv):
    base_env.reset()
    obs, reward, done, _ = base_env.step(4)

    base_env.state.score_item = [10, 200, -500, 500]
    assert reward == -0.01
    assert base_env.get_reward() == 30
