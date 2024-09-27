from parser import *
import pygame

"""TODO: maybe introduce the idea that larger food items require more than one agent to return to the nest?,
more heavily reward finding those foods and/or helping bring them. also deterring predators?
reward the amount of food found and/or number of food spots located
reward for telling swarm about the food spots it has located by returning/sharing information with other agents?"""

class EvolveEach:
    def __init__(self, agent):
        self.agent = agent
        self.gen_seed = random.randint(0,400)


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

#debugging and git controls
#powershell how to use it

# call neighbor (within perception radius) and heed_call for teamwork
# should only go to neighbor if within perception radius?

# reward agents that have performed a task within the last time
# population success fitness metric instead of genome-specific fitness metric? (credit assignment issue)

# implement a eat food/tired metric?

# memory to remember where they have visited (brand new location visited high reward)
# tasks requiring teamwork
# diversity function
# actually implement the evolution
# assumption alignment trackers
# different roles

class Evolver:
    def __init__(self, agent):
        self.agent = agent
        self.environment = self.agent.environment
        # ie, genomes that are not tagged with fitness values?
        # or should genomes get passed with their fitness values?
        self.unused_genomes = deepcopy(self.agent.known_genomes)
        self.used_genomes = deepcopy(self.agent.genomes_done)
        self.new_genomes = []
    
    # should I run this individually for each tick? assign updating fitness values over time?
    def update_fitness(self):
        # TODO: would doing so require some kind of memory that we are trying to avoid in this project?
        if self.agent.time_since_move > 45:
            # print(f'{agent.id} hasn"t moved in {agent.time_since_move} so switching genome')
            #change genome! perform evolutionary operations
            agent.curr_genome.fitness = 0
            agent.genomes_done.append(agent.curr_genome)
            # should we assign fitness values to them?
            if len(agent.known_genomes) != 0:
                self.agent.curr_genome = self.switch_genome()
                parser = Parser(self.agent)
                # print("printing genes: ", {type(self.agent.curr_genome.genes)})
                self.agent.behaviour_tree = py_trees.trees.BehaviourTree(parser.parse_tree())
            self.agent.time_since_move = 0
        else:
            pass

    def mutate(self, genome):
        i = 0
        new_genome = Genome()
        genome1 = deepcopy(genome)
        for i in range(len(genome1.genes)):
            val = random.randint(0,100)
            # 25% chance of mutating
            if val < 25:
                genome1.genes[i] = random.randint(0,10)
        # self.new_genomes.append(genome)
        new_genome.genes = genome1.genes
        return new_genome

    def crossover(self, genes1, genes2):
        # crossover from highest performing two genomes
        new_genome1 = []
        new_genome2 = []
        # curr_index = 0
        mid_index = len(genes1)//2
        print('original length', {len(genes1)})
        # print(f'genes1: {genes1[:10]}')
        # print(f'genes1: {genes2[:10]}')
        for i in range(mid_index+1):
            new_genome1.append(genes1[i])
        for i in range(mid_index+1):
            new_genome2.append(genes2[i])
            # print(curr_index)
        # print("starting second half")
        for i in range(mid_index):
            new_genome2.append(genes2[i])
        for i in range(mid_index):
            new_genome1.append(genes1[i])
        # while curr_index != len(genes1):
        #     new_genome1.append(genes2[:curr_index])
        #     new_genome2.append(genes1[curr_index:])
        #     curr_index += 1
            # print(curr_index)
        # print(f'first crossed genome: {new_genome1[:10]}')
        # print(new_genome2[:10])
        # print('final length:', len(new_genome1), len(new_genome2))
        return new_genome1, new_genome2

    def switch_genome(self):
        print("switching genome")
        all_genomes = []
        # all_genomes = self.used_genomes+self.unused_genomes
        for geno in self.used_genomes:
            all_genomes.append(geno)
        for geno in self.unused_genomes:
            all_genomes.append(geno)
        # print(f'genes of first genome: {all_genomes[0].genes}')
        # print(f'testing: {type(all_genomes[0].genes[0])}')
        # for genome in all_genomes:
        while len(all_genomes) != 0:
            genome = random.choice(all_genomes)
            all_genomes.remove(genome)
            val = random.randint(0,100)
            if val <= 25:
                print('mutating')
                #mutate genome
                self.new_genomes.append(self.mutate(genome))
            if val > 25 and val < 75 and len(all_genomes):
                print('crossover')
                # for now just randomly crossover the genomes, later implement a crossover function influenced by the fitness value
                to_cross = random.choice(all_genomes)
                # print(type(to_cross))
                all_genomes.remove(to_cross)
                crossed1, crossed2 = self.crossover(genome.genes, to_cross.genes)
                # print(f'after cross: {crossed1}')
                # print(f'after cross: {crossed2}')
                gencross1 = Genome()
                gencross1.genes = crossed1
                gencross2 = Genome()
                gencross2.genes = crossed2
                self.new_genomes.append(gencross1)
                self.new_genomes.append(gencross2)
            else:
                print('nothing')
                #do nothing
                self.new_genomes.append(genome)
        use_this_one = random.choice(self.new_genomes)
        #refresh the new_genomes?
        # print(f'type of switchgenome func: {type(use_this_one.genes)}')
        return use_this_one

# TODO: why do some genomes have different lengths?

NUM_FOOD = 30
environment = Environment(NUM_FOOD)
for agent in environment.boids:
    parser = Parser(agent)
    agent.behaviour_tree = py_trees.trees.BehaviourTree(parser.parse_tree())
i = 0
running = True
while running:
    # print(f'Tick: {i}')
    for agent in environment.boids:
        # switch genomes when not moving / accomplishing anything
        # print(agent.time_since_move)
        # also switch genomes when having not accomplished anything new recently? or just after a time threshold
        for neighbor in environment.boids:
            if neighbor != agent:
                if check_collision(agent, neighbor):
                    if neighbor.curr_genome not in agent.known_genomes:
                        # print(f"sharing genome! {agent.id} and {neighbor.id}")
                        agent.known_genomes.append(neighbor.curr_genome)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0, 0, 0))
    for spot in environment.foods:
        spot.show(screen)
    environment.nest.show(screen)
    for food_area in environment.food_areas:
        food_area.show(screen)
    not_movin = 0
    for agent in environment.boids:
        # print(f'before tick {agent.position}')
        agent.previous_position = deepcopy(agent.position)
        agent.behaviour_tree.tick()
        # print(f'after tick {agent.position}')
        if agent.previous_position == agent.position:
            # print("the positions were the same")
            agent.time_since_move += 1
            not_movin += 1
        # print(agent.curr_genome.genes)
        agent.show(screen)
        evolver = Evolver(agent)

        evolver.update_fitness()

    # print(not_movin)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()