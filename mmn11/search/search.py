# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called 
by Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
  """
  This class outlines the structure of a search problem, but doesn't implement
  any of the methods (in object-oriented terminology: an abstract class).
  
  You do not need to change anything in this class, ever.
  """
  
  def getStartState(self):
     """
     Returns the start state for the search problem 
     """
     util.raiseNotDefined()
    
  def isGoalState(self, state):
     """
       state: Search state
    
     Returns True if and only if the state is a valid goal state
     """
     util.raiseNotDefined()

  def getSuccessors(self, state):
     """
       state: Search state
     
     For a given state, this should return a list of triples, 
     (successor, action, stepCost), where 'successor' is a 
     successor to the current state, 'action' is the action
     required to get there, and 'stepCost' is the incremental 
     cost of expanding to that successor
     """
     util.raiseNotDefined()

  def getCostOfActions(self, actions):
     """
      actions: A list of actions to take
 
     This method returns the total cost of a particular sequence of actions.  The sequence must
     be composed of legal moves
     """
     util.raiseNotDefined()
           

def tinyMazeSearch(problem):
  """
  Returns a sequence of moves that solves tinyMaze.  For any other
  maze, the sequence of moves will be incorrect, so only use this for tinyMaze
  """
  from game import Directions
  s = Directions.SOUTH
  w = Directions.WEST
  return  [s,s,w,s,w,w,s,w]

def genericSearch(problem, frontier):
    """
    Implements a generic tree search using a given frontier.
    When frontier is Stack: It performs DFS.
    When frontier is Queue: It performs BFS.
    When frontier is PriorityQueueWithFunction: It performs the search according to the cost function.
    """
    calculated_states = []
    current_state = problem.getStartState()
    frontier.push((current_state, [], 0))

    while not frontier.isEmpty():
        current_state, moves, cost = frontier.pop()

        if current_state in calculated_states:
            continue
        calculated_states.append(current_state)

        if problem.isGoalState(current_state):
            return moves

        for successor, move, successor_cost in problem.getSuccessors(current_state):
            successor_moves = moves[:]
            successor_moves.append(move)
            if successor in calculated_states:
                continue
            frontier.push((successor, successor_moves, cost + successor_cost))

    return []


def depthFirstSearch(problem):
  """
  Search the deepest nodes in the search tree first [p 74].
  
  Your search algorithm needs to return a list of actions that reaches
  the goal.  Make sure to implement a graph search algorithm [Fig. 3.18].
  
  To get started, you might want to try some of these simple commands to
  understand the search problem that is being passed in:
  
  print "Start:", problem.getStartState()
  print "Is the start a goal?", problem.isGoalState(problem.getStartState())
  print "Start's successors:", problem.getSuccessors(problem.getStartState())
  """
  frontier = util.Stack()
  return genericSearch(problem, frontier)


def breadthFirstSearch(problem):
  "Search the shallowest nodes in the search tree first. [p 74]"
  frontier = util.Queue()
  return genericSearch(problem, frontier)
      
def uniformCostSearch(problem):
  "Search the node of least total cost first. "
  myCostFunction = lambda state: state[2] # state[2] = cost of path
  frontier = util.PriorityQueueWithFunction(myCostFunction)
  return genericSearch(problem, frontier)

def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0

def aStarSearch(problem, heuristic=nullHeuristic):
  "Search the node that has the lowest combined cost and heuristic first."
  myHeuristicFunction = lambda state: heuristic(state[0], problem) + state[2] # H(state) + Cost(state)
  frontier = util.PriorityQueueWithFunction(myHeuristicFunction)
  return genericSearch(problem, frontier)
    
  
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch