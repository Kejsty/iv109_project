import numpy as np
import matplotlib.pyplot as plt
import random
import Robot
import  Playground

POPULATION_SIZE = 100
GENERATION_COUNT = 1000
CROSSOVER_PROB = 0.8
MUTATION_PROB = 0.2

def getStatistics( population ):
    fitnesses = [ Robot.getFitness1(robot) for robot in population ]
    return max(fitnesses), np.mean(fitnesses), min(fitnesses), np.std(fitnesses)

def findBest( population ):
    best = None
    for robot in population:
        if best is None:
            best = robot
        if robot.fitness > best.fitness:
            best = robot
    return best

def initPopulation( init ):
    list = []
    for i in range(POPULATION_SIZE):
        list.append( Robot.Robot() )
        list[i].strategy = init[i]
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

        ''' You can change the behaviour of the algorithm here'''
        parent1 = population[ selectParent( wheel ) ]

        ''' either continue with original solution '''
        if random.random() <= CROSSOVER_PROB:
            newPopulation.append( parent1 )
            continue

        parent2 = population[ selectParent( wheel ) ]

        ''' create a new one '''
        child = Robot.crossover( parent1, parent2 )

        ''' mutate new solution, or mutate original solution '''
        Robot.mutate( child, MUTATION_PROB )

        newPopulation.append( child )

        ''''''
    return newPopulation

def geneticAlgorithm():
    # Statistics
    bestList = [0] * GENERATION_COUNT
    meanList = [0] * GENERATION_COUNT
    worstList = [0] * GENERATION_COUNT
    way = ""

    # Initilize
    population = initPopulation( COMPLICATED_INIT )

    # For each generation, select new population
    for i in range(GENERATION_COUNT):
        population = getNewPopulation( population )
        bestList[i], meanList[i], worstList[i], dev = getStatistics( population )

        #play = Playground.Playground( population[i].strategy )
        #play.run()
        #break
    '''
    bestOfLast = findBest( population )
    print str( bestOfLast.fitness ) + ", " + str( bestOfLast.foundTreasures )
    print bestOfLast.strategy
    Robot.doDraw( bestOfLast.strategy )'''
    best, mean, worst, dev = getStatistics( population )
    return best, mean, worst
    # return bestList, meanList, worstList

'''
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
'''

def geneticAlgorithmMultipleRun( runCount ):
    bestOfLast = [ 0 ] * runCount
    meanOfLast = [ 0 ] * runCount
    worstOfLast = [ 0 ] * runCount
    for i in range( runCount ):
        bestOfLast[i], meanOfLast[i], worstOfLast[i] = geneticAlgorithm()
    return np.mean( bestOfLast ), np.mean( meanOfLast ), np.mean( worstOfLast )

# best, mean, worst = geneticAlgorithm()
'''
optimal = Robot.Robot()
optimal.strategy = Robot.simpleOptimal

print Robot.getFitness1( optimal )
print optimal.foundTreasures

print optimal.fitness

Robot.doDraw( Robot.simpleOptimal )

'''
print "Simple map with static initial population\n"

print Robot.values
#print "MAX_BOUND = 60\nMIN_BOUND = 20"

print "POPULATION_SIZE = " + str( POPULATION_SIZE ) + "\nGENERATION_COUNT = " + str( GENERATION_COUNT ) + "\nWe tried different probabilities:\n"

for CROSSOVER_PROB in [ 0.8, 0.7, 0.6 ]:
    for MUTATION_PROB in [ 0.2, 0.3, 0.4 ]:
        best, mean, worst = geneticAlgorithmMultipleRun( 10 )
        print "\tcrossover = " + str( CROSSOVER_PROB ) + ", mutation = " + str( MUTATION_PROB ) + ": \n"
        print "\t\tbest = " + str( best ) + ", mean = " + str( mean ) + ", worst = " + str( worst ) + "\n"

'''
plt.figure(figsize=(10,5))
x = np.linspace( 1, GENERATION_COUNT, GENERATION_COUNT )
plt.xlim([0,GENERATION_COUNT])
#plt.ylim([0,10])



plt.plot( x, best, label='best' )
plt.plot( x, mean, label='mean' )
plt.plot( x, worst, label='worst' )

plt.legend(loc=4)
plt.show()

'''
