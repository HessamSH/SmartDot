import tkinter as tk
from Dot import *
from Goal import *
from __future__ import print_function
import os
import neat
import visualize

def eval_genomes(genomes, config):
    window = tk.Tk()
    window.geometry('500x500')
    window.title("NEAT EXAMPLE")
    window.configure(bg='white')

    c = tk.Canvas(window,width=500, height=500, background="white")
    c.pack()

    goal = Goal()

    ge = []
    nets = []
    dots = []
    for genome_id, genome in genomes:
        dots.append(Dot())
        ge.append(genome)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        genome.fitness = 0

    xgoal, ygoal, goal_radius = goal.xpos, goal.ypos, goal.radius
    
    def updateAndShow():
        c.delete("all")

        dot.update([1,1])
        ## Show Goal ----------------------------------------------------------------------------------------

        c.create_oval(  goal.xpos-goal_radius,
                        goal.ypos-goal_radius,
                        goal.xpos+goal_radius,
                        goal.ypos+goal_radius,
                        fill='red', outline='black', width=1)

        c.create_oval(dot.xpos-3, dot.ypos-3, dot.xpos+3, dot.ypos+3, fill='black', outline='black', width=1)
        fitness = dot.calculateFitness()
        # print(fitness)
        
        window.after(10,updateAndShow)
        c.update()


    window.after(200,updateAndShow)
    window.mainloop()

def run(config_path):
    global pop
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    run(config_path)