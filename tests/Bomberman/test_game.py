import pytest
from env.Bomberman.game import Directions, Configuration, Actions, GameState, EnemyRules, BombermanRules, AgentState
import numpy as np


def test_directions():
    assert Directions.LEFT['West'] == Directions.SOUTH
    assert Directions.RIGHT['West'] == Directions.NORTH
    assert Directions.REVERSE['West'] == Directions.EAST


def test_configuration():
    config = Configuration((0, 0), Directions.STOP)
    config2 = Configuration((0, 0), Directions.STOP)

    assert (0, 0) == config.get_position()
    assert Directions.STOP == config.get_direction()
    assert config.is_integer()
    assert config == config2

    config = config.generate_successor([1, 0])
    assert config != config2

    assert str(config) == "(x,y)=(1, 0), East"


def test_actions(state: GameState):
    state.reset()
    assert Actions.get_action_with_index(0) == 'North'
    assert Actions.get_action_with_index(3) == 'West'
    with pytest.raises(Exception) as ex:
        Actions.get_action_with_index(-1)
    assert "Invalid action index!" in str(ex.value)

    assert Actions.reverse_direction('North') == 'South'
    assert Actions.reverse_direction('South') == 'North'
    assert Actions.reverse_direction('East') == 'West'
    assert Actions.reverse_direction('West') == 'East'

    assert Actions.vector_to_direction((0, 1)) == 'North'
    assert Actions.vector_to_direction((0, -1)) == 'South'
    assert Actions.vector_to_direction((1, 0)) == 'East'
    assert Actions.vector_to_direction((-1, 0)) == 'West'
    assert Actions.vector_to_direction((0, 0)) == 'Stop'

    assert Actions.direction_to_vector('East') == (1, 0)

    assert Actions.get_possible_actions(state.agent_states[0], state) == ['East', 'West', 'Stop']
    bomberman = state.get_bomberman()
    x, y = bomberman.get_position()
    direction = bomberman.get_direction()
    bomberman.configuration.pos = (x + 0.5, y)

    assert Actions.get_possible_actions(bomberman, state) == [direction]
    state.reset()

    state.get_enemy(1).configuration.pos = (x + 1, y)
    assert Actions.get_possible_actions(state.get_bomberman(), state, True) == ['West', 'Stop']


def test_ghost_rules(state: GameState):
    state.reset()
    assert EnemyRules.get_legal_actions(state, 1) == ['West']

    EnemyRules.apply_action(state, "Stop", 1)

    EnemyRules.apply_action(state, 'West', 1)
    assert state.get_enemy(1).get_direction() == 'West'

    assert EnemyRules.can_kill((0, 0), (0, 0))
    EnemyRules.check_death(state, 0)
    EnemyRules.check_death(state, 1)
    state.get_enemy(1).configuration = state.get_bomberman().configuration

    # kill bomberman
    EnemyRules.check_death(state, 1)
    assert state.is_lose()
    state.reset()

    state.get_enemy(1).configuration = state.get_bomberman().configuration
    # kill bomberman
    EnemyRules.check_death(state, 0)
    assert state.is_lose()


def test_pacman_rules(state: GameState):
    state.reset()
    assert BombermanRules.get_legal_actions(state) == ['East', 'West', 'Stop', 'Bomb']
    assert BombermanRules.get_legal_actions(state, True) == ['East', 'West', 'Stop', 'Bomb']

    # not in legal
    BombermanRules.apply_action(state, 'North')
    assert state.get_bomberman().get_direction() == 'Stop'

    state.get_bomberman().configuration.direction = 'North'
    BombermanRules.apply_action(state, 'North')
    assert state.get_bomberman().get_direction() == 'North'

    # legal
    BombermanRules.apply_action(state, 'East')
    assert state.get_bomberman().get_direction() == 'East'

    # Bomb
    BombermanRules.apply_action(state, 'Bomb')
    assert BombermanRules.get_legal_actions(state) == ['East', 'West']

    state.reset()


def test_agent_states():
    bomberman = AgentState(Configuration((0, 0), 'Stop'), True)
    enemy = AgentState(Configuration((0, 1), 'Stop'), False)

    assert str(bomberman) == "Bomberman: (x,y)=(0, 0), Stop"
    assert str(enemy) == "Enemy: (x,y)=(0, 1), Stop"

    assert bomberman != enemy

    assert bomberman

    assert bomberman == bomberman.copy()

    assert bomberman.get_position() == (0, 0)
    assert bomberman.get_direction() == 'Stop'
    bomberman.configuration = None
    assert bomberman.get_position() is None


def test_game_state(state: GameState):
    with pytest.raises(Exception) as ex:
        state.get_enemy(0)
    assert 'Invalid index' in str(ex.value)

    assert not state.get_enemy(1).is_bomberman

    assert state.get_bomberman().is_bomberman

    # test win and lose
    with pytest.raises(Exception) as ex:
        state._win = True
        state.generate_successor(0, "East")

    assert "Can\'t generate a successor of a terminal state." in str(ex.value)

    assert state.get_legal_actions(0) == []

    state.reset()
    # test win and lose
    with pytest.raises(Exception) as ex:
        state._lose = True
        state.generate_successor(0, "East")

    assert "Can\'t generate a successor of a terminal state." in str(ex.value)

    state.reset()
    assert state.get_legal_actions(0, True) == ["East", "West", "Stop", "Bomb"]
    assert state.get_legal_actions(1) == ["West"]

    state.reset()
    state.generate_successor(0, 'Bomb')

    assert np.sum(
        state.to_observation()
    ) == len(state.get_bombs()) + len(state.agent_states) + state.layout.walls.count() + state.layout.bricks.count()

    state.generate_successor(0, 'East')
    assert state.layout.shape == (5, 9)
    assert np.bincount(state.to_observation_((5, 9, 1)).reshape((-1)).astype(np.int8))[2] == state.layout.walls.count()
    assert np.bincount(state.to_observation_((5, 9, 1)).reshape((-1)).astype(np.int8))[3] == state.layout.bricks.count()
    assert np.bincount(state.to_observation_((5, 9, 1)).reshape((-1)).astype(np.int8))[4] == 1
    assert np.bincount(state.to_observation_((5, 9, 1)).reshape((-1)).astype(np.int8))[5] == 1
    state.generate_successor(0, 'Bomb')
    state.generate_successor(0, 'East')
    assert np.bincount(state.to_observation_((5, 9, 1)).reshape((-1)).astype(np.int8))[5] == 2
    state.generate_successor(0, 'East')
    assert str(state) == """% % % % % % % % %
%       E #     %
%   % # % # %   %
%     0 o   B   %
% % % % % % % % %"""
    assert np.bincount(state.to_observation_((5, 9, 1)).reshape((-1)).astype(np.int8))[5] == 1
    assert np.bincount(state.to_observation_((5, 9, 1)).reshape((-1)).astype(np.int8))[6] == 1
    state.generate_successor(0, 'East')
    assert np.bincount(state.to_observation_((5, 9, 1)).reshape((-1)).astype(np.int8))[7] == 1
    print(state)
    assert str(state) == """% % % % % % % % %
%       E #     %
%   % # % # %   %
%     O 0     B %
% % % % % % % % %"""
    state.generate_successor(0, 'East')

    assert str(state) == """% % % % % % % % %
%       E #     %
%   %   % # %   %
% * * * * * * B %
% % % % % % % % %"""

    assert np.bincount(state.to_observation_((5, 9, 1)).reshape((-1)).astype(np.int8))[8] == 6
    assert np.bincount(state.to_observation_((5, 9, 1)).reshape((-1)).astype(np.int8))[3] == state.layout.bricks.count()
