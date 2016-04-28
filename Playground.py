import pygame
import sys
# Initialize the game engine


Colors = {"YELLOW": (254, 254, 0), "RED": (34, 123, 111), "GREY": (224, 224, 224), "BROWN": (153, 76, 0),
          "BEGIN_RED": (255, 204, 204), "BLACK": (0, 0, 0)}

robotPic = pygame.image.load("robot.jpg")
treasurePic = pygame.image.load("treasure.png")
wallPic = pygame.image.load("wall.jpg")



class Playground:
    def __init__(self, strategy, roodSize, gameSize, gameMap, robotInit):
        self.strategy = strategy
        self.roodSize = roodSize
        self.gameSize = gameSize
        self.gameMap = gameMap
        self.trueGameSize = (gameSize[0]*roodSize, gameSize[1] * roodSize )
        self.wasRed = [False,0]
        self.robotPos = robotInit

        self.robotPic = pygame.transform.scale(robotPic, (roodSize, roodSize))
        self.treasurePic = pygame.transform.scale(treasurePic, (roodSize, roodSize))
        self.wallPic = pygame.transform.scale(wallPic, (roodSize - 1, roodSize - 1))


    def convertCoordinates(self, array):
        for i in range(0, len(array)):
            array[i] = [array[i][0] * self.roodSize, array[i][1] * self.roodSize]
        return array

    def drawEmpty(self,screen, x, y ):
        pygame.draw.rect(screen, Colors["BROWN"], [x*self.roodSize, y*self.roodSize, self.roodSize, self.roodSize])

    def drawRobot(self,screen, x, y):
        pygame.draw.rect(screen,
                         Colors["GREY"],
                         [x*self.roodSize, y*self.roodSize, self.roodSize, self.roodSize])
        screen.blit(self.robotPic, (x*self.roodSize, y*self.roodSize))

    def drawTreasure(self, screen, x, y):
        pygame.draw.rect(screen,
                         Colors["BLACK"],
                         [x*self.roodSize, y*self.roodSize, self.roodSize, self.roodSize])
        screen.blit(self.treasurePic, (x*self.roodSize, y*self.roodSize))

    def drawWall(self, screen, x, y):
        screen.blit(self.wallPic, (x * self.roodSize, y * self.roodSize))

    def drawGame(self, screen, gameMap):
        for x in range(len(gameMap)):
            for y in range(len(gameMap[x])):
                if gameMap[x][y] == '.':
                    self.drawEmpty(screen, x,y)
                if gameMap[x][y] == '*':
                    self.drawTreasure(screen, x, y)
                if gameMap[x][y] == '#':
                    self.drawWall(screen, x, y)
        self.drawRobot(screen, self.robotPos[0], self.robotPos[1])

    def run(self):
        pygame.init()
        size = (self.trueGameSize[0],self.trueGameSize[1])
        screen = pygame.display.set_mode(size)

        self.drawGame(screen, self.gameMap)
        pygame.display.flip()

        self.wasRed = [True, 204 + 51]

        for dir in self.strategy:
            self.move(screen, dir)
            pygame.display.flip()

        done = False
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