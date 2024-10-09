from parser import *
import pygame

"""TODO: maybe introduce the idea that larger food items require more than one agent to return to the nest?,
more heavily reward finding those foods and/or helping bring them. also deterring predators?
reward the amount of food found and/or number of food spots located
reward for telling swarm about the food spots it has located by returning/sharing information with other agents?"""



def check_nodes_stack(node):

    # init node dictionary
    node_dict = {
        'Move to food_area': 0,
        'Move to neighbor': 0,
        'Move to den': 0,
        'Do nothing': 0,
        'Food Check': 0,
        'Spot Check': 0,
        'Flock': 0,
        'Explore': 0,
        'Pick up': 0,
        'Drop it': 0,
        'Sequence': 0,
        'Selector': 0
    }

    node_dict = check_node_stack(node, node_dict)

    return node_dict

def check_node_stack(node, node_dict):
    stack = [node]
    
    while stack:
        current_node = stack.pop()

        node_dict[current_node.name] += 1

        if hasattr(current_node, "children"):
            stack.extend(current_node.children)
    
    return node_dict



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

def calc_fitness(agent):
    # dynamic fitness value that lessens over time of having accomplished nothing
    if agent.fitness == 0:
        agent.time_of_0_fitness += 1
    agent.previous_position = deepcopy(agent.position)
    agent.behaviour_tree.tick()
    if agent.previous_position == agent.position and agent.curr_genome.fitness != 0:
        # decrement fitness by each tick it hasn't moved
        agent.fitness -= 1
    # if check_collision(agent, agent.environment.nest) and agent.has_food:
    # will this see if it has occurred?
    if agent.dropped_food:
        # print('dropped food!')
        agent.curr_genome.fitness += 50
        agent.fitness += 50
    # also if finding NEW food spots
    if agent.time_of_0_fitness >= 100 and (len(agent.new_genomes) != 0) or (len(agent.finished_genomes) != 0):
        # MAKE SURE TO RESET TIME OF 0 FITNESS
        agent.time_of_0_fitness = 0
        agent.fitness = 0
        evolver = Evolver(agent)
        # print("switching genome ! ")
        agent.curr_genome = evolver.switch_genome()
        parser = Parser(agent)
        agent.behaviour_tree = py_trees.trees.BehaviourTree(parser.parse_tree())

class Evolver:
    def __init__(self, agent):
        self.agent = agent
        self.environment = self.agent.environment
        # ie, genomes that are not tagged with fitness values?
        # or should genomes get passed with their fitness values?
        self.new_ones_to_use = deepcopy(self.agent.new_genomes)
        self.old_genomes = deepcopy(self.agent.finished_genomes)
        self._after_genomes = []



    #NOT USED ANYMORE
    # should I run this individually for each tick? assign updating fitness values over time?
    def update_fitness(self):
        # TODO: would doing so require some kind of memory that we are trying to avoid in this project?
        if self.agent.time_since_move > 45:
            #change genome! perform evolutionary operations
            agent.curr_genome.fitness = 0
            agent.old_genomes.append(agent.curr_genome)
            # should we assign fitness values to them?
            if len(agent.known_genomes) != 0:
                self.agent.curr_genome = self.switch_genome()
                parser = Parser(self.agent)
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
        new_genome.genes = genome1.genes
        return new_genome

    def crossover(self, genes1, genes2):
        # crossover from highest performing two genomes
        new_genome1 = []
        new_genome2 = []
        mid_index = len(genes1)//2
        for i in range(mid_index):
            new_genome1.append(genes1[i])
        for i in range(mid_index):
            new_genome2.append(genes2[i])
        for i in range(mid_index):
            new_genome2.append(genes2[i])
        for i in range(mid_index):
            new_genome1.append(genes1[i])
        return new_genome1, new_genome2

    def switch_genome(self):
        # fitness specific to agent (do something every once in a while)
        # fitness specific to genome (based on history at accomplishing task? should it reset every time it is run?)
        # should genome fitness be assigned by averaging the previous fitness values of the genomes that created it?
        # TODO: figure out how to implement the evolution with an emphasis towards genomes that have large fitness values

        # some kind of matrix multiplication that assigns weights (percentage chances of selecting that genome to work with) to genomes??
        # hard code it?

        self.new_ones_to_use.append(self.agent.curr_genome)

        all_genomes = []
        for geno in self.new_ones_to_use:
            # print(f'{geno} new genomes')
            all_genomes.append(geno)
        for geno in self.old_genomes:
            # print(f'{geno} old genomes')
            all_genomes.append(geno)
        
        """This is where I am currently implementing the additional fitness incrementation for trees that are more actions/conditions than do nothings"""
        # I probably should implement a boolean check to see if this test has already been run on this particular genome so it doesn't keep incrementing when it should be run new every iteration

        for geno in all_genomes:
            print(f'Before: {geno.fitness}')
            # maybe have each genome have a behaviour tree attached to it so it doesnt have to reparse every time?
            agent = environment.secret_agent
            agent.curr_genome = geno
            parser = Parser(agent)
            agent.behaviour_tree = py_trees.trees.BehaviourTree(parser.parse_tree())
            tree_dict = check_nodes_stack(agent.behaviour_tree.root)
            tree_fitness: float = 0
            num_nodes: float = 0
            for key in tree_dict.keys():
                if key in ["Move to food_area", "Move to neighbor", "Move to den", "Explore", "Pick up", "Drop it", "Flock"]:
                    tree_fitness += tree_dict[key]
                    num_nodes += tree_dict[key]
            num_nodes += tree_dict["Do nothing"]
            print(f'Num actual nodes: {tree_fitness}, Total nodes: {num_nodes}, gives an additional {(tree_fitness/num_nodes)*20} to the genome fitness')
            geno.fitness += (tree_fitness/num_nodes)*10
            print(f'After: {geno.fitness}')

        genomes_sorted = sorted(all_genomes, key=lambda genome: genome.fitness, reverse=True)
        # print(genomes_sorted[0].fitness)

        num_to_take = len(all_genomes) % 10
        # print(f'10% of {len(all_genomes)} is: {num_to_take}')

        # print(genomes_sorted[0].fitness)

        if num_to_take >= 4:
            num_to_take = 4

        # sort by the top 10%
        for i in range(num_to_take):
            self._after_genomes.append(genomes_sorted[i])
            # self.agent.finished_genomes.append(self._after_genomes[i])

            # gen_copy = genomes_sorted[i]
            # self.agent.finished_genomes.append(gen_copy)
            # if len(self.agent.finished_genomes) > 10:
            #     self.agent.finished_genomes.append(gen_copy)
            #     self.agent.finished_genomes = sorted(self.agent.finished_genomes, key=lambda genome: genome.fitness)[:5]
            # else:
            #     self.agent.finished_genomes.append(gen_copy)

        # self.new_genomes.append(genomes_sorted[1])
        while len(self._after_genomes) <= 15:
            genome = random.choice(all_genomes)
            # all_genomes.remove(genome)
            val = random.randint(0,100)
            if val <= 25:
                #mutate genome
                self._after_genomes.append(self.mutate(genome))
            if val > 25 and val < 75 and len(all_genomes):
                # for now just randomly crossover the genomes, later implement a crossover function influenced by the fitness value
                to_cross = random.choice(all_genomes)
                # all_genomes.remove(to_cross)
                crossed1, crossed2 = self.crossover(genome.genes, to_cross.genes)
                gencross1 = Genome()
                gencross1.genes = crossed1
                gencross2 = Genome()
                gencross2.genes = crossed2
                self._after_genomes.append(gencross1)
                self._after_genomes.append(gencross2)
            else:
                self._after_genomes.append(genome)
        use_this_one = random.choice(self._after_genomes)
        # self.agent.finished_genomes = []
        # # for gen in self._after_genomes:
        # #     self.agent.finished_genomes.append(gen)

        self._after_genomes = []
        # self.agent.new_ones_to_use = []
        # keep final genome random, but keep around the top 10% genomes with their assigned fitness values to keep them in the pop
        # refresh the new_genomes?
        return use_this_one

NUM_FOOD = 0
environment = Environment(NUM_FOOD)
for agent in environment.boids:
    parser = Parser(agent)
    agent.behaviour_tree = py_trees.trees.BehaviourTree(parser.parse_tree())
i = 0
running = True
while running:
    # print(i)
    # i += 1
    for agent in environment.boids:
        # switch genomes when not moving / accomplishing anything
        # also switch genomes when having not accomplished anything new recently? or just after a time threshold
        for neighbor in environment.boids:
            if neighbor != agent:
                if check_collision(agent, neighbor):
                    if neighbor.curr_genome not in agent.new_genomes:
                        # print(f"sharing genome! {agent.id} and {neighbor.id}")
                        agent.new_genomes.append(neighbor.curr_genome)
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
        calc_fitness(agent)
        # evolver = Evolver(agent)
        if agent.has_food:
            agent.color = (64,224,208)
        else:
            agent.color = (255,255,255)
        agent.show(screen)
    print(environment.nest.food)
        # evolver.update_fitness()
    pygame.display.flip()
    clock.tick(60)
pygame.quit()

#TODO: if the environment is for whatever reason approaching a low fitness score (not going to survive), the rate of mutation/crossover/exploration/should increase! would be kind of fun to implement