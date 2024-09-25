from bts_evolve import *

num_food = 30
screen = pygame.display.set_mode((WIDTH, HEIGHT))

environment = Environment(num_food)
i = 0
for _ in range(NUM_BOIDS):
    environment.boids[i].behaviour_tree = explore_tree(environment.boids[i])
    i += 1
# for _ in range(30):
#     environment.boids[i].behaviour_tree = flock_tree(environment.boids[i])
#     i += 1

start_time = pygame.time.get_ticks()

parser = Parser(environment.secret_agent)
environment.secret_agent.behaviour_tree = py_trees.trees.BehaviourTree(parser.parse_tree())
print(py_trees.display.ascii_tree(environment.secret_agent.behaviour_tree.root))

clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # run until all food collected
    if num_food == environment.nest.food:
        running = False
    
    screen.fill((0, 0, 0))

    """
    for boid in environment.boids:
        why do i need this first?
        boid.edges()

        implement these checks in the functions? how do i connect them
        without forcing the behaviour tree?
        code just the actions and leave the conditions to be found?
        cannot drop food if doesn't have food

        THIS COULD BE FOR THE HARDCODED AGENTS? create another agent instance, secret agent, colored differently that has to adjust for this?
        then adjust the hard coded solutions to create a flocking group and others that explore, then see what our secret agent does differently

        if boid.has_food and check_collision(boid, boid.nest) == False:
            boid.go_to_den()
        elif boid.has_food and check_collision(boid, boid.nest):
            boid.drop_food()
        elif boid.pick_up_food():
            pass
        else:
            val = random.randint(0,99)
            if val > 5:
                boid.flock(environment.boids)
            else:
                boid.explore()
        boid.update()
        boid.show()
    """
    
    for spot in environment.foods:
        spot.show(screen)
    environment.nest.show(screen)
    for agent in environment.boids:
        agent.behaviour_tree.tick()
        agent.show(screen)
    environment.secret_agent.behaviour_tree.tick()
    environment.secret_agent.show(screen)
    
    pygame.display.flip()
    clock.tick(60)
# except:
#     print("Error, genome ran out.")

elapsed_time = pygame.time.get_ticks() - start_time
print(f'Elapsed time: {elapsed_time}')
pygame.quit()