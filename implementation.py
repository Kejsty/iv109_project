import random
import sys
import  Playground
MAX_BOUND = 60
MIN_BOUND = 20
treasure = [[1,4], [5,7], [8,6]]

def move(position, direction):
    if direction == 'L':
        return  [position[0] - 1, position[1]]
    elif direction == 'R':
        return   [position[0] + 1, position[1]]
    elif direction == 'D':
        return [position[0], position[1] + 1]
    else:
        return [position[0], position[1] - 1]


def fit_function1 (initPosition, result, treasures, gamesize) :
    "treasure gets 100, trash walls gets -10, if trash walls, stay on pozice"""
    position = initPosition
    valuation = 0
    for direction in result :
        position = move(position,direction)
        for treasure in treasures :
            if position[0] < 0:
                valuation -= 10
                position[0] = 0
            elif position[0] >= gamesize[0]:
                valuation -= 10
                position[0] = gamesize[0] - 1
            elif position[1] < 0:
                valuation-= 10
                position[1] = 0
            elif position[1] >= gamesize[1] :
                valuation -= 10
                position[1] = gamesize[1] - 1
            elif position[1] == treasure[1] and position[0] == treasure[0]:
                valuation += 100
                treasures.remove(treasure)
            else :
                valuation += 5
    print
    print treasures
    return valuation

possibleWays = ['R', 'L', 'U', 'D']
generation = []
for i in range(0, 1):
    size = random.randint(MIN_BOUND, MAX_BOUND)
    generation.append("")
    for j in range(1, size):
        generation[i] += random.choice(possibleWays)

print generation[0]
print (fit_function1([3, 5], generation[0], treasure, [10, 10]))
play = Playground.Playground(generation[0], 50, [10, 10], treasure,[3,5])
play.run()



        # play = Playground.Playground(generation[1], 50, [10,10], treasurePos)
# play.run()