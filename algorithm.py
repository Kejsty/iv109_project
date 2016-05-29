import numpy as np
import matplotlib.pyplot as plt
import random
import Robot
import simple_init
import complicated_init
import  Playground

POPULATION_SIZE = 100
GENERATION_COUNT = 1000
CROSSOVER_PROB = 0.8
MUTATION_PROB = 0.2

def getStatistics( population ):
    fitnesses = [ Robot.getFitness1(robot) for robot in population ]
    return max(fitnesses), np.mean(fitnesses), min(fitnesses), np.std(fitnesses)


def initPopulation():
    list = []
    for i in range(POPULATION_SIZE):
        list.append( Robot.Robot() )
    return list

def selectParent( wheel ):
    randomFitness = random.random() * wheel[-1]
    for i in range(POPULATION_SIZE):
        if randomFitness <= wheel[i]:
            return i
    return 0


def createWheel( population ):
    cumulativeFitnesses = [0] * len(population)
    cumulativeFitnesses[0] = Robot.getFitness1(population[0])
    for i in range(1, len(population)):
        cumulativeFitnesses[i] = cumulativeFitnesses[i - 1] + Robot.getFitness1(population[i])
    return cumulativeFitnesses

def getNewPopulation(population):
    wheel = createWheel(population)
    newPopulation = []
    for j in range(POPULATION_SIZE):

        ''' Here you can change the behaviour fo algorithm '''
        parent1 = population[ selectParent( wheel ) ]

        ''' either continue with original solution '''
        if random.random() <= CROSSOVER_PROB:
            newPopulation.append( parent1 )
            continue

        parent2 = population[ selectParent( wheel ) ]

        ''' create a new one '''
        child = Robot.crossover( parent1, parent2 )

        ''' mutate new solution, or mutate original solution '''
        if random.random() <= MUTATION_PROB:
            Robot.mutate( child )

        newPopulation.append( child )

        ''''''
    return newPopulation

def geneticAlgorithm():
    # Statistics
    best = [0] * GENERATION_COUNT
    mean = [0] * GENERATION_COUNT
    worst = [0] * GENERATION_COUNT
    way = ""

    # Initilize
    population = initPopulation()

    # For each generation, select new population
    for i in range(GENERATION_COUNT):
        #for robot in population:
            # print(robot.strategy, Robot.getFitness1(robot))
        # prepare wheel

        population = getNewPopulation( population )
        best[i], mean[i], worst[i], dev  = getStatistics( population )

        #play = Playground.Playground(population[0], 50, (Robot.ROWS, Robot.COLUMNS), Robot.gameMap, INIT_POS)
        #play.run()
    return best, mean, worst

def geneticAlgorithmMultipleRun( runCount ):
    bestOfLastGen = []
    averageBest = [0] * GENERATION_COUNT
    for i in range( runCount ):
        best, mean, worst = geneticAlgorithm()
        for j in range(GENERATION_COUNT):
            averageBest[j] += best[j]
        bestOfLastGen.append( best[-1] )
    for i in range(GENERATION_COUNT):
        averageBest[i] /= 20
    return max(bestOfLastGen), np.mean(bestOfLastGen), min(bestOfLastGen), np.std(bestOfLastGen), averageBest

best, mean, worst = geneticAlgorithm()
Robot.printMap()


# convert strategy to be printable as picture
# strategy = ""
#
# for pos in strategy :
#     if (pos == 'U'):
#         strategy += 'L'
#     if (pos == 'D'):
#         strategy += 'R'
#     if (pos == 'R'):
#         strategy += 'D'
#     if (pos == 'L'):
#         strategy += 'U'
#
# Robot.doDraw(strategy)

x = np.linspace( 1, GENERATION_COUNT, GENERATION_COUNT )
# plt.ylim([0,10])

plt.plot( x, best, label='best' )
plt.plot( x, mean, label='mean' )
plt.plot( x, worst, label='worst' )

plt.legend(loc=4)
plt.show()


