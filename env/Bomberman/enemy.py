import random
from env.Bomberman.game import GameState, Directions


class EnemyAgents:

    @staticmethod
    def get_action(agent_index, state: GameState):
        enemy_state = state.get_enemy(agent_index)
        enemy_direction = enemy_state.get_direction()

        possible = state.get_legal_actions(agent_index)

        if enemy_direction in possible:
            return enemy_direction

        if Directions.REVERSE.get(enemy_direction, Directions.STOP) != Directions.STOP:
            return Directions.REVERSE.get(enemy_direction)

        return random.choice(possible)
