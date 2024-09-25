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


NUM_FOOD = 30
environment = Environment(NUM_FOOD)
for agent in environment.boids:
    parser = Parser(agent)
    agent.behaviour_tree = py_trees.trees.BehaviourTree(parser.parse_tree())


running = True
while running:
    for agent in environment.boids:
        # switch genomes when not moving / accomplishing anything
        # print(agent.time_since_move)
        if agent.time_since_move > 45:
            print(f'{agent.id} hasn"t moved in {agent.time_since_move} so switching genome')
            #change genome! perform evolutionary operations
            agent.genomes_done.append(agent.curr_genome)
            # should we assign fitness values to them?
            if len(agent.known_genomes) != 0:
                agent.curr_genome = agent.known_genomes.pop(0)
                parser = Parser(agent)
                agent.behaviour_tree = py_trees.trees.BehaviourTree(parser.parse_tree())
            agent.time_since_move = 0
        # also switch genomes when having not accomplished anything new recently? or just after a time threshold
        for neighbor in environment.boids:
            if neighbor != agent:
                if check_collision(agent, neighbor):
                    if neighbor.curr_genome not in agent.known_genomes:
                        print(f"sharing genome! {agent.id} and {neighbor.id}")
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
    for agent in environment.boids:
        # print(f'before tick {agent.position}')
        agent.previous_position = deepcopy(agent.position)
        agent.behaviour_tree.tick()
        # print(f'after tick {agent.position}')
        if agent.previous_position == agent.position:
            # print("the positions were the same")
            agent.time_since_move += 1
        agent.show(screen)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()