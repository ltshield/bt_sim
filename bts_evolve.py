from parser import *

# fitness function based on how much food is collected in time, vs one based on how fast all food is collected
# set the environment to reset after each run as to not let the randomness of the environment possibly affect the results (or do we want that for adaptability?)
# simply keep the best result, code mutation.

# regarding the problem of trying to determine the "difference/diversity" between genomes/resulting phenotypes and to create a fitness off of that...
# is there a way to compare two behaviour trees?
# calculate the distance between two genomes as you would two points (if one genome is longer, you can reward or subtract based on length based on whether you want deeper)
# keep track of the part of the genomes that are necessary, then keep only the part of the genome that was actually used to parse the grammar? (efficiency?)
# or make it so that the genome starts as an empty list but gets appended to with a random value (0-10 or based on options in grammar?) when necessary for parsing

# having only the necessary length of the genome would make rating based off of diversity easier, while also making mutation more effective?
# cross/mut would be interesting, (does it have to be allowed to both be specific lengths?) it should probably be allowed to add more numbers if necessary during parsing
# since it could result in an invalid genotype, or should we just not count it if it results in an invalid genotype?
# could allow for more unique phenotypes though, but you risk longer and longer results (maybe lessen the fitness of large phenotypes to prevent overgrowth while also
# allowing for bigger solutions to be created in case one of them is fantastic!)
# would introducing a negative fitness for longer solutions have a negative impact on exploring the solution space? restricting its search? depends on needs of user
import copy

# have it but not having it and keepinig it random would give you a more general solution
GLOBAL_SEED = random.randint(0,400)
NUM_OF_GENERATIONS = 4
# having a global seed keeps the simulations the same through every generation
# making it a local seed that just lasts for the generation might be the best way to prevent a random best fitness

# environment = Environment(NUM_FOOD)

class Evolver:
    def __init__(self, agent):
        self.rand_seed = random.randint(0,400)
        random.seed = self.rand_seed
        self.agent = agent
        self.new_genomes = []
        # make it the same for each generation? or change after each generation (more general solution)?
        # self.genomes = [Genome(self.agent) for x in range(50)]

    # subtract by how long the behaviour tree is, how many nodes it has? simplest == better
    # def fitness(self):
    #     self.agent.fitness = ()

    def mutate(self, genome):
        i = 0
        for i in range(len(genome)):
            val = random.randint(0,100)
            # 25% chance of mutating
            if val < 25:
                genome[i] = random.randint(0,10)
        # self.new_genomes.append(genome)
        return genome
    
    def crossover(self, genes1, genes2):
        # crossover from highest performing two genomes
        new_genome1 = []
        new_genome2 = []
        curr_index = 0
        mid_index = len(genes1)//2
        while curr_index < mid_index:
            new_genome1.append(genes1[curr_index])
            new_genome2.append(genes2[curr_index])
            curr_index += 1
            # print(curr_index)
        # print("starting second half")
        while curr_index != len(genes1):
            new_genome1.append(genes2[curr_index])
            new_genome2.append(genes1[curr_index])
            curr_index += 1
            # print(curr_index)
        return new_genome1, new_genome2

    # find a way to normalize the two vectors to dimensionally-

    def run_genome(self):
        num_food = 30
        random.seed = self.rand_seed
        parser = Parser(self.agent)
        self.agent.behaviour_tree = py_trees.trees.BehaviourTree(parser.parse_tree())
        pygame.init()
        environment = Environment(NUM_FOOD)
        i = 0



        # maybe take these out, have them run solo
        for _ in range(NUM_BOIDS):
            environment.boids[i].behaviour_tree = explore_tree(environment.boids[i])
            i += 1



        # for _ in range(30):
        #     environment.boids[i].behaviour_tree = flock_tree(environment.boids[i])
        #     i += 1
        start_time = pygame.time.get_ticks()

        running=True
        while running:
            elapsed_time = pygame.time.get_ticks() - start_time
            # print(f"{elapsed_time}")
            if elapsed_time >= 3000:
                running=False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                # run until all food collected
            # if num_food == environment.nest.food:
            #     running = False
                # or until it has run on for too long
            # if (pygame.time.get_ticks() - start_time) > 100000:
            #     running = False


            for agent in environment.boids:
                agent.behaviour_tree.tick()


            self.agent.behaviour_tree.tick()    

        # to account for randomness affecting effectiveness?
        # not having random agent movements to differentiate them, I lowered the division factor by 10 to see bigger differences
        fitness = environment.nest.food * 10
        pygame.quit()
        return fitness
    
    def run_population(self):
        best_fitness = 0
        best_genome = []
        # doing it solo without other agents in the environment is making it very hard for it to find a genome that gets any fitness value at all
        # maybe lessen the size of the environment/up the food?
        # or implement the simultaneous evolution
        # or just let the hard coded agents be in the sim
        while best_genome == []:
            # print("trying again")
            for gen in self.agent.genomes_to_do:
                # print(gen.genes)
                self.agent.genome = copy.deepcopy(gen.genes)
                try:
                    gen.fitness = self.run_genome()
                except:
                    print("couldn't run genome")
                    gen.fitness = 0
            # sorted list based on fitness value?
            for gen in self.agent.genomes_to_do:
                if gen.fitness > best_fitness:
                    best_genome = gen.genes
                    best_fitness = gen.fitness
            if best_genome == []:
                self.agent.genomes_to_do = [Genome() for _ in range(10)]
        return best_genome
    
    def run_the_generations(self):
        for i in range(NUM_OF_GENERATIONS):
            print("here")
            self.run_the_generation()
            for i in range(len(self.agent.genomes_to_do)-1):
                self.agent.genomes_to_do[i].genes = copy.deepcopy(self.new_genomes[i].genes)
        return self.agent.genomes_to_do[0].genes

    def run_the_generation(self):
        for gen_obj in self.agent.genomes_to_do:
            self.agent.genome = copy.deepcopy(gen_obj.genes)
            try:
                gen_obj.fitness = self.run_genome()
            except (RecursionError, IndexError) as e:
                print(f"couldn't run the genome due to {e}")
                gen_obj.fitness = 0

        sorted_dic = {gen_obj.id: gen_obj.fitness for gen_obj in sorted(self.agent.genomes_to_do, key=lambda x: x.fitness, reverse=True)}
        top_two_ids = list(sorted_dic.keys())[:2]
        for gen_obj in self.agent.genomes_to_do:
            if gen_obj.id in top_two_ids:
                self.new_genomes.append(gen_obj)
            # maybe put a while loop here that randomly decides to perform crossover with random genomes in the population and mutation (until you have 10 genomes or smth)
        cross1, cross2 = self.crossover(self.new_genomes[0].genes,self.new_genomes[1].genes)
        crossgen1 = Genome()
        crossgen1.genes = cross1
        crossgen2 = Genome()
        crossgen2.genes = cross2
        self.new_genomes.append(crossgen1)
        self.new_genomes.append(crossgen2)
        mutated_genomes = []
        for j in range(0,3):
            # if no changes made don't append it maybe?
            mut = self.mutate(self.new_genomes[j].genes)
            mutated_genomes.append(mut)
        for item in mutated_genomes:
            mutgen = Genome()
            mutgen.genes = item
            self.new_genomes.append(mutgen)
        self.new_genomes.append(Genome())
        self.new_genomes.append(Genome())
        return

    def run_and_show(self):
        num_food = 30
        environment = Environment(num_food)
        environment.secret_agent.genome = self.run_the_generations()
        # print(environment.secret_agent.genome)
        # passing as both a genes and fitness
        # random.seed(rand_seed)

        # maybe throw a try/except here?
        parser = Parser(environment.secret_agent)
        environment.secret_agent.behaviour_tree = py_trees.trees.BehaviourTree(parser.parse_tree())

        "TODO: create smaller test environment? have small portion be hardcoded while others are all learning based upon those behaviours? how to do learning amongst all the agents with the other agents learning simultaneously"
        "TODO: it fails if max recursion depth is reached, ie. the genome runs out before it can finish parsing. FIX THI"
        i = 0
        for agent in environment.boids:
            print("Agent", i)
            i += 1
            evolve = Evolver(agent)
            try:
                agent.genome = evolve.run_the_generations()
                parser2 = Parser(agent)
                agent.behaviour_tree = py_trees.trees.BehaviourTree(parser2.parse_tree())
            except:
                environment.unused_agents += 1

        print("all agents done")
        pygame.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        clock = pygame.time.Clock()

        # print(py_trees.display.ascii_tree(environment.secret_agent.behaviour_tree.root))

        # i = 0
        # for _ in range(NUM_BOIDS):
        #     environment.boids[i].behaviour_tree = explore_tree(environment.boids[i])
        #     i += 1
        # for _ in range(30):
        #     environment.boids[i].behaviour_tree = flock_tree(environment.boids[i])
        #     i += 1
        print(environment.unused_agents)
        start = pygame.time.get_ticks()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                # run until all food collected
            if num_food == environment.nest.food:
                running = False
            if (pygame.time.get_ticks() - start) > 100000:
                running = False
            screen.fill((0, 0, 0))
            for spot in environment.foods:
                spot.show(screen)
            environment.nest.show(screen)
            for food_area in environment.food_areas:
                food_area.show(screen)
            for agent in environment.boids:
                agent.behaviour_tree.tick()
                agent.show(screen)
            environment.secret_agent.behaviour_tree.tick()
            environment.secret_agent.show(screen)
            pygame.display.flip()
            clock.tick(60)
        elapsed = pygame.time.get_ticks() - start
        # print(elapsed//10)
        pygame.quit()

environment = Environment(NUM_FOOD)
evolve_agent = Evolver(environment.secret_agent)

try:
    evolve_agent.run_and_show()
except IndexError:
    print("right here is the error")
