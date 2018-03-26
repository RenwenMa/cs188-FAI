# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util
from game import Actions
from game import Agent

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
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        score = successorGameState.getScore()
        "*** YOUR CODE HERE ***"
        if successorGameState.isLose():
          return -float("inf")
        if successorGameState.isWin():
          return float("inf")
        newFood = newFood.asList()
        closestDoc = newPos
        if newFood:
          manhattanDistanceToClosestFood,closestDoc = minManhattanDistanceDoc(newPos, newFood)
        else:
          manhattanDistanceToClosestFood = float("inf")

        numFood = successorGameState.getNumFood()
        distanceToScaredGhost = 0
        distanceToNonScaredGhost = 0
        ghostToFood = 0
        for ghostState in successorGameState.getGhostStates():
            ghostPos = ghostState.getPosition()
            if ghostState.scaredTimer == 0:
              # when ghost is scared calculate minimun distance
              #  from ghost to food and from pacman to ghost
                if distanceToNonScaredGhost == 0:
                  ghostToFood = manhattanDistance(ghostPos,closestDoc)
                  distanceToNonScaredGhost = manhattanDistance(ghostPos, newPos)
                else:
                  distanceToNonScaredGhost = min(distanceToNonScaredGhost, \
                    manhattanDistance(ghostPos, newPos))
                  ghostToFood = min(manhattanDistance(ghostPos,closestDoc),ghostToFood)

            else:
              # when ghost is not scared calculate minimun distance
              #  from ghost to food and from pacman to ghost
                if distanceToScaredGhost == 0:
                  distanceToScaredGhost = manhattanDistance(ghostPos,newPos)
                else:
                  distanceToScaredGhost = min(distanceToScaredGhost, \
                    manhattanDistance(ghostPos, newPos))
        if manhattanDistanceToClosestFood < distanceToNonScaredGhost - 5:
          distanceToNonScaredGhost += 10 # if ghost is far to food and pacman, penalize it.
        elif distanceToNonScaredGhost < 2:
          distanceToNonScaredGhost -= 2

        if ghostToFood > manhattanDistanceToClosestFood + 5:
          if manhattanDistanceToClosestFood > ghostToFood - manhattanDistanceToClosestFood:
            manhattanDistanceToClosestFood = ghostToFood - manhattanDistanceToClosestFood
        return score + -2 * manhattanDistanceToClosestFood + \
         2 * distanceToNonScaredGhost + -2 * distanceToScaredGhost + \
          -9 * numFood + 2 * ghostToFood

def minManhattanDistanceDoc(start, docList):
    distance = float("inf")
    closestDoc = start
    for doc in docList:
        if distance > manhattanDistance(start,doc):
          distance = manhattanDistance(start,doc)
          closestDoc = doc
    return distance,closestDoc

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
    def terminalTest(self, gameState):
      if gameState.isLose() or gameState.isWin():
        return True
      else: return False

    def minValue(self, gameState, i ,depth):
      if self.terminalTest(gameState):
        return self.evaluationFunction(gameState)
      actions = gameState.getLegalActions(i)
      value = float('inf')
      if i == gameState.getNumAgents() - 1: # last min node of this depth
        for action in actions:
          nextState = gameState.generateSuccessor(i,action)
          value = min(self.maxValue(nextState, depth  - 1),value)
      else: # min node move
        for action in actions:
          nextState = gameState.generateSuccessor(i,action)
          value = min(self.minValue(nextState, i + 1, depth),value)
      return value

    def maxValue(self, gameState,depth):
      if self.terminalTest(gameState) or depth == 0:
        return self.evaluationFunction(gameState)
      actions = gameState.getLegalActions(0)
      value = -float('inf')
      for action in actions:
        nextState = gameState.generateSuccessor(0,action)
        value = max(self.minValue(nextState, 1, depth),value)
      return value
       
    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game

          gameState.isWin():
            Returns whether or not the game state is a winning state

          gameState.isLose():
            Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        actionsOfMax = gameState.getLegalActions()
        bestAction = ""
        value = -float('inf')

        for action in actionsOfMax:
          nextState = gameState.generateSuccessor(0,action)
          evaluation = self.minValue(nextState,1,self.depth)
          if evaluation > value:
            value = evaluation
            bestAction = action
        return bestAction

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """
    
    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def minValue(gameState, i ,depth,a, b):
          if gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState)
          actions = gameState.getLegalActions(i)
          value = float('inf')
          if i == gameState.getNumAgents() - 1: # last min node of this depth
            for action in actions:
              nextState = gameState.generateSuccessor(i,action)
              value = min(maxValue(nextState, depth  - 1,a,b),value)
              if value < a:
                return value
              else:
                b = min(b,value)
          else: # min node move
            for action in actions:
              nextState = gameState.generateSuccessor(i,action)
              value = min(minValue(nextState, i + 1, depth,a,b),value)
              if value < a:
                return value
              else:
                b = min(b,value)
          return value

        def maxValue( gameState,depth, a, b):
          if gameState.isLose() or gameState.isWin() or depth == 0:
            return self.evaluationFunction(gameState)
          actions = gameState.getLegalActions(0)
          value = -float('inf')
          for action in actions:
            nextState = gameState.generateSuccessor(0,action)
            value = max(minValue(nextState, 1, depth,a,b),value)
            if value > b:
              return value
            else:
              a = max(a,value)
          return value

        actionsOfMax = gameState.getLegalActions()
        bestAction = ""
        value = -float('inf')
        a = -float('inf')
        b = float('inf')
        for action in actionsOfMax:
          nextState = gameState.generateSuccessor(0,action)
          evaluation = minValue(nextState,1,self.depth,a,b)
          if evaluation > b:
              return evaluation
          else:
              a = max(a,evaluation)
          if evaluation > value:
            value = evaluation
            bestAction = action
        return bestAction
        util.raiseNotDefined()
       

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
        "*** YOUR CODE HERE ***"
        def expValue(gameState, i ,depth):
          if gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState)
          actions = gameState.getLegalActions(i)
          prob = 1./float(len(actions))
          value = 0.0
          if i == gameState.getNumAgents() - 1: # last min node of this depth
            for action in actions:
              nextState = gameState.generateSuccessor(i,action)
              value += maxValue(nextState, depth  - 1) * prob
          else: # min node move
            for action in actions:
              nextState = gameState.generateSuccessor(i,action)
              value += expValue(nextState, i + 1, depth) * prob
          return value

        def maxValue( gameState,depth):
          if gameState.isLose() or gameState.isWin() or depth == 0:
            return self.evaluationFunction(gameState)
          actions = gameState.getLegalActions(0)
          value = -float('inf')
          for action in actions:
            nextState = gameState.generateSuccessor(0,action)
            value = max(expValue(nextState, 1, depth),value)
          return value

        actionsOfMax = gameState.getLegalActions()
        bestAction = ""
        value = -float('inf')
        for action in actionsOfMax:
          nextState = gameState.generateSuccessor(0,action)
          evaluation = expValue(nextState,1,self.depth)
          if evaluation > value:
            value = evaluation
            bestAction = action
        return bestAction
        

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).
      DESCRIPTION: 
      Return infinite if win or -infinit if lose.Otherwise calculate minimun distances 
      from pacman to food, and from ghost to food, from pacman to ghost, from pacman to capsules and 
      from ghost of capsules.
      If pacmanToGhost is larger than pacmanToFood or ghostToFood is larger than pacmanToFood a lot,
      just consider distance to food. If ghost is far from pacman, ignore ghost.
      Finally, calculate these features by combination.
    """
    "*** YOUR CODE HERE ***"
    if currentGameState.isWin():
      return float("inf")
    if currentGameState.isLose():
      return - float("inf")
    score = scoreEvaluationFunction(currentGameState)
    pacmanPos = currentGameState.getPacmanPosition()
    foods = currentGameState.getFood()
    foods = foods.asList()
    closestDoc = pacmanPos
    if foods:
      manhattanDistanceToClosestFood,closestDoc = minManhattanDistanceDoc(pacmanPos, foods)
    else:
      manhattanDistanceToClosestFood = float("inf")
    numFood = currentGameState.getNumFood()
    capsules = currentGameState.getCapsules()
    numCapsules = len(capsules)
    ghostToCapsules = 0
    if numCapsules != 0:
      distanceToCapsules,capsules = minManhattanDistanceDoc(pacmanPos, capsules)
    else:
      distanceToCapsules = 0
    distanceToScaredGhost = 0
    distanceToNonScaredGhost = 0
    ghostToFood = 0
    for ghostState in currentGameState.getGhostStates():
        ghostPos = ghostState.getPosition()
        if ghostState.scaredTimer == 0:
          if distanceToNonScaredGhost == 0:
            ghostToFood = manhattanDistance(ghostPos,closestDoc)
            distanceToNonScaredGhost = manhattanDistance(ghostPos, pacmanPos)
            if capsules:
              ghostToCapsules = manhattanDistance(ghostPos,capsules)
          else:
            distanceToNonScaredGhost = min(distanceToNonScaredGhost, \
              manhattanDistance(ghostPos, pacmanPos))
            ghostToFood = min(manhattanDistance(ghostPos,closestDoc),ghostToFood)
            if capsules:
              ghostToCapsules = min(manhattanDistance(ghostPos,capsules).ghostToCapsules)
        # ghost is scared, try best to eat it.
        else:
          return score - 10 * manhattanDistance(ghostPos, pacmanPos)
        # if ghost is too far, ingore it.
        if manhattanDistanceToClosestFood < distanceToNonScaredGhost - 5 or \
          manhattanDistanceToClosestFood <ghostToFood - 4:
          return score - 10 * manhattanDistanceToClosestFood -4 * numFood
        # if ghost is too close, let distance be negetive
        elif distanceToNonScaredGhost < 2:
          distanceToNonScaredGhost -= 2
          
        if ghostToFood > manhattanDistanceToClosestFood + 5:
          ghostToFood = 0
        if distanceToNonScaredGhost > 8:    
          distanceToNonScaredGhost = 0

        
        return score + -2 * manhattanDistanceToClosestFood + \
         2 * distanceToNonScaredGhost + -2 * distanceToScaredGhost + \
        -4 * numFood + 1.5 * ghostToFood  + \
        -2.5 * distanceToCapsules + ghostToCapsules * 2 

# Abbreviation
better = betterEvaluationFunction

