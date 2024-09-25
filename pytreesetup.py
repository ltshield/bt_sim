from environment import *

food_check = py_trees.common.ComparisonExpression(
    variable= "has_food",
    value = True,
    operator=lambda x, y: x == y
)

tired_check = py_trees.common.ComparisonExpression(
    variable= "is_tired",
    value = True,
    operator=lambda x, y: x == y
)

spot_check = py_trees.common.ComparisonExpression(
    variable= "found_food",
    value = True,
    operator=lambda x, y: x == y
)

# simulate a random choice function by having a list of random numbers (one for each random choice, ie neighbors and food spots cause of range)
# make it a list of random numbers with range of the indexes, (10 food spots range is 1-10), and then pop one of those each time that it is needed
# then the simulation will remain identical since the seed (which doesn't change) will recreate the same list as well later

class Move_to(py_trees.behaviour.Behaviour):
    def __init__(self, agent, location):
        super(Move_to, self).__init__(name=f"Move to {location}")
        self.agent = agent
        self.location = location

    def update(self):
        success = self.agent.move_to(self.location)
        if success == "RUNNING":
            return py_trees.common.Status.RUNNING
        elif success:
            return py_trees.common.Status.SUCCESS
        else:
            return py_trees.common.Status.FAILURE

class Go_den(py_trees.behaviour.Behaviour):
    def __init__(self, agent):
        super(Go_den, self).__init__(name="Go den")
        self.agent = agent

    def update(self):
        success = self.agent.go_to_den()
        if success == "RUNNING":
            return py_trees.common.Status.RUNNING
        elif success:
            return py_trees.common.Status.SUCCESS
        else:
            return py_trees.common.Status.FAILURE

# drop food, pick up, explore, flock
class Drop_it(py_trees.behaviour.Behaviour):
    def __init__(self, agent):
        super(Drop_it, self).__init__(name="Drop it")
        self.agent = agent

    def update(self):
        success = self.agent.drop_food()
        if success:
            return py_trees.common.Status.SUCCESS
        else:
            return py_trees.common.Status.FAILURE
        
class Pick_up(py_trees.behaviour.Behaviour):
    def __init__(self, agent):
        super(Pick_up, self).__init__(name="Pick up")
        self.agent = agent

    def update(self):
        success = self.agent.pick_up_food()
        if success:
            return py_trees.common.Status.SUCCESS
        else:
            return py_trees.common.Status.FAILURE

class Expl(py_trees.behaviour.Behaviour):
    def __init__(self, agent):
        super(Expl, self).__init__(name="Explore")
        self.agent = agent
    
    def update(self):
        success = self.agent.explore()
        if success:
            return py_trees.common.Status.SUCCESS
        else:
            return py_trees.common.Status.FAILURE

class Flo(py_trees.behaviour.Behaviour):
    def __init__(self, agent):
        super(Flo, self).__init__(name="Flock")
        self.agent = agent
    
    # should it return failure when there are no other agents around?

    def update(self):
        success = self.agent.flock()
        if success:
            return py_trees.common.Status.SUCCESS
        else:
            return py_trees.common.Status.FAILURE

class SpotCheck(py_trees.behaviour.Behaviour):
    def __init__(self, agent):
        super(SpotCheck, self).__init__(name="Spot Check")
        self.agent = agent
    
    def update(self):
        for spo in self.agent.environment.foods:
            if check_collision(spo, self.agent):
                return py_trees.common.Status.SUCCESS
        else:
            return py_trees.common.Status.FAILURE

class FoodCheck(py_trees.behaviour.Behaviour):
    def __init__(self, agent):
        super(FoodCheck, self).__init__(name="Food Check")
        self.agent = agent

    def update(self):
        if self.agent.has_food:
            return py_trees.common.Status.SUCCESS
        else:
            return py_trees.common.Status.FAILURE

# should explore/flock 

class Do_Nothing(py_trees.behaviour.Behaviour):
    def __init__(self, agent):
        super(Do_Nothing, self).__init__(name="Do nothing")
        self.agent = agent
    
    # should it return failure when there are no other agents around?

    def update(self):
        return py_trees.common.Status.FAILURE
