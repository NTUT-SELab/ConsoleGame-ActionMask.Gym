from env.Pacman.utils import manhattanDistance, nearestPoint
from env.Pacman.map_define import MapObsEnum, MapEnum
import numpy as np

SCARED_TIME = 40  # Moves ghosts are scared
COLLISION_TOLERANCE = 0.7  # How close ghosts must be to Pacman to kill
TIME_PENALTY = 1  # Number of points lost each round


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

    def getPosition(self):
        return (self.pos)

    def getDirection(self):
        return self.direction

    def isInteger(self):
        x, y = self.pos
        return x == int(x) and y == int(y)

    def __eq__(self, other):
        if other is None:
            return False
        return (self.pos == other.pos and self.direction == other.direction)

    def __str__(self):
        return "(x,y)=" + str(self.pos) + ", " + str(self.direction)

    def generateSuccessor(self, vector):
        """
        Generates a new configuration reached by translating the current
        configuration by the action vector.  This is a low-level call and does
        not attempt to respect the legality of the movement.
        Actions are movement vectors.
        """
        x, y = self.pos
        dx, dy = vector
        direction = Actions.vectorToDirection(vector)
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

    _directionsAsList = list(_directions.items())

    TOLERANCE = .001

    @staticmethod
    def getActionWithIndex(index):
        if index >= len(Actions._directionsAsList) or index < 0:
            raise Exception("Invalid action index!")
        return Actions._directionsAsList[index][0]

    @staticmethod
    def reverseDirection(action):
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
    def vectorToDirection(vector):
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
    def directionToVector(direction, speed=1.0):
        dx, dy = Actions._directions[direction]
        return (dx * speed, dy * speed)

    @staticmethod
    def getPossibleActions(agentState, walls, ghosts=[]):
        possible = []
        x, y = agentState.getPosition()
        x_int, y_int = int(x + 0.5), int(y + 0.5)

        # In between grid points, all agents must continue straight
        if (abs(x - x_int) + abs(y - y_int) > Actions.TOLERANCE):
            return [agentState.getDirection()]

        for dir, vec in Actions._directionsAsList:
            dx, dy = vec
            next_y = y_int + dy
            next_x = x_int + dx
            if not walls[next_x][next_y]:
                if agentState.isPacman:
                    for ghostState in ghosts:
                        if (next_x,
                            next_y) == nearestPoint(ghostState.configuration.pos) and ghostState.scaredTimer <= 1:
                            break
                    else:
                        possible.append(dir)
                else:
                    possible.append(dir)

        return possible


class GhostRules:
    GHOST_SPEED = 1.0

    @staticmethod
    def getLegalActions(state, ghostIndex):
        """
        Ghosts cannot stop, and cannot turn around unless they
        reach a dead end, but can turn 90 degrees at intersections.
        """
        agentState = state.getGhostState(ghostIndex)

        possibleActions = Actions.getPossibleActions(agentState, state.layout.walls)

        reverse = Actions.reverseDirection(agentState.getDirection())
        if Directions.STOP in possibleActions:
            possibleActions.remove(Directions.STOP)
        if reverse in possibleActions and len(possibleActions) > 1:
            possibleActions.remove(reverse)

        return possibleActions

    @staticmethod
    def applyAction(state, action, ghostIndex):
        legal = GhostRules.getLegalActions(state, ghostIndex)
        if action not in legal:
            raise Exception("Illegal ghost action " + str(action))

        ghostState = state.getGhostState(ghostIndex)
        speed = GhostRules.GHOST_SPEED
        if ghostState.scaredTimer > 0:
            speed /= 2.0
        vector = Actions.directionToVector(action, speed)
        ghostState.configuration = ghostState.configuration.generateSuccessor(vector)

    @staticmethod
    def decrementTimer(ghostState):
        timer = ghostState.scaredTimer
        if timer == 1:
            ghostState.configuration.pos = nearestPoint(ghostState.configuration.pos)
        ghostState.scaredTimer = max(0, timer - 1)

    @staticmethod
    def canKill(pacmanPosition, ghostPosition):
        return manhattanDistance(ghostPosition, pacmanPosition) <= COLLISION_TOLERANCE

    @staticmethod
    def checkDeath(state, agentIndex):
        pacmanPosition = state.getPacmanPosition()
        if agentIndex == 0:  # Pacman just moved; Anyone can kill him
            for index in range(1, len(state.agentStates)):
                ghostState = state.agentStates[index]
                ghostPosition = ghostState.configuration.getPosition()
                if GhostRules.canKill(pacmanPosition, ghostPosition):
                    GhostRules.collide(state, ghostState, index)
        else:
            ghostState = state.agentStates[agentIndex]
            ghostPosition = ghostState.configuration.getPosition()
            if GhostRules.canKill(pacmanPosition, ghostPosition):
                GhostRules.collide(state, ghostState, agentIndex)

    @staticmethod
    def collide(state, ghostState, agentIndex):
        if ghostState.scaredTimer > 0:
            state.scoreChange += 200
            GhostRules.placeGhost(state, ghostState)
            ghostState.scaredTimer = 0
        else:
            if not state._win:
                state.scoreChange -= 500
                state._lose = True

    @staticmethod
    def placeGhost(state, ghostState):
        ghostState.configuration = ghostState.start


class PacmanRules:
    PACMAN_SPEED = 1.0

    @staticmethod
    def getLegalActions(state, has_ghost=False):
        """
        Returns a list of possible actions.
        """

        if has_ghost:
            return Actions.getPossibleActions(
                state.getPacmanState(), state.layout.walls,
                [state.getGhostState(i) for i in range(1, state.getNumAgents())]
            )
        else:
            return Actions.getPossibleActions(state.getPacmanState(), state.layout.walls)

    @staticmethod
    def applyAction(state, action):
        """
        Edits the state to reflect the results of the action.
        """
        legal = PacmanRules.getLegalActions(state)
        pacmanState = state.getPacmanState()

        if action not in legal:
            if pacmanState.getDirection() in legal:
                action = pacmanState.getDirection()
            else:
                action = Directions.STOP
            # raise Exception("Illegal action " + str(action))

        # Update Configuration
        vector = Actions.directionToVector(action, PacmanRules.PACMAN_SPEED)
        pacmanState.configuration = pacmanState.configuration.generateSuccessor(vector)

        # Eat
        next = pacmanState.configuration.getPosition()
        nearest = nearestPoint(next)
        if manhattanDistance(nearest, next) <= 0.5:
            # Remove food
            PacmanRules.consume(nearest, state)

    @staticmethod
    def consume(position, state):
        x, y = position
        # Eat food
        if state.layout.food[x][y]:
            state.scoreChange += 10
            state.layout.food = state.layout.food.copy()
            state.layout.food[x][y] = False

            numFood = state.getNumFood()
            if numFood == 0 and not state.isLose():
                state.scoreChange += 500
                state._win = True
        # Eat capsule
        if (position in state.getCapsules()):
            state.layout.capsules.remove(position)
            # Reset all ghosts' scared timers
            for index in range(1, len(state.agentStates)):
                state.agentStates[index].scaredTimer = SCARED_TIME


class AgentState:

    def __init__(self, startConfiguration, isPacman=False):
        self.start = startConfiguration
        self.isPacman = isPacman
        self.scaredTimer = 0
        self.configuration = startConfiguration

    def __str__(self):
        if self.isPacman:
            return "Pacman: " + str(self.configuration)
        else:
            return "Ghost: " + str(self.configuration)

    def __eq__(self, other):
        if other is None:
            return False
        return self.configuration == other.configuration and self.scaredTimer == other.scaredTimer

    def copy(self):
        state = AgentState(self.start, self.isPacman)
        state.configuration = self.configuration
        state.scaredTimer = self.scaredTimer
        return state

    def getPosition(self):
        if self.configuration is None:
            return None
        return self.configuration.getPosition()

    def getDirection(self):
        return self.configuration.getDirection()


class GameState:

    def __init__(self, layout):
        self.layout = layout
        self.agentStates = [
            AgentState(Configuration(pos, Directions.STOP), isPacman) for isPacman, pos in layout.agentPositions
        ]
        self.score = 0
        self.scoreChange = 0
        self._win = False
        self._lose = False

    def getGhostState(self, agentIndex):
        if agentIndex == 0 or agentIndex >= len(self.agentStates):
            raise Exception("Invalid index")

        return self.agentStates[agentIndex]

    def getGhostPosition(self, agentIndex):
        if agentIndex == 0 or agentIndex >= len(self.agentStates):
            raise Exception("Invalid index")

        return self.agentStates[agentIndex].getPosition()

    def getPacmanState(self):
        return self.agentStates[0]

    def getPacmanPosition(self):
        return self.agentStates[0].getPosition()

    def getPacmanDirection(self):
        return self.agentStates[0].getDirection()

    def deepCopy(self):
        layout = self.layout.deepCopy()
        state = GameState(layout)
        state.score = self.score
        state.scoreChange = self.scoreChange
        state._win = self._win
        state._lose = self._lose
        state.agentStates = []
        for agentState in self.agentStates:
            state.agentStates.append(agentState.copy())

        return state

    def reset(self):
        self.layout.reset()
        self.agentStates = [
            AgentState(Configuration(pos, Directions.STOP), isPacman) for isPacman, pos in self.layout.agentPositions
        ]
        self.score = 0
        self.scoreChange = 0
        self._win = False
        self._lose = False

    def getNumFood(self):
        return self.layout.food.count()

    def getCapsules(self):
        return self.layout.capsules

    def isWin(self):
        return self._win

    def isLose(self):
        return self._lose

    def getNumAgents(self):
        return len(self.agentStates)

    def getLegalActions(self, agentIndex=0, has_ghost=False):
        """
        Returns the legal actions for the agent specified.
        """
        # GameState.explored.add(self)
        if self.isWin() or self.isLose():
            return []

        if agentIndex == 0:  # Pacman is moving
            return PacmanRules.getLegalActions(self, has_ghost)
        else:
            return GhostRules.getLegalActions(self, agentIndex)

    def generateSuccessor(self, agentIndex, action):
        """
        Returns the successor state after the specified agent takes the action.
        """
        self.scoreChange = 0
        # Check that successors exist
        if self.isWin() or self.isLose():
            raise Exception('Can\'t generate a successor of a terminal state.')

        # Let agent's logic deal with its action's effects on the board
        if agentIndex == 0:  # Pacman is moving
            PacmanRules.applyAction(self, action)
        else:  # A ghost is moving
            GhostRules.applyAction(self, action, agentIndex)

        # Time passes
        if agentIndex == 0:
            self.scoreChange += -TIME_PENALTY  # Penalty for waiting around
        else:
            GhostRules.decrementTimer(self.agentStates[agentIndex])

        # Resolve multi-agent effects
        GhostRules.checkDeath(self, agentIndex)

        # Book keeping
        self.score += self.scoreChange

        return self

    def toObservationMatrix(self):
        """
        Convert map data to neural network input format.
        """

        def getWallMatrix(state):
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

        def getPacmanMatrix(state):
            """ Return matrix with pacman coordinates set to 1 """
            width, height = state.layout.width, state.layout.height
            matrix = np.zeros((height, width), dtype=np.int8)

            for agentState in state.agentStates:
                if agentState.isPacman:
                    pos = agentState.configuration.getPosition()
                    cell = 1
                    matrix[-1 - int(pos[1])][int(pos[0])] = cell

            return matrix

        def getGhostMatrix(state):
            """ Return matrix with ghost coordinates set to 1 """
            width, height = state.layout.width, state.layout.height
            matrix = np.zeros((height, width), dtype=np.int8)

            for agentState in state.agentStates:
                if not agentState.isPacman:
                    if not agentState.scaredTimer > 0:
                        pos = agentState.configuration.getPosition()
                        cell = 1
                        matrix[-1 - int(pos[1])][int(pos[0])] = cell

            return matrix

        def getScaredGhostMatrix(state):
            """ Return matrix with ghost coordinates set to 1 """
            width, height = state.layout.width, state.layout.height
            matrix = np.zeros((height, width), dtype=np.int8)

            for agentState in state.agentStates:
                if not agentState.isPacman:
                    if agentState.scaredTimer > 0:
                        pos = agentState.configuration.getPosition()
                        cell = 1
                        matrix[-1 - int(pos[1])][int(pos[0])] = cell

            return matrix

        def getFoodMatrix(state):
            """ Return matrix with food coordinates set to 1 """
            width, height = state.layout.width, state.layout.height
            grid = state.layout.food
            matrix = np.zeros((height, width), dtype=np.int8)

            for i in range(grid.height):
                for j in range(grid.width):
                    # Put cell vertically reversed in matrix
                    cell = 1 if grid[j][i] else 0
                    matrix[-1 - i][j] = cell

            return matrix

        def getCapsulesMatrix(state):
            """ Return matrix with capsule coordinates set to 1 """
            width, height = state.layout.width, state.layout.height
            capsules = state.layout.capsules
            matrix = np.zeros((height, width), dtype=np.int8)

            for i in capsules:
                # Insert capsule cells vertically reversed into matrix
                matrix[-1 - i[1], i[0]] = 1

            return matrix

        observation = np.zeros((6, self.layout.height, self.layout.width), dtype=np.int8)

        observation[0] = getWallMatrix(self)
        observation[1] = getPacmanMatrix(self)
        observation[2] = getGhostMatrix(self)
        observation[3] = getScaredGhostMatrix(self)
        observation[4] = getFoodMatrix(self)
        observation[5] = getCapsulesMatrix(self)

        observation = np.swapaxes(observation, 0, 2)

        return observation

    def toObservation(self, shape):
        """
        Convert map data to neural network input format.

        : param shape:      (obs_shape) 神經網路輸入的形狀
        """
        map_data = np.zeros((self.layout.shape[0], self.layout.shape[1]))
        map_data[self.layout.walls.data.T[::-1]] = MapObsEnum.wall.value
        map_data[self.layout.food.data.T[::-1]] = MapObsEnum.food.value
        for pos in self.layout.capsules:
            map_data[-1 - int(pos[1])][int(pos[0])] = MapObsEnum.capsules.value

        for agentState in self.agentStates:
            pos = agentState.configuration.getPosition()
            if agentState.isPacman:
                map_data[-1 - int(pos[1])][int(pos[0])] = MapObsEnum.pacman.value
            elif agentState.scaredTimer > 0:
                map_data[-1 - int(pos[1])][int(pos[0])] = MapObsEnum.fleeghost.value
            else:
                map_data[-1 - int(pos[1])][int(pos[0])] = MapObsEnum.ghost.value

        return np.reshape(map_data.astype(np.float16), shape)

    def __str__(self):
        layout = self.layout.deepCopy()
        map_data = np.full((layout.height, layout.width), ' ')
        map_data[layout.walls.data.T[::-1]] = MapEnum.wall.value
        map_data[layout.food.data.T[::-1]] = MapEnum.food.value
        for pos in layout.capsules:
            map_data[-1 - int(pos[1])][int(pos[0])] = MapEnum.capsules.value

        for agentState in self.agentStates:
            pos = agentState.configuration.getPosition()
            if agentState.isPacman:
                map_data[-1 - int(pos[1])][int(pos[0])] = MapEnum.pacman.value
            elif agentState.scaredTimer > 0:
                map_data[-1 - int(pos[1])][int(pos[0])] = MapEnum.fleeghost.value
            else:
                map_data[-1 - int(pos[1])][int(pos[0])] = MapEnum.ghost.value

        out = [[str(map_data[y][x])[0] for x in range(layout.width)] for y in range(layout.height)]
        return '\n'.join([' '.join(x) for x in out])
