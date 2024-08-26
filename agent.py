import py_trees
import pygame
import random

WIDTH, HEIGHT = 800, 600
NUM_BOIDS = 30
MAX_SPEED = 4
MAX_FORCE = 0.1
PERCEPTRON_RADIUS = 50

BOID_SIZE = 30

def check_collision(obj1, obj2):
    # print(f'{obj1} to {obj2}')
    dist = obj1.position.distance_to(obj2.position)
    if dist < obj1.radius or dist < obj2.radius:
        return True
    else:
        return False

class Agent:
    def __init__(self, environment, nest, color=(255,255,255)):
        # self.position = pygame.Vector2(random.uniform(0,WIDTH),random.uniform(0,HEIGHT))
        self.velocity = pygame.Vector2(random.uniform(-1,1),random.uniform(-1,1))
        self.velocity.scale_to_length(MAX_SPEED)
        self.acceleration = pygame.Vector2(0,0)
        self.radius = 5

        self.environment = environment
        self.nest = nest
        self.has_food = False
        # self.nest = nest
        self.position = pygame.Vector2(WIDTH//2,HEIGHT//2)
        self.color = color
        self.behaviour_tree = None
        self.genome = [random.randint(0,10) for _ in range(500)]
        self.fitness = 0
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
            if self != boid and self.position != boid.position and self.position.distance_to(boid.position) < PERCEPTRON_RADIUS:
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
            if self != boid and self.position != boid.position and self.position.distance_to(boid.position) < PERCEPTRON_RADIUS:
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
            if self != boid and self.position != boid.position and self.position.distance_to(boid.position) < PERCEPTRON_RADIUS:
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
    
    # should I just code it around, if it is over food, pick it up?
    # assume there are no food spots for now?
    # UNUSED FOR RIGHT NOW
    def go_to_food_spot(self):
        if len(self.food_spot) == 0:
            # print("No food spot found.")
            return False
        else:
            # print("going to food spot")
            return True

    def pick_up_food(self):
        for spot in self.environment.foods:
            if check_collision(self, spot):
                # print("pick up food")
                self.has_food = True
                self.environment.foods.remove(spot)
                return True
        for area in self.environment.food_areas:
            # print("here")
            if check_collision(self, area):
                return True
        else:
            # print("no food available")
            return False

    # are we just to code the specific behaviours/actions and not the 
    # condition statements? Like whether it returns true/false?

    def drop_food(self):
        if self.has_food and check_collision(self, self.nest):
            # print("dropping food")
            self.has_food = False
            self.nest.food += 1
            return True
        else:
            # print("no food to drop or not at nest")
            return False

    # UNUSED RIGHT NOW
    # or should the agent be allowed to eat food that it is carrying (more opportunity to explore)
    def eat_food(self):
        # should I create it so that the eat food function includes the agent returning to the nest in order to eat?
        if self.nest.food == 0 or check_collision(self.nest, self) == False:
            # print("no food to eat :( or not at nest")
            return False
        else:
            self.nest.food -= 1
            # print("eating food")
            return True

    # how do i make it so it continues repeating until it makes it to den
    def go_to_den(self):
        if check_collision(self.nest, self):
            return True
        direct = pygame.Vector2(0,0)
        direct += (self.nest.position - self.position).normalize()
        self.acceleration += direct
        self.update()
        return "RUNNING"

    def move_to(self, location):
        # print(location)
        if check_collision(location, self):
            return True
        elif location:
            direct = pygame.Vector2(0,0)
            direct += (location.position - self.position).normalize()
            self.acceleration += direct
            self.update()
            return "RUNNING"
        else:
            return False

    """
    TODO: write up the functions to create nest location, food spot locations,
        : and create the behaviour tree with each condition leading to an action
        : THEN, write up a grammar that creates a BT (and an FSM? one that 
        : can run from anywhere, like Prof said (all states are possible
        : starting states))
        : then code up an evolutionary algorithm + fitness function (amount 
        : of food collected in time, number of iterations)
        : figure out how to hardcode certain agents (percentage of population
        : are gatherers, others are explorers?) WHAT OTHER ROLES ARE THERE?
        : (are we then going to let it randomly assign conditions to actions?)
        : supposedly they should evolve to the needs of the population?
        : population is hardcoded, only one agent run by behaviour tree
        : then create fitness functions dependent upon whether they are
        : in a group or on their own (higher possibility of surviving on
        : own but lower chance of finding food), see what evolution occurs
        : we are trying to see what the agent evolves into
    """

    def check_if_food_spot(self):
        for area in self.environment.food_areas:
            if check_collision(self, area) == True:
                if area != self.environment.found_areas:
                    self.environment.found_areas.append(area)

    def update(self):
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