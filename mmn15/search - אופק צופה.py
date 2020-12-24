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
from util import Stack;
from util import Queue;
from util import PriorityQueue;

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
  
  currentPos = problem.getStartState();
  """the Nodes in this function contain as value 
  a tuple of a position and the direction traveled from parent to get to this node"""
  currentNode = Node((currentPos,None),None);
  frontier = Stack();
  frontier.push(currentNode);
  explored = set();
  foundGoal = False;
  
  while not frontier.isEmpty() and not foundGoal:
    currentNode = frontier.pop();
    currentPos = currentNode.getValue()[0];
    if problem.isGoalState(currentPos):
      foundGoal = True;
    elif currentPos not in explored:
      explored.add(currentPos);
      successors = problem.getSuccessors(currentPos);
      for suc in successors:
        frontier.push(Node((suc[0],suc[1]),currentNode));
  
  if not foundGoal:
    return [];
  
  "if foundGoal == True then currentNode holds the goal node that has been found"
  
  result = [];
  
  "creates the result by going back the path of parents from the goal node"
  if foundGoal:
    while currentNode.getParent() != None:
      result.insert(0,currentNode.getValue()[1]);
      currentNode = currentNode.getParent();
  
  return result;

def breadthFirstSearch(problem):
  "Search the shallowest nodes in the search tree first. [p 74]"
  
  currentPos = problem.getStartState();
  """the Nodes in this function contain as value 
  a tuple of a position and the direction traveled from parent to get to this node"""
  currentNode = Node((currentPos,None),None);
  frontier = Queue();
  frontier.push(currentNode);
  explored = set();
  foundGoal = False;
  
  while not frontier.isEmpty() and not foundGoal:
    currentNode = frontier.pop();
    currentPos = currentNode.getValue()[0];
    if problem.isGoalState(currentPos):
      foundGoal = True;
    elif currentPos not in explored:
      explored.add(currentPos);
      successors = problem.getSuccessors(currentPos);
      for suc in successors:
        frontier.push(Node((suc[0],suc[1]),currentNode));
        
  if not foundGoal:
    return [];
  
  "if foundGoal == True then currentNode holds the goal node that has been found"
  
  result = [];
  
  "creates the result by going back the path of parents from the goal node"
  if foundGoal:
    while currentNode.getParent() != None:
      result.insert(0,currentNode.getValue()[1]);
      currentNode = currentNode.getParent();
  
  return result;
      
def uniformCostSearch(problem):
  "Search the node of least total cost first. "
  
  currentPos = problem.getStartState();
  """the Nodes in this function contain as value 
  a triple of a position, the direction traveled from parent to get to this node
  and the cost of traveling to this node from the start node"""
  currentNode = Node((currentPos,None,0),None);
  frontier = PriorityQueue();
  frontier.push(currentNode,0);
  explored = set();
  foundGoal = False;
  
  while not frontier.isEmpty() and not foundGoal:
    currentNode = frontier.pop();
    currentPos = currentNode.getValue()[0];
    currentCost = currentNode.getValue()[2];
    if problem.isGoalState(currentPos):
      foundGoal = True;
    elif currentPos not in explored:
      explored.add(currentPos);
      successors = problem.getSuccessors(currentPos);
      for suc in successors:
        frontier.push(Node((suc[0],suc[1],currentCost+suc[2]),currentNode), currentCost+suc[2]);
        
  if not foundGoal:
    return [];
  
  "if foundGoal == True then currentNode holds the goal node that has been found"

  result = [];
  
  "creates the result by going back the path of parents from the goal node"
  if foundGoal:
    while currentNode.getParent() != None:
      result.insert(0,currentNode.getValue()[1]);
      currentNode = currentNode.getParent();
  
  return result;

def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0

def aStarSearch(problem, heuristic=nullHeuristic):
  "Search the node that has the lowest combined cost and heuristic first."
  
  currentPos = problem.getStartState();
  """the Nodes in this function contain as value 
  a triple of a position, the direction traveled from parent to get to this node
  and the cost of traveling to this node from the start node"""
  currentNode = Node((currentPos,None,0),None);
  frontier = PriorityQueue();
  frontier.push(currentNode,heuristic(currentPos,problem));
  explored = list();
  foundGoal = False;
  
  while not frontier.isEmpty() and not foundGoal:
    currentNode = frontier.pop();
    currentPos = currentNode.getValue()[0];
    currentCost = currentNode.getValue()[2];
    if problem.isGoalState(currentPos):
      foundGoal = True;
    elif currentPos not in explored:
      explored.append(currentPos);
      successors = problem.getSuccessors(currentPos);
      for suc in successors:
        frontier.push(Node((suc[0],suc[1],currentCost+suc[2]),currentNode),
                      currentCost+suc[2]+heuristic(suc[0],problem));
        
  if not foundGoal:
    return [];
  
  "if foundGoal == True then currentNode holds the goal node that has been found"

  result = [];
  
  "creates the result by going back the path of parents from the goal node"
  if foundGoal:
    while currentNode.getParent() != None:
      result.insert(0,currentNode.getValue()[1]);
      currentNode = currentNode.getParent();
  
  return result;
    
  
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch

class Node:
  "A container with a value and a parent (the Node which led to this Node's discovery)"
  def __init__(self, val, p):
    self.value = val;
    self.parent = p;
    
  def getValue(self):
    "returns the node's value"
    return self.value;

  def getParent(self):
    "returns the node's parent"
    return self.parent;


