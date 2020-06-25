import numpy as np
from env.Bomberman.map import Map
from env.Bomberman.utils import manhattanDistance
from env.Bomberman.map_define import MapEnum, MapObsEnum

TIME_PENALTY = 0  # Number of points lost each round
COLLISION_TOLERANCE = 0.001


class Directions:
    NORTH = 'North'
    SOUTH = 'South'
    EAST = 'East'
    WEST = 'West'
    STOP = 'Stop'

    LEFT = {NORTH: WEST, SOUTH: EAST, EAST: NORTH, WEST: SOUTH, STOP: STOP}

    RIGHT = dict([(y, x) for x, y in list(LEFT.items())])

    REVERSE = {NORTH: SOUTH, SOUTH: NORTH, EAST: WEST, WEST: EAST, STOP: STOP}


class Configuration:
    """
    A Configuration holds the (x,y) coordinate of a character, along with its
    traveling direction.
    The convention for positions, like a graph, is that (0,0) is the lower left corner, x increases
    horizontally and y increases vertically.  Therefore, north is the direction of increasing y, or (0,1).
    """

    def __init__(self, pos, direction):
        self.pos = pos
        self.direction = direction

    def get_position(self):
        return (self.pos)

    def get_direction(self):
        return self.direction

    def is_integer(self):
        x, y = self.pos
        return x == int(x) and y == int(y)

    def __eq__(self, other):
        if other is None:
            return False
        return (self.pos == other.pos and self.direction == other.direction)

    def __str__(self):
        return "(x,y)=" + str(self.pos) + ", " + str(self.direction)

    def generate_successor(self, vector):
        """
        Generates a new configuration reached by translating the current
        configuration by the action vector.  This is a low-level call and does
        not attempt to respect the legality of the movement.
        Actions are movement vectors.
        """
        x, y = self.pos
        dx, dy = vector
        direction = Actions.vector_to_direction(vector)
        if direction == Directions.STOP:
            direction = self.direction  # There is no stop direction
        return Configuration((x + dx, y + dy), direction)


class Actions:
    """
    A collection of static methods for manipulating move actions.
    """
    # Directions
    _directions = {
        Directions.NORTH: (0, 1),
        Directions.SOUTH: (0, -1),
        Directions.EAST: (1, 0),
        Directions.WEST: (-1, 0),
        Directions.STOP: (0, 0)
    }

    _directions_as_list = list(_directions.items())

    TOLERANCE = .001

    @staticmethod
    def get_action_with_index(index):
        if index > len(Actions._directions_as_list) or index < 0:
            raise Exception("Invalid action index!")

        if index == 5:
            return 'Bomb'

        return Actions._directions_as_list[index][0]

    @staticmethod
    def reverse_direction(action):
        if action == Directions.NORTH:
            return Directions.SOUTH
        if action == Directions.SOUTH:
            return Directions.NORTH
        if action == Directions.EAST:
            return Directions.WEST
        if action == Directions.WEST:
            return Directions.EAST
        return action

    @staticmethod
    def vector_to_direction(vector):
        dx, dy = vector
        if dy > 0:
            return Directions.NORTH
        if dy < 0:
            return Directions.SOUTH
        if dx < 0:
            return Directions.WEST
        if dx > 0:
            return Directions.EAST
        return Directions.STOP

    @staticmethod
    def direction_to_vector(direction, speed=1.0):
        dx, dy = Actions._directions[direction]
        return (dx * speed, dy * speed)

    @staticmethod
    def get_possible_actions(agent_state, state, exclude_enemy=False):
        possible = []
        x, y = agent_state.get_position()
        x_int, y_int = int(x + 0.5), int(y + 0.5)

        # In between grid points, all agents must continue straight
        if (abs(x - x_int) + abs(y - y_int) > Actions.TOLERANCE):
            return [agent_state.get_direction()]

        walls = state.get_walls()
        bricks = state.get_bricks()
        bombs = [bomb.pos for bomb in state.get_bombs()]

        for dir, vec in Actions._directions_as_list:
            dx, dy = vec
            next_y = y_int + dy
            next_x = x_int + dx
            if not walls[next_x][next_y] and not bricks[next_x][next_y] and (next_x, next_y) not in bombs:
                if exclude_enemy:
                    for agent in state.agent_states:
                        if not agent.is_bomberman and (next_x, next_y) == (agent.get_position()):
                            break
                    else:
                        possible.append(dir)

                else:
                    possible.append(dir)

        return possible


class Bomb:

    def __init__(self, pos):
        self.pos = pos
        self.countdown = 5
        self.range = 2
        self.exploded = False

    def next(self, state):
        self.countdown -= 1

        if self.exploded:
            return

        if self.countdown <= 0:
            bombs = state.get_bombs()
            bombs.remove(self)
            self.exploded = True
            self.explode(self.pos, state)

            x, y = self.pos

            for i in range(self.range):
                y += 1
                if self.explode((x, y), state):
                    break

            x, y = self.pos

            for i in range(self.range):
                y -= 1
                if self.explode((x, y), state):
                    break

            x, y = self.pos

            for i in range(self.range):
                x += 1
                if self.explode((x, y), state):
                    break

            x, y = self.pos

            for i in range(self.range):
                x -= 1
                if self.explode((x, y), state):
                    break

    def explode(self, position, state):
        walls = state.get_walls()
        bricks = state.get_bricks()
        agents = state.agent_states[:]
        bombs = state.get_bombs()[:]

        x, y = position
        x = int(x)
        y = int(y)

        if x < 0 or y < 0 or x >= state.width or y >= state.height:
            return True

        if walls[x][y]:
            return True  # block next

        if bricks[x][y]:
            bricks[x][y] = False
            state.score_item.append(10)
            state.score += 10
            return True

        for agent in agents:
            if agent.get_position() == position:
                if agent.is_bomberman and not state.is_win() and not state.is_lose():
                    # lose
                    state.score -= 500
                    state.score_item.append(-500)
                    state._lose = True
                else:
                    # kill enemy
                    state.score += 200
                    state.score_item.append(200)
                    state.agent_states.remove(agent)
                    if len(state.agent_states) == 1 and not state.is_win() and not state.is_lose():
                        state.score += 500
                        state.score_item.append(500)
                        state._win = True

        for bomb in bombs:
            if bomb.pos == position:
                bomb.countdown = 1
                bomb.next(state)

        state.explode_regions.append(position)
        return False


class EnemyRules:

    @staticmethod
    def get_legal_actions(state, enemy_index):
        possible = Actions.get_possible_actions(state.get_enemy(enemy_index), state)

        if Directions.STOP in possible:
            possible.remove(Directions.STOP)

        if possible == []:
            possible.append(Directions.STOP)

        return possible

    @staticmethod
    def apply_action(state, action, enemy_index):
        legal = EnemyRules.get_legal_actions(state, enemy_index)
        enemy = state.get_enemy(enemy_index)

        if action not in legal:
            action = Directions.STOP

        vector = Actions.direction_to_vector(action)
        enemy.configuration = enemy.configuration.generate_successor(vector)

    @staticmethod
    def can_kill(bomberman_position, enemy_position):
        return manhattanDistance(bomberman_position, enemy_position) <= COLLISION_TOLERANCE

    @staticmethod
    def check_death(state, agent_index):
        bomberman_position = state.get_bomberman().get_position()
        if agent_index == 0:
            for index in range(1, len(state.agent_states)):
                enemy_state = state.agent_states[index]
                enemy_position = enemy_state.get_position()
                if EnemyRules.can_kill(bomberman_position,
                                       enemy_position) and not state.is_win() and not state.is_lose():
                    state.score -= 500
                    state.score_item.append(-500)
                    state._lose = True
        else:
            enemy_state = state.agent_states[agent_index]
            enemy_position = enemy_state.get_position()
            if EnemyRules.can_kill(bomberman_position, enemy_position) and not state.is_win() and not state.is_lose():
                state.score -= 500
                state.score_item.append(-500)
                state._lose = True


class BombermanRules:

    @staticmethod
    def get_legal_actions(state, exclude_enemy=False):
        bomberman = state.get_bomberman()
        possible = Actions.get_possible_actions(bomberman, state, exclude_enemy)
        bombs = [bomb.pos for bomb in state.get_bombs()]

        if len(state.get_bombs()) < 3 and bomberman.get_position() not in bombs:
            possible.append('Bomb')

        return possible

    @staticmethod
    def apply_action(state, action):
        legal = BombermanRules.get_legal_actions(state)
        bomberman = state.get_bomberman()

        if action not in legal:
            action = Directions.STOP

        if action == 'Bomb':
            BombermanRules.place_bomb(bomberman.get_position(), state)
        else:
            vector = Actions.direction_to_vector(action)
            bomberman.configuration = bomberman.configuration.generate_successor(vector)

    @staticmethod
    def place_bomb(pos, state):
        state.get_bombs().append(Bomb(pos))


class AgentState:

    def __init__(self, start_configuration, is_bomberman=False):
        self.is_bomberman = is_bomberman
        self.configuration = start_configuration

    def __str__(self):
        if self.is_bomberman:
            return "Bomberman: " + str(self.configuration)
        else:
            return "Enemy: " + str(self.configuration)

    def __eq__(self, other):
        if other is None:
            return False
        return self.configuration == other.configuration

    def copy(self):
        state = AgentState(self.configuration, self.is_bomberman)
        state.configuration = self.configuration
        return state

    def get_position(self):
        if self.configuration is None:
            return None
        return self.configuration.get_position()

    def get_direction(self):
        return self.configuration.get_direction()


class GameState:

    def __init__(self, layout: Map):
        self.layout = layout
        self.reset()

    def reset(self):
        self.layout.reset()
        self.height = self.layout.height
        self.width = self.layout.width
        self._win = False
        self._lose = False
        self.score = 0
        self.score_item = []
        self.bombs = []
        self.explode_regions = []
        self.agent_states = [
            AgentState(Configuration(pos, Directions.STOP), i == 0) for i, pos in self.layout.agent_positions
        ]

    def get_legal_actions(self, agent_index, exclude_enemy=False):
        if agent_index >= len(self.agent_states) or agent_index < 0:
            raise Exception('Invalid index')

        if self._win or self._lose:
            return []

        if agent_index == 0:
            possible = BombermanRules.get_legal_actions(self, exclude_enemy)
        else:
            possible = EnemyRules.get_legal_actions(self, agent_index)

        return possible

    def is_win(self):
        return self._win

    def is_lose(self):
        return self._lose

    def get_bombs(self):
        return self.bombs

    def get_bomberman(self):
        return self.agent_states[0]

    def get_enemy(self, index=0):
        if index >= len(self.agent_states) or index <= 0:
            raise Exception('Invalid index for get_enemy')

        return self.agent_states[index]

    def get_walls(self):
        return self.layout.walls

    def get_bricks(self):
        return self.layout.bricks

    def generate_successor(self, agent_index, action):
        score_change = 0

        if agent_index >= len(self.agent_states) or agent_index < 0:
            raise Exception('Invalid index')

        if self._win or self._lose:
            raise Exception("Can\'t generate a successor of a terminal state.")

        if agent_index == 0:
            BombermanRules.apply_action(self, action)
        else:
            EnemyRules.apply_action(self, action, agent_index)

        # Time pass
        if agent_index == 0:
            self.score_item = []
            self.explode_regions = []
            score_change += -TIME_PENALTY
            if action != "Bomb":
                for bomb in self.bombs:
                    bomb.next(self)

        EnemyRules.check_death(self, agent_index)

        self.score += score_change

        return self

    def __str__(self):
        layout = self.layout
        map_data = np.full((layout.height, layout.width), ' ')
        map_data[layout.walls.data.T[::-1]] = MapEnum.wall.value
        map_data[layout.bricks.data.T[::-1]] = MapEnum.brick.value

        for bomb in self.bombs:
            if bomb.countdown >= 3:
                map_data[-1 - int(bomb.pos[1])][int(bomb.pos[0])] = MapEnum.bomb3.value
            elif bomb.countdown == 2:
                map_data[-1 - int(bomb.pos[1])][int(bomb.pos[0])] = MapEnum.bomb2.value
            elif bomb.countdown == 1:
                map_data[-1 - int(bomb.pos[1])][int(bomb.pos[0])] = MapEnum.bomb1.value

        for agent_state in self.agent_states:
            pos = agent_state.get_position()
            if agent_state.is_bomberman:
                map_data[-1 - int(pos[1])][int(pos[0])] = MapEnum.bomberman.value
            else:
                map_data[-1 - int(pos[1])][int(pos[0])] = MapEnum.enemy.value

        for pos in self.explode_regions:
            map_data[-1 - int(pos[1])][int(pos[0])] = MapEnum.bomb0.value

        out = [[str(map_data[y][x])[0] for x in range(layout.width)] for y in range(layout.height)]
        return '\n'.join([' '.join(x) for x in out])

    def to_observation(self):
        """
        Convert map data to neural network input format.
        """

        def get_wall_matrix(state):
            """ Return matrix with wall coordinates set to 1 """
            width, height = state.layout.width, state.layout.height
            grid = state.layout.walls
            matrix = np.zeros((height, width), dtype=np.int8)
            for i in range(grid.height):
                for j in range(grid.width):
                    # Put cell vertically reversed in matrix
                    cell = 1 if grid[j][i] else 0
                    matrix[-1 - i][j] = cell
            return matrix

        def get_brick_matrix(state):
            """ Return matrix with wall coordinates set to 1 """
            width, height = state.layout.width, state.layout.height
            grid = state.layout.bricks
            matrix = np.zeros((height, width), dtype=np.int8)
            for i in range(grid.height):
                for j in range(grid.width):
                    # Put cell vertically reversed in matrix
                    cell = 1 if grid[j][i] else 0
                    matrix[-1 - i][j] = cell
            return matrix

        def get_bomberman_matrix(state):
            """ Return matrix with pacman coordinates set to 1 """
            width, height = state.layout.width, state.layout.height
            matrix = np.zeros((height, width), dtype=np.int8)

            for agent_state in state.agent_states:
                if agent_state.is_bomberman:
                    pos = agent_state.get_position()
                    cell = 1
                    matrix[-1 - int(pos[1])][int(pos[0])] = cell

            return matrix

        def get_enemy_matrix(state):
            """ Return matrix with pacman coordinates set to 1 """
            width, height = state.layout.width, state.layout.height
            matrix = np.zeros((height, width), dtype=np.int8)

            for agent_state in state.agent_states:
                if not agent_state.is_bomberman:
                    pos = agent_state.get_position()
                    cell = 1
                    matrix[-1 - int(pos[1])][int(pos[0])] = cell

            return matrix

        def get_bomb3_matrix(state):
            """ Return matrix with pacman coordinates set to 1 """
            width, height = state.layout.width, state.layout.height
            matrix = np.zeros((height, width), dtype=np.int8)

            for bomb in state.bombs:
                if bomb.countdown >= 3:
                    pos = bomb.pos
                    cell = 1
                    matrix[-1 - int(pos[1])][int(pos[0])] = cell

            return matrix

        def get_bomb2_matrix(state):
            """ Return matrix with pacman coordinates set to 1 """
            width, height = state.layout.width, state.layout.height
            matrix = np.zeros((height, width), dtype=np.int8)

            for bomb in state.bombs:
                if bomb.countdown == 2:
                    pos = bomb.pos
                    cell = 1
                    matrix[-1 - int(pos[1])][int(pos[0])] = cell

            return matrix

        def get_bomb1_matrix(state):
            """ Return matrix with pacman coordinates set to 1 """
            width, height = state.layout.width, state.layout.height
            matrix = np.zeros((height, width), dtype=np.int8)

            for bomb in state.bombs:
                if bomb.countdown == 1:
                    pos = bomb.pos
                    cell = 1
                    matrix[-1 - int(pos[1])][int(pos[0])] = cell

            return matrix

        def get_bomb0_matrix(state):
            """ Return matrix with pacman coordinates set to 1 """
            width, height = state.layout.width, state.layout.height
            matrix = np.zeros((height, width), dtype=np.int8)

            for pos in state.explode_regions:
                cell = 1
                matrix[-1 - int(pos[1])][int(pos[0])] = cell

            return matrix

        observation = np.zeros((8, self.layout.height, self.layout.width), dtype=np.int8)

        observation[0] = get_wall_matrix(self)
        observation[1] = get_brick_matrix(self)
        observation[2] = get_bomberman_matrix(self)
        observation[3] = get_enemy_matrix(self)
        observation[4] = get_bomb3_matrix(self)
        observation[5] = get_bomb2_matrix(self)
        observation[6] = get_bomb1_matrix(self)
        observation[7] = get_bomb0_matrix(self)

        observation = np.swapaxes(observation, 0, 2)

        return observation

    def to_observation_(self, shape):
        """
        Convert map data to neural network input format.

        : param shape:      (obs_shape) 神經網路輸入的形狀
        """
        map_data = np.zeros((self.layout.shape[0], self.layout.shape[1]))
        map_data[self.layout.walls.data.T[::-1]] = MapObsEnum.wall.value
        map_data[self.layout.bricks.data.T[::-1]] = MapObsEnum.brick.value

        for bomb in self.bombs:
            pos = bomb.pos
            if bomb.countdown >= 3:
                map_data[-1 - int(pos[1])][int(pos[0])] = MapObsEnum.bomb3.value
            elif bomb.countdown == 2:
                map_data[-1 - int(pos[1])][int(pos[0])] = MapObsEnum.bomb2.value
            elif bomb.countdown == 1:
                map_data[-1 - int(pos[1])][int(pos[0])] = MapObsEnum.bomb1.value

        for pos in self.explode_regions:
            map_data[-1 - int(pos[1])][int(pos[0])] = MapObsEnum.bomb0.value

        for agent_state in self.agent_states:
            pos = agent_state.get_position()
            if agent_state.is_bomberman:
                map_data[-1 - int(pos[1])][int(pos[0])] = MapObsEnum.bomberman.value
            else:
                map_data[-1 - int(pos[1])][int(pos[0])] = MapObsEnum.enemy.value

        return np.reshape(map_data.astype(np.float16), shape)
