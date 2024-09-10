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
# having a global seed keeps the simulations the same through every generation
# making it a local seed that just lasts for the generation might be the best way to prevent a random best fitness

# environment = Environment(NUM_FOOD)

class Evolver:
    def __init__(self, agent):
        self.rand_seed = random.randint(0,400)
        random.seed = self.rand_seed
        self.agent = agent
        # make it the same for each generation? or change after each generation (more general solution)?
        # self.genomes = [Genome(self.agent) for x in range(50)]

    # subtract by how long the behaviour tree is, how many nodes it has? simplest == better
    # def fitness(self):
    #     self.agent.fitness = ()

    # def mutate(self):
    #     i = 0
    #     for i in len(self.agent.genome):
    #         val = random.randint(0,100)
    #         if val < 25:
    #             self.agent.genome[0] = random.randint(0,10)
    
    # def crossover(self):
    #     pass

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
        for gen in self.agent.genomes_to_do:
            # print(gen.genes)
            self.agent.genome = copy.deepcopy(gen.genes)
            # print(self.agent.genome)
            try:
                gen.fitness = self.run_genome()
            except:
                gen.fitness = 0
        best_fitness = 0
        best_genome = []
        # sorted list based on fitness value?
        for gen in self.agent.genomes_to_do:
            print(gen.fitness)
            if gen.fitness > best_fitness:
                best_genome = gen.genes
                best_fitness = gen.fitness
        return best_genome
    
    def run_and_show(self):
        num_food = 30
        environment = Environment(num_food)
        environment.secret_agent.genome = self.run_population()
        # passing as both a genes and fitness
        # random.seed(rand_seed)
        parser = Parser(environment.secret_agent)
        environment.secret_agent.behaviour_tree = py_trees.trees.BehaviourTree(parser.parse_tree())

        "TODO: create smaller test environment? have small portion be hardcoded while others are all learning based upon those behaviours? how to do learning amongst all the agents with the other agents learning simultaneously"
        i = 0
        for agent in environment.boids:
            print("Agent", i)
            i += 1
            evolve = Evolver(agent)
            agent.genome = evolve.run_population()
            parser2 = Parser(agent)
            agent.behaviour_tree = py_trees.trees.BehaviourTree(parser2.parse_tree())

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

evolve_agent.run_and_show()

# i need to 
