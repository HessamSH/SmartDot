## ALL THE PROGRAM PROBLEMS ---------------------------------------------------
## 1: WHEN KILLING A DOT FOR BEING LAZY (AFTER TIME_TILL_DEATH) WE DONT TAKE
##INTO ACCOUNT IT'S FITNESS AND JUST KILL IT
##
## 2: WHEN PASSING LEFT AND UP BOUNDARIES, WE CAN'T SEE THE DOTS ANYMORE

import pygame
import os
import math as mt
import neat
import sys
import time



pygame.init()
## Defining display variables ----------------------------------------------
time_till_death = 8
display_width = 800
display_height = 600
black = (0,0,0)
white = (255,255,255)
FONT = pygame.font.Font('freesansbold.ttf', 20)
SCREEN = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Smart Dot AI')
clock = pygame.time.Clock()


class Environment():
    def __init__(self):
        self.border = [0,0, display_width, display_height]
    def show(self):
        pygame.draw.rect(SCREEN, (50,50,50), pygame.Rect(self.border[0], self.border[1], self.border[2], self.border[3]), 2)

## GOAL CLASS---------------------------------------------------------------------
class Goal():
    def __init__(self):
        self.xpos = 0.9*display_width
        self.ypos = display_height / 2
        self.radius = 25
    def show(self):
        pygame.draw.circle(SCREEN, (255,0,0), (self.xpos, self.ypos), self.radius)


## DOT CLASS----------------------------------------------------------------------
class Dot:
    goaltest = Goal()
    def __init__(self):
        self.radius = 10
        self.THEBALLIMG = pygame.image.load(os.path.join("Assets", "rsz_theball.png"))
        self.THEBALLIMG = pygame.transform.scale(self.THEBALLIMG, (self.radius, self.radius))
        self.alive = True
        self.xpos = 0.1 * display_width
        self.ypos = display_height / 2
        self.speed = 5
        self.fitness = 0
        self.steps = 0
        self.reachedGoal = False
    
    def see(self):
        try:
            rightx , leftx, upy, downy = 0,0,0,0
            for i in range(int(self.xpos + self.radius), display_width):
                if SCREEN.get_at((i, int(self.ypos))) == (0,0,0,255):
                    rightx += 1
            for i in range(0, int(self.xpos - self.radius)):
                if SCREEN.get_at((i, int(self.ypos))) == (0,0,0,255):
                    leftx += 1
            for j in range(int(self.ypos + self.radius), display_height):
                if SCREEN.get_at((int(self.xpos), j)) == (0,0,0,255):
                    downy += 1
            for j in range(0, int(self.ypos - self.radius)):
                if SCREEN.get_at((int(self.xpos), j)) == (0,0,0,255):
                    upy += 1
            distfromgoalx = self.goaltest.xpos - self.xpos
            distfromgoaly = self.goaltest.ypos - self.ypos
            return distfromgoalx, distfromgoaly, rightx, leftx, upy, downy
        except IndexError:
            print ("x and y is : (%d, %d)" %(self.xpos, self.ypos))



    def move(self, direction):
        xrange = [0, display_width]
        yrange = [0, display_height]
        newx = self.xpos + self.speed * direction[0]
        newy = self.ypos + self.speed * direction[1]
        ## Check for IndexError ----------------------------------------------
        if newx < xrange[0] or newx >= xrange[1] or newy < yrange[0] or newy >= yrange[1]:
            self.alive = False
        else:
            self.xpos = newx
            self.ypos = newy
            self.steps += 1


## Countdown timer-------------------------------------------------------------       

##-----------------------------------------------------------------------------
## if not dead, move and check if it is dead now
    def update(self, direction):
        if self.alive == False or self.reachedGoal == True:
            return
        self.move(direction)
        # if self.xpos < 2 or self.xpos > display_width-2:
        #     self.alive = False
        # if self.ypos < 2 or self.ypos > display_height-2:
        #     self.alive = False
        
        ## Check if goal is reached -------------------------------------------
        if self.goaltest.xpos - self.goaltest.radius < self.xpos and self.goaltest.xpos + self.goaltest.radius > self.xpos:
            if self.goaltest.ypos - self.goaltest.radius < self.ypos and self.goaltest.ypos + self.goaltest.radius > self.ypos:
                self.reachedGoal = True
                
    def calculateFitness(self):
        xgoal , ygoal = self.goaltest.xpos, self.goaltest.ypos
        self.fitness = 1 /( mt.dist((self.xpos, self.ypos), (xgoal, ygoal)))
        if self.reachedGoal == True:
            self.fitness *= 5
        print(self.fitness)
        return self.fitness
    
    def show(self):
        SCREEN.blit(self.THEBALLIMG, (self.xpos - self.radius, self.ypos - self.radius))
  



## run the damn stuff -----------------------------------------------------------------
def eval_genomes(genomes, config):
    startofGen = time.time()
    deathDots = []
    reached = 0
    def removeDot(ndx):
        deathDots.append(dots.pop(ndx))
        ge.pop(ndx)
        nets.pop(ndx)
    
    def statistics(num, reached):
        text_1 = FONT.render(f'Dots Alive:  {num}', True, (0, 0, 0))
        text_2 = FONT.render(f'Generation:  {pop.generation+1}', True, (0, 0, 0))
        text_3 = FONT.render(f'Reached Goal:  {reached}', True, (0, 0, 0))

        SCREEN.blit(text_1, (50, 0.9*display_height))
        SCREEN.blit(text_2, (50, 0.9*display_height+20))
        SCREEN.blit(text_3, (50, 0.9*display_height+40))

    ## our the lists ------------------------------------------------------------------
    dots = []
    ge = []
    nets = []

    for genome_id, genome in genomes:
        dots.append(Dot())
        genome.fitness = dots[-1].calculateFitness() 
        ge.append(genome)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)

    goal = Goal()
    env = Environment()
    onthego = True
    while onthego:
        curofGen = time.time()
        SCREEN.fill(white)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                onthego = False
                pygame.quit()
                sys.exit()
        
        if len(dots) == 0:
            break
        
        goal.show()
        env.show()
        
        if curofGen - startofGen > time_till_death:
            print('time elapsed...')
            for dot in dots:
                if dot.alive == True:
                    dot.alive = False
            startofGen = time.time()

        searching = 150
        ## Show and check for number of alive or searching -------------------------------
        for i, dot in enumerate(dots):
            dot.show()
            if dot.alive == False or dot.reachedGoal == True:
                if dot.reachedGoal == True:
                    reached += 1
                ge[i].fitness = dot.calculateFitness()
                searching -= 1
            # if dot.alive == False:
                removeDot(i)
        for dot in deathDots:
            dot.show()
        
        ## When they're all dead, calculate their fitness --------------------------------
        # if searching == 0:
        #     for i, dot in enumerate(dots):
        #         ge[i].fitness = dot.calculateFitness()

        
        ## give input to NN and get output to update the dot ------------------------------
        for i, dot in enumerate(dots):
            distfromgoalx, distfromgoaly, rightx, leftx, upy, downy = dot.see()
            output = nets[i].activate((distfromgoalx,
                                       distfromgoaly,
                                       rightx,
                                       leftx,
                                       upy,
                                       downy))
            if output[0] > 0.5:
                upordown = 1
            if output[0] < -0.5:
                upordown = -1
            if output[1] > 0.5:
                leftorright = 1
            if output[1] < -0.5:
                leftorright = -1
            dot.update([leftorright,upordown])

        statistics(len(dots), reached)
        clock.tick(60)
        pygame.display.update()
    time.sleep(2)



# Setup the NEAT Neural Network -------------------------------------------
def run(config_path):
    global pop
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )

    pop = neat.Population(config)
    pop.run(eval_genomes, 50)


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    run(config_path)
