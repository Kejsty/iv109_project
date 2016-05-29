import pygame
import sys
# Initialize the game engine


Colors = {"YELLOW": (254, 254, 0), "RED": (34, 123, 111), "GREY": (224, 224, 224), "BROWN": (153, 76, 0),
          "BEGIN_RED": (255, 204, 204), "BLACK": (0, 0, 0)}

robotPic = pygame.image.load("robot.jpg")
treasurePic = pygame.image.load("treasure.png")
wallPic = pygame.image.load("wall.jpg")

ROODSIZE = 30
GAMESIZE = [10,10]
TREASURE = [[1,3], [1,4], [3,2], [3,8], [4,5], [5,4],[5,8],[6,3], [7,8], [8,3] ]
BORDERS = [[2,3],[2,4],[2,5], [2,7],[4,2],[4,3], [6,4], [6,7], [6,8], [7,1], [7,4], [7,7]]

# for complicated map
# TREASURE = [[1,3], [1,8],[3,1], [3,8], [4,1],[4,5], [5,4], [5,8],  [7,8], [8,3]]
# BORDERS = [[1,7], [2,1],[2,2],[2,3],[2,4],[2,5],[2,7],[3,2], [3,7],[4,2],[4,3],[4,4],[5,2],
#            [6,2],[6,4],[6,6],[6,7],[7,2],[7,3],[7,4],[7,6],[7,7]]

ROBOT = [5,3]

class Playground:
    def __init__(self, way):
        self.way = way
        self.roodSize = ROODSIZE
        self.gamesize = GAMESIZE
        self.trueGameSize = [GAMESIZE[0]*self.roodSize, GAMESIZE[1] * self.roodSize ]
        self.wasRed = [False,0]
        self.robot = [ROBOT[0] * self.roodSize, ROBOT[1] * self.roodSize]
        self.treasures = self.convertCoordinates(TREASURE)
        self.robotPic = pygame.transform.scale(robotPic, (self.roodSize, self.roodSize))
        self.treasurePic = pygame.transform.scale(treasurePic, (self.roodSize, self.roodSize))
        self.wallPic = pygame.transform.scale(wallPic, (self.roodSize - 1, self.roodSize - 1))


    def convertCoordinates(self, array):
        for i in range(0, len(array)):
            array[i] = [array[i][0] * self.roodSize, array[i][1] * self.roodSize]
        return array

    def drawRobot(self,screen, x, y):
        pygame.draw.rect(screen,
                         Colors["GREY"],
                         [x, y, self.roodSize, self.roodSize])
        screen.blit(self.robotPic, (x, y))

    def drawTreasure(self, screen, x, y):
        pygame.draw.rect(screen,
                         Colors["BLACK"],
                         [x, y, self.roodSize, self.roodSize])
        screen.blit(self.treasurePic, (x, y))

    def applyWalls(self,screen):
        pygame.draw.rect(screen, Colors["BROWN"], [0, 0, self.trueGameSize[0], self.roodSize])
        pygame.draw.rect(screen, Colors["BROWN"],
                         [0, self.trueGameSize[1] - self.roodSize, self.trueGameSize[0], self.roodSize])
        pygame.draw.rect(screen, Colors["BROWN"], [0, 0, self.roodSize, self.trueGameSize[1]])
        pygame.draw.rect(screen, Colors["BROWN"],
                         [self.trueGameSize[0] - self.roodSize, 0, self.roodSize, self.trueGameSize[1]])

        for wall in BORDERS :
            pygame.draw.rect(screen, Colors["BROWN"], [wall[0]*self.roodSize, wall[1]*self.roodSize, self.roodSize, self.roodSize])
            screen.blit(self.wallPic, (1+wall[0]*self.roodSize, 1+wall[1]*self.roodSize))


        for i in range(0, self.gamesize[0]):
            screen.blit(self.wallPic, (i * self.roodSize + 1, 1))
            screen.blit(self.wallPic, (i * self.roodSize + 1,self.trueGameSize[1]- self.roodSize + 1))
        for j in range(0, self.gamesize[1]):
            screen.blit(self.wallPic, (1, j * self.roodSize + 1 ))
            screen.blit(self.wallPic, (self.trueGameSize[0] - self.roodSize + 1, j * self.roodSize + 1))

    def run(self):
        pygame.init()
        size = (self.trueGameSize[0],self.trueGameSize[1])
        screen = pygame.display.set_mode(size)

        for treasure in self.treasures:
            self.drawTreasure(screen, treasure[0], treasure[1])

        self.applyWalls(screen)

        pygame.draw.rect(screen, Colors["GREY"], [self.robot[0], self.robot[1], self.roodSize, self.roodSize])
        self.drawRobot(screen, self.robot[0], self.robot[1])
        pygame.display.flip()
        self.wasRed = [True, 204 + 51]
        for word in self.way:
            self.move(screen, word)
            pygame.display.flip()
        done = False
        pygame.image.save(screen, "result.jpg")
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True

        pygame.quit()

    def color(self,screen, x, y):
        if self.wasRed[0]:
            pygame.draw.rect(screen,
                             (255, max(self.wasRed[1] - 51,30),
                              max(self.wasRed[1] - 51, 30)),
                             [self.robot[0], self.robot[1], self.roodSize, self.roodSize])
            self.wasRed[0] = False

        if screen.get_at((x, y))[0] == 255:
            ''' he accesed place he already was'''
            self.wasRed = [True, screen.get_at((x, y))[2]]
            self.drawRobot(screen, x, y)
            self.robot= [ x, y]
        elif screen.get_at((x, y))[0] == 153:
            ''' it's wall'''
            self.drawRobot(screen,self.robot[0], self.robot[1])
            self.wasRed = [True,0]
        else:
            ''' it's new place or treasure'''
            self.drawRobot(screen, x, y)
            self.robot = [x, y]
            self.wasRed =  [True, 204 + 51]

    def move(self,screen, direction):
        if direction == 'L':
            self.color(screen, self.robot[0] - self.roodSize, self.robot[1])
        elif direction == 'R':
            self.color(screen, self.robot[0] + self.roodSize, self.robot[1])
        elif direction == 'D':
            self.color(screen, self.robot[0], self.robot[1] + self.roodSize)
        else:
            self.color(screen, self.robot[0], self.robot[1] - self.roodSize)