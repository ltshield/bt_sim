from agent import *

class Environment:
    def __init__(self, num_food=25):
        self.nest = Nest()
        self.foods = [Food() for _ in range(num_food)]
        self.food_areas = [Food_Area() for _ in range(5)]
        self.boids = [Agent(self, self.nest) for _ in range(NUM_BOIDS)]
        self.secret_agent = Agent(self, self.nest, color=(255,125,125))
        self.found_areas = []

class Nest:
    def __init__(self):
        self.position = pygame.Vector2(WIDTH//2,HEIGHT//2)
        self.radius = 20
        self.food = 0

    def update(self):
        pass

    def show(self, screen):
        pygame.draw.circle(screen, (0,0, 255, 50), ((self.position)), self.radius)

class Food:
    def __init__(self):
        self.position = pygame.Vector2(random.uniform(0, WIDTH), random.uniform(0, HEIGHT))
        self.radius = 20
    
    def update(self):
        pass

    def show(self, screen):
        pygame.draw.circle(screen, (255,0,255), ((self.position)), self.radius)

class Food_Area:
    def __init__(self):
        self.position = pygame.Vector2(random.uniform(0, WIDTH), random.uniform(0, HEIGHT))
        self.radius = random.randint(10, 30)
        # should food spots disappear when all food has been gathered from them?
        # should they just replenish over time?
        # self.food_quantity = random.randin
    
    def show(self, screen):
        pygame.draw.circle(screen, (255,0,0), ((self.position)), self.radius)

# do we want them to change color based on what their action is?
# ie. blue ones are the exploring group that only explore
# purple are the flocking group that travel together?
# maybe have multiple flocking groups?
# they need to be all or nothing? or percentage chances of doing flocking vs exploring, see how evolution occurs in different percentage scenarios, # of agents, 
# size of food spots, number of food spots, etc.
# maybe work on implementing tiredness/eating food later? right now just see how the agent evolves to best help the population collect food the quickest
# is hardcoding referring to hardcoding the paths of the agents and the locations of the food so that randomness doesn't affect the resulting behaviour?
# or are we accepting that in an IRL scenario those things would of course be random, and the evolution would be environmentally / populationally dependent
# PROBABLY hard code the location of the food spots for each evolutionary process (not every generation but every run) 
# so as to find what works best for that particular layout, see how the resulting phenotype differs
# base it off of success at gathering all hardcoded food fast (one fitness function without replenishing food)
# then do it with a replenishing food function randomly placing more food as time goes on. test how good it is at finding and gathering that food when it appears
# (function based on how much time the food is allowed to be in the environment after spawning before being found, the sooner the better)
# and another function based on how much food can be gathered in the shortest amount of time (both randomly spawning, and spawning in specific "food spots" over time
# and a list of locations that spawns one food at next location over same interval of time to see what can finish the list fastest)
# then of course introduce more secret agents into the mix to see how they adapt to each other :) multiple evolutionary algorithms occurring in response to
# other evolutionary algorithms... more effective or less?
# should neighboring agents be able to share their effective genotypes with other agents in the population? should they all be trying to find an identical genotype
# that works for them all as a whole? or individual ones that work to fulfill their role in the population amongst other evolved agents?

# find a ratio of hardcoded agents to evolving ones to see what is most effective overall in random simulated environments

blackboard = py_trees.blackboard.Client(name="My Client")
blackboard.register_key(key="has_food", access=py_trees.common.Access.WRITE)
blackboard.register_key(key="is_tired", access=py_trees.common.Access.WRITE)
blackboard.register_key(key="found_food", access=py_trees.common.Access.WRITE)