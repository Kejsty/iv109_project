import copy
import random
import Playground

MAX_BOUND = 60
MIN_BOUND = 40

ROWS = 10
COLUMNS = 10

INIT_POS = (3,5)

directions = { 'L': (-1, 0),    # left
               'R': (1, 0),     # right
               'D': (0, 1),     # down
               'U': (0, -1) }   # up

values = { '.': 0,      # empty
           '#': -10,    # border
           '*': 100 }   # treasure

class Robot:
    def __init__(self):
        self.init_pos = INIT_POS
        self.pos = INIT_POS
        self.strategy = getRandomStrategy()

    def updatePos(self, dir):
        self.pos[0], self.pos[1] = self.pos[0] + directions[dir][0], self.pos[1] + directions[dir][1]


''' Creates new random strategy, that is string of L, R, U, D symbols with bounded length '''
def getRandomStrategy():
    possibleWays = ['L', 'R', 'D', 'U']
    size = random.randint(MIN_BOUND, MAX_BOUND)
    strategy = []
    for j in range(size):
        strategy.append(random.choice(possibleWays))
    return strategy

def printMap():
    for row in gameMap:
        rowString = ''
        for symbol in row:
            rowString += symbol
        print(row)

''' Returns randomly generated map with given bounds '''
def getRandomMap():
    # Create empty map
    gameMap = [ [ '.' for y in range(COLUMNS)] for x in range(ROWS) ]
    # Build borders around map
    for y in range(COLUMNS):
        gameMap[0][y] = '#'
        gameMap[ROWS - 1][y] = '#'
    for x in range(ROWS):
        gameMap[x][0] = '#'
        gameMap[x][COLUMNS - 1] = '#'

    # Add treasures
    treasure_count = 10
    for i in range(treasure_count):
        x = random.randrange(ROWS)
        y = random.randrange(COLUMNS)
        # Find empty position
        while gameMap[x][y] != '.':
            x = random.randrange(ROWS)
            y = random.randrange(COLUMNS)
        gameMap[x][y] = '*'

    return gameMap

''' Updates position '''
def move(position, dir):
    deltax, deltay = directions[dir]
    return (position[0] + deltax, position[1] + deltay)

''' Count fitness function for a strategy on given map and initial position '''
def objectiveFitness( robot ):
    gameMapCopy = copy.deepcopy(gameMap)
    position = robot.init_pos
    valuation = 0
    for direction in robot.strategy :
        newPosition = move(position, direction)
        x, y = newPosition
        if gameMapCopy[x][y] != '#': # updates position only if new position empty
            return valuation
        if gameMapCopy[x][y] == '*': # collects treasure, position is now empty
            gameMapCopy[x][y] = '.'
            valuation += 1
    return valuation

def getFitness1(robot):
    gameMapCopy = copy.deepcopy(gameMap)
    position = robot.init_pos
    valuation = 0
    for direction in robot.strategy :
        newPosition = move(position, direction)
        x, y = newPosition
        valuation += values[ gameMapCopy[x][y] ]
        if gameMapCopy[x][y] != '#': # updates position only if new position empty
            position = newPosition
        if gameMapCopy[x][y] == '*': # collects treasure, position is now empty
            gameMapCopy[x][y] = '.'

    return valuation

''' Crossover & Mutate functions '''

def crossover( robot_A, robot_B ):
    robot_C = Robot()
    crossing_point = random.randrange( min(len(robot_A.strategy), len(robot_B.strategy)) )
    robot_C.strategy =   robot_A.strategy[:crossing_point] \
                       + robot_B.strategy[crossing_point:]
    return robot_C

def mutate( robot, prob ):
    possibleWays = ['L', 'R', 'D', 'U']
    for i in range( len(robot.strategy) ):
        if random.random() < prob:
            robot.strategy[i] = random.choice(possibleWays)

random.seed()
simpleMap =[
['#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
['#', '.', '.', '.', '.', '.', '.', '#', '.', '#'],
['#', '.', '.', '*', '#', '.', '.', '.', '.', '#'],
['#', '*', '#', '.', '#', '.', '*', '.', '*', '#'],
['#', '.', '#', '.', '.', '*', '#', '#', '.', '#'],
['#', '*', '#', '.', '*', '.', '.', '.', '.', '#'],
['#', '.', '.', '.', '.', '.', '.', '.', '.', '#'],
['#', '.', '#', '.', '.', '.', '#', '#', '.', '#'],
['#', '.', '.', '*', '.', '*', '#', '*', '.', '#'],
['#', '#', '#', '#', '#', '#', '#', '#', '#', '#']
]

complicatedMap =[
['#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
['#', '.', '#', '*', '*', '.', '.', '.', '.', '#'],
['#', '.', '#', '#', '#', '#', '#', '#', '.', '#'],
['#', '*', '#', '.', '#', '.', '*', '#', '*', '#'],
['#', '.', '#', '.', '#', '*', '#', '#', '.', '#'],
['#', '.', '#', '.', '*', '.', '.', '.', '.', '#'],
['#', '.', '.', '.', '.', '.', '.', '#', '.', '#'],
['#', '#', '#', '#', '.', '.', '#', '#', '.', '#'],
['#', '*', '.', '*', '.', '*', '#', '*', '.', '#'],
['#', '#', '#', '#', '#', '#', '#', '#', '#', '#']
]

gameMap = complicatedMap


def doDraw(way):
    play = Playground.Playground(way)
    play.run()
