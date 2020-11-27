# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from util import manhattanDistance
from game import Directions
import random, util
import math

from game import Agent


def convertActionToPosition(current_position, action):
    # action should be a legal action
    if action == "Stop":
        return current_position
    if action == "West":
        return current_position[0] - 1, current_position[1]
    if action == "East":
        return current_position[0] + 1, current_position[1]
    if action == "North":
        return current_position[0], current_position[1] + 1
    if action == "South":
        return current_position[0], current_position[1] - 1

    # Invalid action!
    return -1, -1


def mazeDistanceToClosestPoint(state, pointsList):
    # Basically the same BFS code from mmn11
    calculatedPositions = []
    frontier = util.Queue()

    frontier.push((state, 0))
    while not frontier.isEmpty():
        currentState, distance = frontier.pop()

        if currentState.getPacmanPosition() in calculatedPositions:
            continue
        calculatedPositions.append(currentState.getPacmanPosition())

        for p in pointsList:
            if util.manhattanDistance(currentState.getPacmanPosition(), p) < 1:
                return distance

        for action in currentState.getLegalActions():
            successor = currentState.generatePacmanSuccessor(action)
            if successor.getPacmanPosition() in calculatedPositions:
                continue
            frontier.push((successor, distance + 1))

    return float("Inf")

def manhattanDistanceToClosestPoint(state, pointsList):
    minimumDistance = float("Inf")

    for point in pointsList:
        distance = util.manhattanDistance(state.getPacmanPosition(), point)
        minimumDistance = min(distance, minimumDistance)

    return minimumDistance


class ReflexAgent(Agent):
  """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
  """


  def getAction(self, gameState):
    """
    You do not need to change this method, but you're welcome to.

    getAction chooses among the best options according to the evaluation function.

    Just like in the previous project, getAction takes a GameState and returns
    some Directions.X for some X in the set {North, South, West, East, Stop}
    """
    # Collect legal moves and successor states
    legalMoves = gameState.getLegalActions()

    # Choose one of the best actions
    scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
    bestScore = max(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices) # Pick randomly among the best

    "Add more of your code here if you want to"
    return legalMoves[chosenIndex]

  def evaluationFunction(self, currentGameState, action):
    """
    Design a better evaluation function here.

    The evaluation function takes in the current and proposed successor
    GameStates (pacman.py) and returns a number, where higher numbers are better.

    The code below extracts some useful information from the state, like the
    remaining food (oldFood) and Pacman position after moving (newPos).
    newScaredTimes holds the number of moves that each ghost will remain
    scared because of Pacman having eaten a power pellet.

    Print out these variables to see what you're getting, then combine them
    to create a masterful evaluation function.
    """
    # Useful information you can extract from a GameState (pacman.py)
    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newFood = currentGameState.getFood().asList()
    newGhostStates = successorGameState.getGhostStates()
    boardWidth = currentGameState.data.layout.width
    boardHeight = currentGameState.data.layout.height

    oldFoodCount = currentGameState.getNumFood()
    newFoodCount = successorGameState.getNumFood()

    totalValue = 0

    # Since openClassic doesn't have any walls, we better use manhattan distance instead of maze distance
    # In mazes where there are walls, you should use mazeDistanceToClosestPoint as distanceFunction
    distanceFunction = manhattanDistanceToClosestPoint

    # Checks if any of the ghosts was eaten in the successor state (indicated by drastic change in location)
    ghostsEaten = 0
    for currentGhost, successorGhost in zip(currentGameState.getGhostStates(), newGhostStates):
        if util.manhattanDistance(currentGhost.getPosition(), successorGhost.getPosition()) > 1:
            ghostsEaten += 1

    # Implements a mechanism for escaping ghosts (keeps a distance of `safeDistance` away from closest ghost)
    safeDistance = 3
    normalGhosts = [util.nearestPoint(ghost.getPosition()) for ghost in newGhostStates if ghost.scaredTimer == 0]
    if len(normalGhosts) > 0:  # If there are normal ghosts
        distanceFromClosestGhost = distanceFunction(successorGameState, normalGhosts)

        # If a ghost was eaten and other ghosts are not close, we should do this action!
        if ghostsEaten > 0 and distanceFromClosestGhost > safeDistance:
            return (boardWidth + boardHeight) * 100  # Eat the ghost!

        # If a ghost is too close, we should avoid this action, according to the distance
        if distanceFromClosestGhost <= safeDistance:
            totalValue += -50 * (safeDistance - distanceFromClosestGhost)
    elif ghostsEaten > 0:  # If there are no normal ghosts and we have eaten a ghost with this action
        return (boardWidth + boardHeight) * 100  # Eat the ghost!

    # Implements a mechanism for hunting scared ghosts
    # We prioritize hunting a ghost over eating food (we do this by multiplying the distance difference by 5)
    scaredGhosts = [convertActionToPosition(ghost.getPosition(), ghost.getDirection()) for ghost in newGhostStates if ghost.scaredTimer > 0]
    if len(scaredGhosts) > 0:
        distanceFromClosestGhost = distanceFunction(successorGameState, scaredGhosts)
        totalValue += (boardWidth + boardHeight - distanceFromClosestGhost) * 5  # multiply by 5 to prefer eating a ghost

    # Implements food eating: First we check if we just ate some food, and if not,
    #                         Adds some points according to the distance to the closest food
    if oldFoodCount > newFoodCount:  # If we ate some food in the successor state
        distanceFromClosestFood = 0
    elif newFoodCount > 0:  # Checks distance to closest food (makes sure some food exists)
        distanceFromClosestFood = distanceFunction(successorGameState, newFood)
    else:  # Should not occur
        distanceFromClosestFood = 0  # Defaults to zero

    totalValue += boardWidth + boardHeight - distanceFromClosestFood

    return totalValue

def scoreEvaluationFunction(currentGameState):
  """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
  """
  return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
  """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
  """

  def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
    self.index = 0 # Pacman is always agent index 0
    self.evaluationFunction = util.lookup(evalFn, globals())
    self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
  """
    Your minimax agent (question 2)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action from the current gameState using self.depth
      and self.evaluationFunction.

      Here are some method calls that might be useful when implementing minimax.

      gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game
    """
    value, action = self.calculateMinimaxState(gameState, self.depth, 0)
    return action

  def calculateMinimaxState(self, state, depth, agentIndex):
      # If we calculated all agents in all depths
      if depth == 0 and agentIndex == 0:
          return self.evaluationFunction(state), Directions.STOP

      # Calculate index of next agent
      nextAgentIndex = agentIndex + 1
      if nextAgentIndex >= state.getNumAgents():
          depth -= 1
          nextAgentIndex = 0

      # Set parameters of node according to agent (max node for pacman, min node for ghost)
      if agentIndex == 0:
          # Max node
          value = -float("Inf")
          compareFunction = max
      else:
          # Min node
          value = float("Inf")
          compareFunction = min

      if len(state.getLegalActions(agentIndex)) == 0:
          stateValue, _ = self.calculateMinimaxState(state, depth, nextAgentIndex)
          return stateValue, Directions.STOP

      bestAction = Directions.STOP
      Actions = state.getLegalActions(agentIndex)
      """
      #     Uncomment this to remove 'Stop' action
      if Directions.STOP in Actions:
          Actions.remove(Directions.STOP)
      """

      for action in Actions:
          successorState = state.generateSuccessor(agentIndex, action)
          stateValue, _ = self.calculateMinimaxState(successorState, depth, nextAgentIndex)
          value = compareFunction(value, stateValue)
          if value == stateValue:
              bestAction = action

      return value, bestAction


class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (question 3)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    value, action = self.calculateAlphaBetaState(gameState, self.depth, 0, -float("Inf"), float("Inf"))
    return action

  def calculateAlphaBetaState(self, state, depth, agentIndex, alpha, beta):
      # If we calculated all agents in all depths
      if depth == 0 and agentIndex == 0:
          return self.evaluationFunction(state), Directions.STOP

      # Calculate index of next agent
      nextAgentIndex = agentIndex + 1
      if nextAgentIndex >= state.getNumAgents():
          depth -= 1
          nextAgentIndex = 0

      # Set parameters of node according to agent (max node for pacman, min node for ghost)
      if agentIndex == 0:
          # Max node
          value = -float("Inf")
          compareFunction = max
      else:
          # Min node
          value = float("Inf")
          compareFunction = min

      if len(state.getLegalActions(agentIndex)) == 0:
          stateValue, _ = self.calculateAlphaBetaState(state, depth, nextAgentIndex, alpha, beta)
          return stateValue, Directions.STOP

      bestAction = Directions.STOP
      Actions = state.getLegalActions(agentIndex)

      """
      #     Uncomment this to remove 'Stop' action
      if Directions.STOP in Actions:
          Actions.remove(Directions.STOP)
      """

      for action in Actions:
          successorState = state.generateSuccessor(agentIndex, action)
          stateValue, _ = self.calculateAlphaBetaState(successorState, depth, nextAgentIndex, alpha, beta)
          value = compareFunction(value, stateValue)
          if value == stateValue:
              bestAction = action

          # Check for node type (min/max) and check for pruning
          if agentIndex == 0:
              if value > beta:
                  return value, bestAction
              alpha = max(alpha, value)
          else:
              if value < alpha:
                  return value, bestAction
              beta = min(beta, value)


      return value, bestAction

class ExpectimaxAgent(MultiAgentSearchAgent):
  """
    Your expectimax agent (question 4)
  """

  def getAction(self, gameState):
    """
      Returns the expectimax action using self.depth and self.evaluationFunction

      All ghosts should be modeled as choosing uniformly at random from their
      legal moves.
    """
    value, action = self.calculateExpectimaxState(gameState, self.depth, 0)
    return action

  def calculateExpectimaxState(self, state, depth, agentIndex):
      # If we calculated all agents in all depths
      if depth == 0 and agentIndex == 0:
          return self.evaluationFunction(state), Directions.STOP

      # Calculate index of next agent
      nextAgentIndex = agentIndex + 1
      if nextAgentIndex >= state.getNumAgents():
          depth -= 1
          nextAgentIndex = 0

      # Set parameters of node according to agent (max node for pacman, min node for ghost)
      if agentIndex == 0:
          # Max node
          value = -float("Inf")
          estimationFunction = max
      else:
          # Min node
          value = 0
          estimationFunction = lambda totalSum, valueToAdd: totalSum + valueToAdd

      if len(state.getLegalActions(agentIndex)) == 0:
          stateValue, _ = self.calculateExpectimaxState(state, depth, nextAgentIndex)
          return stateValue, Directions.STOP

      bestAction = Directions.STOP
      Actions = state.getLegalActions(agentIndex)
      """
      #     Uncomment this to remove 'Stop' action
      if Directions.STOP in Actions:
          Actions.remove(Directions.STOP)
      """

      for action in Actions:
          successorState = state.generateSuccessor(agentIndex, action)
          stateValue, _ = self.calculateExpectimaxState(successorState, depth, nextAgentIndex)
          value = estimationFunction(value, stateValue)
          if value == stateValue:
              bestAction = action

      if agentIndex == 0:
          # With pacman, we select the best option!
          return value, bestAction
      else:
          # With ghost, we expect the average value
          average = float(value) / len(Actions)
          return average, Directions.STOP  # The action doesn't matter for the ghosts

def betterEvaluationFunction(currentGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
  """
  "*** YOUR CODE HERE ***"
  util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
  """
    Your agent for the mini-contest
  """

  def getAction(self, gameState):
    """
      Returns an action.  You can use any method you want and search to any depth you want.
      Just remember that the mini-contest is timed, so you have to trade off speed and computation.

      Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
      just make a beeline straight towards Pacman (or away from him if they're scared!)
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

