from parser import *

def mutate(genes):
        i = 0
        for i in range(len(genes)):
            val = random.randint(0,100)
            # 25% chance of mutating
            if val < 25:
                genes[i] = random.randint(0,10)
        # self.new_genomes.append(genome)
        return genes
    
def crossover(genes1, genes2):
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

def evolution_algorithm(agent):
    pass

# should crossover occur with the agents' genomes that they touch?
# or should the genome just be given to them to deal with how their evolve algorithm works out? (ie. neighbor's genome is appended to a list of seen genomes of that agent vs. crossing over immediately)
# or maybe have crossover occur when new genome is shared but its appended as a new genome for agent to try out
# should they discard bad genomes from their list? would doing so cause it to converge? lower the solution space too much?

def __init__():
    pygame.init()
    num_food = 30
    environment = Environment(num_food)
    "TODO: create smaller test environment? have small portion be hardcoded while others are all learning based upon those behaviours? how to do learning amongst all the agents with the other agents learning simultaneously"
    "TODO: it fails if max recursion depth is reached, ie. the genome runs out before it can finish parsing. FIX THI"
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    start = pygame.time.get_ticks()
    running = True

    #redundant
    for agent in environment.boids:
        agent.curr_genome = [random.randint(0,10) for i in range(500)]
        parser = Parser(agent)
        try:
            agent.behaviour_tree = py_trees.trees.BehaviourTree(parser.parse_tree())
        except:
            pass

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # run until all food collected
        screen.fill((0, 0, 0))
        for spot in environment.foods:
            spot.show(screen)
        environment.nest.show(screen)
        for food_area in environment.food_areas:
            food_area.show(screen)
        for agent in environment.boids:
            # implement evolution algorithm here
            if agent.time_since_move == 10:
                agent.curr_genome = [random.randint(0,10) for i in range(500)]
                parser = Parser(agent)
                agent.time_since_move = 0
                try:
                    print("trying")
                    agent.behaviour_tree = py_trees.trees.BehaviourTree(parser.parse_tree())
                except Exception as e:
                    print(f"This one didn't work. due to {e}")
            elif agent.previous_position == agent.position:
                agent.time_since_move += 1
                print(f'{agent.id} time since move == {agent.time_since_move}')
            try:
                print("ticking")
                agent.behaviour_tree.tick()
            except:
                print(f"cannot tick for {agent.id}")
                pass
            for neighbor in (environment.boids):
                # make a function that handles the evolution as well as the shifting to a new genome if not being effective (not moving). Make sure it also creates a new behaviour tree for it to run (and deletes the old genome? or should we keep it around?)
                # do an evolutionary process that randomly mixes the genes around that have been found by the agent? Don't do crossover during the initial switch maybe?
                if check_collision(agent,neighbor) and agent == neighbor and agent.curr_genome not in neighbor.known_genomes:
                    gen1, gen2 = crossover(agent.curr_genome, neighbor.curr_genome)
                    agent.known_genomes.append(gen1)
                    print(len(agent.known_genomes))
                    neighbor.known_genomes.append(gen2)
                    print("oh their genomes are shared now")
            agent.previous_position = agent.position
            agent.show(screen)
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

__init__()