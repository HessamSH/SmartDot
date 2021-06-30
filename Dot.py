from math import dist
from Goal import *

class Dot:
    goaltest = Goal()
    def __init__(self):
        self.alive = True
        self.xpos = 50
        self.ypos = 250
        self.speed = 1
        self.fitness = 0
        self.steps = 0
        self.reachedGoal = False
    
    def move(self, direction):
        self.steps += 1
        self.xpos += self.speed * direction[0]
        self.ypos += self.speed * direction[1]


##-----------------------------------------------------------------------------
## if not dead, move and check if it is dead now
    def update(self, direction):
        if self.alive == False or self.reachedGoal == True:
            return
        self.move(direction)
        if self.xpos < 2 or self.xpos > 497:
            self.alive = False
        if self.ypos < 2 or self.ypos > 497:
            self.alive = False
        
        ## Check if goal is reached -------------------------------------------
        if self.goaltest.xpos - self.goaltest.radius < self.xpos and self.goaltest.xpos + self.goaltest.radius > self.xpos:
            if self.goaltest.ypos - self.goaltest.radius < self.ypos and self.goaltest.ypos + self.goaltest.radius > self.ypos:
                self.reachedGoal = True
                
    def calculateFitness(self):
        if self.alive == False or self.reachedGoal == True:
            pass
        xgoal , ygoal = self.goaltest.xpos, self.goaltest.ypos
        self.fitness = self.steps + 1 /( 2*(dist((self.xpos, self.ypos), (xgoal, ygoal))))
        print(self.fitness)
        return self.fitness

        