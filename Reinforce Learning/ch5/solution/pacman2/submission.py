from util import manhattanDistance
from game import Directions
import random, util
import decimal

from game import Agent

class ReflexAgent(Agent):
  """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
  """
  def __init__(self):
    self.lastPositions = []
    self.dc = None


  def getAction(self, gameState):
    """
    getAction chooses among the best options according to the evaluation function.

    getAction takes a GameState and returns some Directions.X for some X in the set {North, South, West, East, Stop}
    ------------------------------------------------------------------------------
    Description of GameState and helper functions:

    A GameState specifies the full game state, including the food, capsules,
    agent configurations and score changes. In this function, the |gameState| argument 
    is an object of GameState class. Following are a few of the helper methods that you 
    can use to query a GameState object to gather information about the present state 
    of Pac-Man, the ghosts and the maze.
    
    gameState.getLegalActions(): 
        Returns the legal actions for the agent specified. Returns Pac-Man's legal moves by default.

    gameState.generateSuccessor(agentIndex, action): 
        Returns the successor state after the specified agent takes the action. 
        Pac-Man is always agent 0.

    gameState.getPacmanState():
        Returns an AgentState object for pacman (in game.py)
        state.configuration.pos gives the current position
        state.direction gives the travel vector

    gameState.getGhostStates():
        Returns list of AgentState objects for the ghosts

    gameState.getNumAgents():
        Returns the total number of agents in the game

    gameState.getScore():
        Returns the score corresponding to the current state of the game

    
    The GameState class is defined in pacman.py and you might want to look into that for 
    other helper methods, though you don't need to.
    """
    # Collect legal moves and successor states
    legalMoves = gameState.getLegalActions()

    # Choose one of the best actions
    scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
    bestScore = max(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices) # Pick randomly among the best


    return legalMoves[chosenIndex]

  def evaluationFunction(self, currentGameState, action):
    """
    The evaluation function takes in the current and proposed successor
    GameStates (pacman.py) and returns a number, where higher numbers are better.

    The code below extracts some useful information from the state, like the
    remaining food (oldFood) and Pacman position after moving (newPos).
    newScaredTimes holds the number of moves that each ghost will remain
    scared because of Pacman having eaten a power pellet.
    """
    # Useful information you can extract from a GameState (pacman.py)
    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = successorGameState.getPacmanPosition()
    oldFood = currentGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    return successorGameState.getScore()


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

######################################################################################
# Problem: implementing minimax

class MinimaxAgent(MultiAgentSearchAgent):
  """
    Your minimax agent
  """
  
  def V(self, gameState, player, d):
    # Set legal moves
    legalMoves = gameState.getLegalActions(player)
    random.shuffle(legalMoves)
      
    is_end = gameState.isWin() or gameState.isLose() or len(legalMoves) == 0
    
    # If IsEnd(s)
    if is_end:
      return gameState.getScore()
    
    # If depth = 0
    if d == 0:
      return self.evaluationFunction(gameState)
    
    # Maximizing player
    if player == 0:
      value = decimal.Decimal('-Infinity')
      for action in legalMoves:
        value = max(value, self.V(gameState.generateSuccessor(player, action), player+1, d))
      return value
      
    # 1 ~ n-1 minimizing players
    elif player < (gameState.getNumAgents() - 1):
      value = decimal.Decimal('Infinity')
      for action in legalMoves:
        value = min(value, self.V(gameState.generateSuccessor(player, action), player+1, d))
      return value
    
    # Last(n-th) minimizing player
    else:
      value = decimal.Decimal('Infinity')
      for action in legalMoves:
        value = min(value, self.V(gameState.generateSuccessor(player, action), 0, d-1))
      return value

  def getAction(self, gameState):
    player = self.index
    
    legalMoves = gameState.getLegalActions(player)
    random.shuffle(legalMoves)
    
    # Maximizing player
    if player == 0:
        return max(legalMoves, key=lambda x: self.V(
          gameState.generateSuccessor(player, x), player + 1, self.depth))
    # Minimizing player  
    else:
        raise Exception('Unnecessary part')

######################################################################################
# Problem: implementing alpha-beta

class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning
  """
  
  def V(self, gameState, player, d, alpha, beta):
    # Set legal moves
    legalMoves = gameState.getLegalActions(player)
      
    is_end = gameState.isWin() or gameState.isLose() or len(legalMoves) == 0
    
    # If IsEnd(s)
    if is_end:
      return gameState.getScore()
    
    # If depth = 0
    if d == 0:
      return self.evaluationFunction(gameState)
    
    # Maximizing player
    if player == 0:
      value = decimal.Decimal('-Infinity')
      for action in legalMoves:
        value = max(value, self.V(gameState.generateSuccessor(player, action), player+1, d, alpha, beta))
        alpha = max(alpha, value)
        if beta <= alpha: break
      return value
      
    # 1 ~ n-1 minimizing players
    elif player < (gameState.getNumAgents() - 1):
      value = decimal.Decimal('Infinity')
      for action in legalMoves:
        value = min(value, self.V(gameState.generateSuccessor(player, action), player+1, d, alpha, beta))
        beta = min(beta, value)
        if beta <= alpha: break
      return value
    
    # Last(n-th) minimizing player
    else:
      value = decimal.Decimal('Infinity')
      for action in legalMoves:
        value = min(value, self.V(gameState.generateSuccessor(player, action), 0, d-1, alpha, beta))
        beta = min(beta, value)
        if beta <= alpha: break
      return value

  def getAction(self, gameState):
    player = self.index
    
    legalMoves = gameState.getLegalActions(player)
    random.shuffle(legalMoves)
    
    alpha = -decimal.Decimal('Infinity')
    beta = decimal.Decimal('Infinity')
    
    # Maximizing player
    if player == 0:
        values = []
        for action in legalMoves:
          value = self.V(gameState.generateSuccessor(player, action), player+1, self.depth, alpha, beta)
          values.append(value)
          alpha = max(alpha, value)
        return max(list(zip(legalMoves, values)), key=lambda x: x[1])[0]
        
    # Minimizing player  
    else:
        raise Exception('Unnecessary part')        

######################################################################################
# Problem: implementing expectimax

class ExpectimaxAgent(MultiAgentSearchAgent):
  """
    Your expectimax agent
  """
  
  def V(self, gameState, player, d):
    # Set legal moves
    legalMoves = gameState.getLegalActions(player)
      
    is_end = gameState.isWin() or gameState.isLose() or len(legalMoves) == 0
    
    # If IsEnd(s)
    if is_end:
      return gameState.getScore()
    
    # If depth = 0
    if d == 0:
      return self.evaluationFunction(gameState)
    
    # Maximizing player
    if player == 0:
      value = decimal.Decimal('-Infinity')
      for action in legalMoves:
        value = max(value, self.V(gameState.generateSuccessor(player, action), player+1, d))
      return value
      
    # 1 ~ n-1 minimizing players
    elif player < (gameState.getNumAgents() - 1):
      value = 0
      for action in legalMoves:
        value += (self.V(gameState.generateSuccessor(player, action), player+1, d) / float(len(legalMoves)))
      return value
    
    # Last(n-th) minimizing player
    else:
      value = 0
      for action in legalMoves:
        value += (self.V(gameState.generateSuccessor(player, action), 0, d-1) / float(len(legalMoves)))
      return value

  def getAction(self, gameState):
    player = self.index
    
    legalMoves = gameState.getLegalActions(player)
    random.shuffle(legalMoves)
    
    # Maximizing player
    if player == 0:
        return max(legalMoves, key=lambda x: self.V(
          gameState.generateSuccessor(player, x), player + 1, self.depth))
    # Minimizing player  
    else:
        raise Exception('Unnecessary part')


######################################################################################
# Problem: creating a better evaluation function

# def betterEvaluationFunction(currentGameState):
#   """
#     Your extreme, unstoppable evaluation function (problem 4).

#     DESCRIPTION: <write something here so we know what you did>
#   """
#   evaluationFunction = util.lookup('scoreEvaluationFunction', globals())
#   return evaluationFunction(currentGameState)


def betterEvaluationFunction(currentGameState):
  """
    Your extreme, unstoppable evaluation function (problem 4).

    DESCRIPTION: <write something here so we know what you did>

  *** defined sub-functions ***
  @ search_item: it uses breadth first search (BFS) to find an item, by which has_item(x, y) == True, and the path length (=depth) from the start position (=start_pos: its default value is the Pac-Man's position).

  *** defined features ***
  @ game_state.getScore(): default evaluation score.
  @ depth_food: the path length to the closest food from Pac-Man.
  @ depth_capsule: the path length to the closest capsule from Pac-Man.
  @ depth_normal_ghost: the path length to the closest normal ghost from Pac-Man.
  @ depth_second_normal_ghost: the path length to the second closest normal ghost from Pac-Man.
  @ depth_normal_ghost_from_capsule: the path length to the closest normal ghost from the closest capsule.
  @ depth_scared_ghost: the path length to the closest scared ghost from Pac-Man.
  """

  # BEGIN_YOUR_CODE
  from collections import deque
  import sys
  # from math copysign
  import math

  game_state = currentGameState

  def search_item(has_item, start_pos=game_state.getPacmanPosition()):
    if start_pos[0] is None:  # or start_pos[1] is None
      return (None, None), None
    q = deque([(start_pos, 0)])  # queue contains pairs of positions & depths
    wall_grid = game_state.getWalls()
    visited = [[False] * wall_grid.height for _ in range(wall_grid.width)]
    visited[start_pos[0]][start_pos[1]] = True
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while q:
      (x, y), depth = q.popleft()
      if has_item(x, y):
        return (x, y), depth
      else:
        random.shuffle(moves)
        for x_move, y_move in moves:
          new_x, new_y = x + x_move, y + y_move
          if wall_grid[new_x][new_y] or visited[new_x][new_y]:
            continue
          else:
            visited[new_x][new_y] = True
            q.append(((new_x, new_y), depth + 1))
    else:
      return (None, None), None

  normal_ghost_set = {ghost_state.getPosition() for ghost_state in game_state.getGhostStates()
                      if ghost_state.scaredTimer == 0}

  scared_ghost_set = set()
  for ghost_state in game_state.getGhostStates():
    if ghost_state.scaredTimer > 0:
      ghost_x, ghost_y = ghost_state.getPosition()
      scared_ghost_set.update([(ghost_x, ghost_y),
                               (math.floor(ghost_x), ghost_y), (math.ceil(ghost_x), ghost_y),
                               (ghost_x, math.floor(ghost_y)), (ghost_x, math.ceil(ghost_y))])

  pos_food, depth_food = search_item(game_state.hasFood)
  pos_capsule, depth_capsule = search_item(lambda x, y: (x, y) in game_state.getCapsules())
  pos_normal_ghost, depth_normal_ghost = search_item(lambda x, y: (x, y) in normal_ghost_set)
  pos_second_normal_ghost, depth_second_normal_ghost = search_item(
    lambda x, y: (x, y) in normal_ghost_set and (x, y) != pos_normal_ghost)
  pos_normal_ghost_from_capsule, depth_normal_ghost_from_capsule = search_item(
    lambda x, y: (x, y) in normal_ghost_set, start_pos=pos_capsule)
  pos_scared_ghost, depth_scared_ghost = search_item(lambda x, y: (x, y) in scared_ghost_set)

  for ghost_state in game_state.getGhostStates():
    ghost_x, ghost_y = ghost_state.getPosition()
    if pos_scared_ghost in {(ghost_x, ghost_y),
                            (math.floor(ghost_x), ghost_y), (math.ceil(ghost_x), ghost_y),
                            (ghost_x, math.floor(ghost_y)), (ghost_x, math.ceil(ghost_y))}:
      scared_ghost_state = ghost_state
      break
  else:
    scared_ghost_state = None

  score = game_state.getScore()
  score += - 0.3 * depth_food if depth_food else 0
  score += 0.2 * max(depth_normal_ghost, 8)
  score += 2 * math.log(max(depth_second_normal_ghost + 1, 8)) if depth_second_normal_ghost else 0
  score += 5 * (depth_normal_ghost_from_capsule - depth_capsule) if depth_normal_ghost_from_capsule is not None else 0
  score += 5 * max(scared_ghost_state.scaredTimer - 1.5 * depth_scared_ghost + 5, 0) if scared_ghost_state else 0

  return score


# Abbreviation
better = betterEvaluationFunction
