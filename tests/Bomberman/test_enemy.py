from env.Bomberman.enemy import EnemyAgents
from env.Bomberman.game import GameState


def test_enemy_agents(state: GameState):
    assert EnemyAgents.get_action(1, state) == "West"
    state.generate_successor(1, "West")

    assert EnemyAgents.get_action(1, state) == "West"
    state.generate_successor(1, "West")

    assert EnemyAgents.get_action(1, state) == "West"
    state.generate_successor(1, "West")

    assert EnemyAgents.get_action(1, state) == "East"
    state.generate_successor(1, "East")

    assert EnemyAgents.get_action(1, state) == "East"
    state.generate_successor(1, "East")

    assert EnemyAgents.get_action(1, state) == "East"
