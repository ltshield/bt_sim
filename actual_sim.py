from bts_evolve import *
import copy

def evaluate_tree():
    pygame.init()
    num_food = 30
    i = 0
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
        environment.secret_agent.behaviour_tree.tick()    

    # to account for randomness affecting effectiveness?
    # not having random agent movements to differentiate them, I lowered the division factor by 10 to see bigger differences
    fitness = environment.nest.food * 10
    pygame.quit()
    return fitness

best_genome = [random.randint(0,10) for _ in range(500)]
best_fitness = 0

# maybe make it so that the agents return to the previous spot they were at before they found food to continue acting from there?
# implement that in a move_to function along with replenishing food spots? make it an option of where to go, to nest, to food spot, or to previous spot, or to random neighbor?)

#define the list of genomes outside and iterate through each of them, keeping the best one
genomes = [[random.randint(0,10) for _ in range(500)] for _ in range(25)]

# set the seed prior to all the simulations to see how well the agent does in helping the other population accomplish the task
rand_seed = random.randint(0,400)
# rand_food_list = [random.randint(0,(len(genome)-1)) for _ in range(10)]
# rand_neighbor_list = [random.randint(0,(len(genome)-1)) for _ in range(25)]

# keeping the random seed would then let us recreate the exact genome, tree, and runtime, would it be more effective to keep track of that instead?
while len(genomes) != 0:
    print(len(genomes))
    # genome = [random.randint(0,10) for _ in range(500)]
    genome = genomes.pop(0)
    # make sure to make a deepcopy of the genome, otherwise python passes it as a reference
    genome_copy = copy.deepcopy(genome)

    #then set the random seed after the genome initialization so that we don't get the same genome each time
    random.seed(rand_seed)
    try:
        num_food = 30
        environment = Environment(num_food)
        environment.secret_agent.genome = genome
        parser = Parser(environment.secret_agent)
        environment.secret_agent.behaviour_tree = py_trees.trees.BehaviourTree(parser.parse_tree())
        print(py_trees.display.ascii_tree(environment.secret_agent.behaviour_tree.root))
    except:
        print("genome failed, trying again")
        continue
    fitness= evaluate_tree()
    if fitness == "Error":
        continue
    if best_fitness < fitness:
        # print(f'{fitness} is faster than {best_fitness}')
        best_fitness = fitness
        best_genome = genome_copy
    # else:
        # print(f'{fitness} is not faster than {best_fitness}')
    # print(f'bf: {best_fitness}')
    # print(f'bg: {best_genome}')
    print(fitness)
    print(py_trees.display.ascii_tree(environment.secret_agent.behaviour_tree.root))

# print(f'bestgen = {best_genome[:10]}')
# run the best simulation
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
# random.seed(rand_seed)
num_food = 30
environment = Environment(num_food)
environment.secret_agent.genome = best_genome
parser = Parser(environment.secret_agent)
environment.secret_agent.behaviour_tree = py_trees.trees.BehaviourTree(parser.parse_tree())
print(py_trees.display.ascii_tree(environment.secret_agent.behaviour_tree.root))

i = 0
for _ in range(NUM_BOIDS):
    environment.boids[i].behaviour_tree = explore_tree(environment.boids[i])
    i += 1
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


#best of 20
"""
Here is the thing, the secret agent isn't going to be able to do anything unless he gets the perfect tree
Also, make sure there is a failsafe for if it is running on for too long (ie. secret agent picked up food but won't drop it so infinite loop)
reward actionable trees?
implement move_to's and replenishing food spots
     - change fitness function to amount of food gathered in determined amount of time
does current grammar allow agent to accomplish the task on its own in a variety of different ways or not?
how can I make it so that it does better at that?

bestgen = [5, 8, 8, 7, 1, 4, 4, 10, 4, 9]
{o} Selector
    --> Explore
    --> Flock
    --> Drop it

448
"""