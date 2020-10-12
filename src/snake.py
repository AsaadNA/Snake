import sys,pygame
from pygame.locals import *
from enum import Enum

class Directions(Enum):
    up = 1
    down = 2
    right = 3
    left = 4

class Vector:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def getX(self):
        return self.x
    def getY(self):
        return self.y

class Snake:

    def __init__(self):
        self.currentDirection = None
        self.x = 800/2
        self.y = 600/2
        self.xSpeed = 6
        self.ySpeed = 0
        self.size = 15
        self.snakeCount = 0
        self.tail = []

    def increase(self):
        for i in range(0,3):
            self.snakeCount += 1
            self.tail.append(Vector(self.x,self.y))

    def setDirection(self,x,y):
        self.xSpeed = x
        self.ySpeed = y

    def getSnakeCount(self):
        return self.snakeCount
    
    def reset(self):
        self.tail.clear()
        self.snakeCount = 0
        self.x = 800/2
        self.y = 600/2
        self.xSpeed = 0 
        self.ySpeed = 0

    def update(self):

        #This shifts the head history when only a new tail is inserted
        if len(self.tail) == self.snakeCount:
            for i in range(0,len(self.tail)-1):
                self.tail[i] = self.tail[i + 1]
        if len(self.tail) != 0:
            self.tail[len(self.tail)-1] = Vector(self.x,self.y)

        #move
        self.x += self.xSpeed
        self.y += self.ySpeed
        
        #checks for collision of head with tail
        for i in range(0,len(self.tail)-1):
            if self.x == self.tail[i].getX() and self.y == self.tail[i].getY():
                self.reset()
                break
        
        #Boundaries
        if self.x > 800 or self.x < 0 or self.y > 600 or self.y < 0:
            self.reset()
    
    def render(self,window):
        pygame.draw.rect(window,(255,0,0),(self.x,self.y,self.size,self.size))
        for i in range(0,len(self.tail)-1):
            pygame.draw.rect(window,(255,255,255),(self.tail[i].getX(),self.tail[i].getY(),self.size,self.size))

class Game:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake")
        self.window = pygame.display.set_mode((800,600))
        running = True
        clock = pygame.time.Clock()

        self.currentDirection = None
        self.snakeSpeed = 6
        self.snake = Snake()

        while running == True:
            clock.tick(60)
            for e in pygame.event.get():
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_i:
                        self.snake.increase()
                    if e.key == pygame.K_UP:
                        if self.currentDirection != Directions.down or self.snake.getSnakeCount() == 0:
                            self.snake.setDirection(0,-self.snakeSpeed)
                            self.currentDirection = Directions.up
                    if e.key == pygame.K_DOWN:
                        if self.currentDirection != Directions.up or self.snake.getSnakeCount() == 0:
                            self.snake.setDirection(0,self.snakeSpeed)
                            self.currentDirection = Directions.down
                    if e.key == pygame.K_RIGHT:
                        if self.currentDirection != Directions.left or self.snake.getSnakeCount() == 0:
                            self.snake.setDirection(self.snakeSpeed,0)
                            self.currentDirection = Directions.right
                    if e.key == pygame.K_LEFT:
                        if self.currentDirection != Directions.right or self.snake.getSnakeCount() == 0:
                            self.snake.setDirection(-self.snakeSpeed,0)
                            self.currentDirection = Directions.left
                if e.type == QUIT:
                    running = False
            self.update()
            self.render()

    def update(self):
        self.snake.update()

    def render(self):
        self.window.fill((0,0,0))
        self.snake.render(self.window)
        pygame.display.update()

game = Game()