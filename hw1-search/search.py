# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
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
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

import time
def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    start = (problem.getStartState(),"Stop",1) # data structure of node(pos, action, cost)
    explored = set() # a list of nodes explored
    frontier = util.Stack()
    frontier.push(start)
    path = {} # a map of nodes and its parent <node,parent>
    while frontier:
        node = frontier.pop()
        if problem.isGoalState(node[0]):
            return backtrace(path, start, node) # backtrace from goal to start
        else:  
            explored.add(node[0])
        for child in problem.getSuccessors(node[0]):
            if child[0] not in explored:
                path[child] = node
                frontier.push(child)


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    start = (problem.getStartState(),"Stop",1)
    explored = set()
    frontier = util.Queue()
    recordFrontier = set()
    frontier.push(start)
    recordFrontier.add(start[0]) # list of position of nodes pushed into frontier
    path = {}
    while frontier:
        node = frontier.pop()
        explored.add(node[0])
        if problem.isGoalState(node[0]):
            return backtrace(path, start, node)
        for child in problem.getSuccessors(node[0]):
            if child[0] not in explored and child[0] not in recordFrontier:
                path[child] = node
                frontier.push(child)
                recordFrontier.add(child[0])        

# backtrace actions
def backtrace(parent, start, end):
    path = [end]
    while parent[path[-1]] != start:
        path.append(parent[path[-1]])
    path.reverse()
    actions = []
    for node in path:
        actions.append(node[1])
    return actions

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    start = problem.getStartState()
    explored = set()
    frontier = util.PriorityQueue()
    costRecord = {}
    frontier.update(start,0)
    costRecord[start] = 0
    path = {} # a map of nodes and its parent <node,parent>
    actions = {} # map node and its action <pos, action>
    actions[start] = 'Stop' 
    while frontier:
        node = frontier.pop()
        cost = costRecord[node] # current cost to node
        if problem.isGoalState(node):
            return backtrace1(path, start, node, actions)
        else: 
            explored.add(node)
        for child in problem.getSuccessors(node):
            nextState = child[0]
            nextCost = child[2]
            nextAction = child[1]
            if nextState not in explored:
                frontier.update(nextState, nextCost + cost)
                if (nextState in costRecord and nextCost + cost < costRecord[nextState]) \
                or nextState not in costRecord: # update cost,action,and path 
                    costRecord[nextState] = nextCost + cost
                    actions[nextState] = nextAction
                    path[nextState] = node
# backtrace for UCS , A       
def backtrace1(parent, start, end, actions):
    path = [actions[end]]
    while end != start:
        path.append(actions[parent[end]])
        end = parent[end]
    path.reverse()
    del path[0]
    return path

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    start = problem.getStartState()
    explored = set()
    frontier = util.PriorityQueue()
    costRecord = {}
    g = 0
    h = heuristic(start, problem) 
    f = g + h
    frontier.update(start, f)
    costRecord[start] = 0
    path = {}
    actions = {}
    actions[start] = 'Stop'
    while frontier:
        node = frontier.pop()
        cost = costRecord[node]
        if problem.isGoalState(node):
            return backtrace1(path, start, node, actions)
        else: 
            explored.add(node)
        for child in problem.getSuccessors(node):
            nextState = child[0]
            nextCost = child[2]
            nextAction = child[1]
            if nextState not in explored:
                nextCost = cost + nextCost
                h = heuristic(nextState, problem)
                priority = nextCost + h
                frontier.update(nextState, priority)
                if (nextState in costRecord and priority < costRecord[nextState] + h) \
                    or nextState not in costRecord:
                        costRecord[nextState] = nextCost
                        actions[nextState] = nextAction
                        path[nextState] = node


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
