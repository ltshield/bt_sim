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

class Evolver:
    def __init__(self, agent):
        self.agent = agent

    # subtract by how long the behaviour tree is, how many nodes it has? simplest == better
    def fitness(self):
        self.agent.fitness = ()

    def mutate(self):
        i = 0
        for i in len(self.agent.genome):
            val = random.randint(0,100)
            if val < 25:
                self.agent.genome[0] = random.randint(0,10)
    
    def crossover(self):
        pass

    # find a way to normalize the two vectors to dimensionally-