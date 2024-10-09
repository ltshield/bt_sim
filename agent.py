import py_trees
import pygame
import random
from copy import deepcopy

WIDTH, HEIGHT = 800, 600
# WIDTH, HEIGHT = 400, 300
NUM_BOIDS = 30
MAX_SPEED = 4
MAX_FORCE = 0.1
PERCEPTION_RADIUS = 50

BOID_SIZE = 30

GENOME_LENGTH = 750
NUM_FOOD = 30

def check_collision(obj1, obj2):
    dist = obj1.position.distance_to(obj2.position)
    if dist < obj1.radius or dist < obj2.radius:
        return True
    else:
        return False

class Genome:
    # right now just code the genome to handle the secret_agent running (only one agent at a time) so the evolver class can just keep track of the number of populations
    def __init__(self):
        self.genes = [random.randint(0,10) for _ in range(GENOME_LENGTH)]
        self.fitness = 0
        self.id = random.randint(0,100000)
        self.tree_created_and_checked = False
        # how sorted list/dictionary for fitness values?

class Agent:
    def __init__(self, environment, nest, color=(255,255,255)):
        # self.position = pygame.Vector2(random.uniform(0,WIDTH),random.uniform(0,HEIGHT))
        self.velocity = pygame.Vector2(random.uniform(-1,1),random.uniform(-1,1))
        self.velocity.scale_to_length(MAX_SPEED)
        self.acceleration = pygame.Vector2(0,0)
        self.radius = 5
        self.id = random.randint(0, 100000)

        self.previous_position = (0,0)
        self.time_since_move = 0

        self.genomes_to_do = [Genome() for _ in range(10)]
        
        self.curr_genome = deepcopy(self.genomes_to_do[0])
        self.new_genomes = []

        self.finished_genomes = []

        self.environment = environment
        self.nest = nest
        self.has_food = False
        # self.nest = nest

        # I AM GOING TO HAVE THEM START FROM ANYWHERE SO THEY DONT IMMEDIATELY SHARE THEIR FIRST GENOMES
        self.position = pygame.Vector2(random.randint(0,WIDTH),random.randint(0,HEIGHT))
        self.color = color
        self.behaviour_tree = None

        self.time_of_0_fitness = 0
        self.not_doing_anything = 0
        self.fitness = 0
        self.dropped_food = False

        # the environment is not constructed yet, I need to wait
        self.neighbors = None
        self.rand_food_list = None
        self.rand_neighbor_list = None

        self.food_index = 0
        self.neighbor_index = 0

        self.to_location = None

        best_genome = None
        all_genomes = []

    def edges(self):
        if self.position.x > WIDTH:
            self.position.x = 0
        elif self.position.x < 0:
            self.position.x = WIDTH
        if self.position.y > HEIGHT:
            self.position.y = 0
        elif self.position.y < 0:
            self.position.y = HEIGHT
        
    def align(self):
        # set the tuple for new direction of boid's next movement
        direct = pygame.Vector2(0,0)
        boids = self.environment.boids
        # add up the number of boids within radius to average result
        total = 0
        for boid in boids:
            # as long as not self and the boid is in position threshold
            if self != boid and self.position != boid.position and self.position.distance_to(boid.position) < PERCEPTION_RADIUS:
                # add the other positions to the direction (??) and add to total
                direct += boid.velocity
                total += 1
        if total > 0:
            # divide by total number of boids whose positions are included
            direct /= total
            # subtract by current position (??)
            direct -= self.velocity
            # normalize the new vector so we only have the unit vector
            direct = direct.normalize() * MAX_FORCE
        return direct
    
    def cohesion(self):
        boids = self.environment.boids
        direct = pygame.Vector2(0,0)
        total = 0
        for boid in boids:
            if self != boid and self.position != boid.position and self.position.distance_to(boid.position) < PERCEPTION_RADIUS:
                direct += boid.position
                total += 1
        if total > 0:
            direct /= total
            # why do you subtract your own position from the steering?
            direct -= self.position
            direct = direct.normalize() * MAX_FORCE
        return direct
    
    def separation(self):
        boids = self.environment.boids
        direct = pygame.Vector2(0,0)
        total = 0
        for boid in boids:
            if self != boid and self.position != boid.position and self.position.distance_to(boid.position) < PERCEPTION_RADIUS:
                diff = self.position - boid.position
                diff /= self.position.distance_to(boid.position)
                direct += diff
                total += 1
        if total > 0:
            direct /= total
            direct = direct.normalize() * MAX_FORCE
        return direct

    def flock(self):
        alignment = self.align()
        cohesion = self.cohesion()
        separation = self.separation()

        self.acceleration += separation
        self.acceleration += alignment
        self.acceleration += cohesion
        self.update()
        return True
    
    def explore(self):
        self.acceleration += self.separation()
        self.acceleration += pygame.Vector2(random.uniform(-1,1), random.uniform(-1,1))
        self.acceleration.scale_to_length(MAX_SPEED)
        self.update()
        return True
    
    # UNUSED FOR RIGHT NOW

    def go_to_food_spot(self):
        if len(self.food_spot) == 0:
            return False
        else:
            return True

    def pick_up_food(self):
        for spot in self.environment.foods:
            if check_collision(self, spot):
                self.has_food = True
                self.environment.foods.remove(spot)
                return True
        for area in self.environment.food_areas:
            if check_collision(self, area):
                return True
        else:
            return False

    def drop_food(self):
        if self.has_food and check_collision(self, self.nest):
            print("dropped food")
            self.has_food = False
            self.nest.food += 1
            self.dropped_food = True
            return True
        else:
            self.dropped_food = False
            return False

    # UNUSED RIGHT NOW
    def eat_food(self):
        if self.nest.food == 0 or check_collision(self.nest, self) == False:
            return False
        else:
            self.nest.food -= 1
            return True

    def go_to_den(self):
        if check_collision(self.nest, self):
            return True
        direct = pygame.Vector2(0,0)
        direct += (self.nest.position - self.position).normalize()
        self.acceleration += direct
        self.update()
        return "RUNNING"

    def determine_location(self, location):
        # it is still going to the same neighbor
        if location == "food_area":
            try:
                location = self.environment.food_areas[self.rand_food_list[self.food_index]]
                self.food_index += 1
            # location = random.choice(agent.environment.food_areas)
            except:
                self.food_index = 0
                location = self.environment.food_areas[self.rand_food_list[self.food_index]]
                self.food_index += 1
        elif location == "den":
            location = self.nest
        elif location == "neighbor":
            try:
                location = self.environment.boids[self.rand_neighbor_list[self.neighbor_index]]
                self.neighbor_index += 1
            except:
                self.neighbor_index = 0
                location = self.environment.boids[self.rand_neighbor_list[self.neighbor_index]]
                self.neighbor_index += 1
            # location = random.choice(agent.environment.boids)
        return location

    def move_to(self, location):
        if self.to_location == None:
            self.to_location = self.determine_location(location)
        if check_collision(self.to_location, self):
            self.to_location = None
            # print(f"moved to {location}")
            return True
        # elif location:
        elif self.to_location:
            direct = pygame.Vector2(0,0)
            direct += (self.to_location.position - self.position).normalize()
            self.acceleration += direct
            self.update()
            return "RUNNING"
        else:
            return False

    def check_if_food_spot(self):
        for area in self.environment.food_areas:
            if check_collision(self, area) == True:
                if area != self.environment.found_areas:
                    self.environment.found_areas.append(area)

    def update(self):
        self.edges()
        self.check_if_food_spot()
        self.velocity += self.acceleration
        if self.velocity.length() > MAX_SPEED:
            self.velocity.scale_to_length(MAX_SPEED)
        self.position += self.velocity
        self.acceleration *= 0

    def show(self, screen):
        # angle = self.velocity.angle_to(pygame.Vector2(1,0))
        # point1 = pygame.Vector2(0,-10).rotate(angle) + self.position
        # point2 = pygame.Vector2(-5,5).rotate(angle) + self.position
        # point3 = pygame.Vector2(5,5).rotate(angle) + self.position
        pygame.draw.circle(screen, self.color, self.position, self.radius)