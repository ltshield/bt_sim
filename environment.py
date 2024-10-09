from agent import *

class Environment:
    def __init__(self, num_food=1):
        self.nest = Nest()
        self.foods = [Food() for _ in range(num_food)]
        self.food_areas = [Food_Area() for _ in range(9)]
        self.boids = [Agent(self, self.nest) for _ in range(NUM_BOIDS)]
        self.secret_agent = Agent(self, self.nest, color=(255,125,125))
        self.found_areas = []
        self.unused_agents = 0

        for agent in self.boids:
            agent.neighbors = self.boids
            agent.rand_food_list = [random.randint(0,(len(agent.environment.food_areas)-1)) for _ in range(10)]
            agent.rand_neighbor_list = [random.randint(0,(len(agent.neighbors)-1)) for _ in range(25)]
        self.secret_agent.neighbors = self.boids
        self.secret_agent.rand_food_list = [random.randint(0,(len(self.secret_agent.environment.food_areas)-1)) for _ in range(10)]
        self.secret_agent.rand_neighbor_list = [random.randint(0,(len(self.secret_agent.neighbors)-1)) for _ in range(25)]

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
        self.radius = 5
    
    def update(self):
        pass

    def show(self, screen):
        pygame.draw.circle(screen, (255,0,255), ((self.position)), self.radius)

class Food_Area:
    def __init__(self):
        self.position = pygame.Vector2(random.uniform(0, WIDTH), random.uniform(0, HEIGHT))
        self.radius = random.randint(10, 30)
        # self.food_quantity = random.randin
    
    def show(self, screen):
        pygame.draw.circle(screen, (255,0,0), ((self.position)), self.radius)

# is this being used?
blackboard = py_trees.blackboard.Client(name="My Client")
blackboard.register_key(key="has_food", access=py_trees.common.Access.WRITE)
blackboard.register_key(key="is_tired", access=py_trees.common.Access.WRITE)
blackboard.register_key(key="found_food", access=py_trees.common.Access.WRITE)

# environment = Environment(num_food=20)
# print(environment.boids)