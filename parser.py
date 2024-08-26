from other_agents_trees import *

"""
GRAMMAR

<tree> ::= <node>
<node> ::= <selector> | <sequence> | <action> | <condition>

# should I hardcode them to be <condition><action>?

<sequence> ::= <children>
<selector> ::= <children>
<action> ::= <to_do>
<condition> ::= <cond>

<children> ::= <node> | <node> <children>

<to_do> ::= pick_up_food | drop_food_off | eat_food | explore | go_to(<location>)
<cond> ::= tired | knows_spot | has_food
<location> ::= den | food_spot

"""

class Parser:
    def __init__(self, agent):
        self.agent = agent
        self.children = []

    def parse_tree(self):
        return self.parse_node()
    
    def parse_node(self):
        # print("parsing node")
        val = self.agent.genome.pop(0) % 4
        if val == 0:
            return self.parse_sequence()
        elif val == 1:
            return self.parse_selector()
        elif val == 2:
            return self.parse_to_do()
        elif val == 3:
            return self.parse_cond()
        else:
            print("Nope you messed up.")
    
    def parse_sequence(self):
        # print("parsing sequence")
        children = self.parse_children()
        sequence_node = py_trees.composites.Sequence(name="Sequence", memory=True)
        sequence_node.add_children(children)
        return sequence_node
    
    def parse_selector(self):
        # print("parse selector")
        children = self.parse_children()
        # self.expect(")")
        selector_node = py_trees.composites.Selector(name="Selector", memory=True)
        selector_node.add_children(children)
        return selector_node

    def parse_to_do(self):
        # print("parse_to_do")
        val = self.agent.genome.pop(0)
        if val % 5 == 0:
            return Pick_up(agent=self.agent)
        elif val % 5 == 1:
            return Drop_it(agent=self.agent)
        elif val % 5 == 2:
            return Flo(agent=self.agent)
        elif val % 5 == 3:
            return Expl(agent=self.agent)
        elif val % 5 == 4:
            location = self.parse_location()
            # print(f'Move_to(agent, {location})')
            agent = self.agent
            return Move_to(agent, location)

    def parse_location(self):
        val = self.agent.genome.pop(0)
        if val % 3 == 0:
            return "den"
        elif val % 3 == 1:
            return "neighbor"
        elif val % 3 == 2:
            return "food_area"

    def parse_cond(self):
        # print("parsing cond")
        val = self.agent.genome.pop(0)
        if val % 2 == 0:
            return FoodCheck(agent=self.agent)
        elif val % 2 == 1:
            return SpotCheck(agent=self.agent)
        # else:
        #     return "tired"

    """ 
        def parse_child(self):
            print("parsing children")
            # make it so multiple children or 1 child is possible
            val = self.agent.genome.pop(0) % 2
            if val == 0:
                return self.parse_children()
            elif val == 1:
                return "done"
        
        def parse_children(self):
            if len(self.agent.genome) == 0:
                return "INVALID, no more space"
            children = []
            child = self.parse_node()
            children.append(child)
            more = self.parse_child()
            if child == "done":
                return children
            else:
                children.append(more)
                return self.parse_children()
    """

    def parse_children(self):
        val = self.agent.genome.pop(0) % 5
        # if val == 0:
        #     children = [self.parse_node()]
        #     return children
        # limit it to a condition -> action combo?
        if val == 0:
            children = [self.parse_cond(), self.parse_to_do()]
            return children
        elif val == 1:
            children = [self.parse_cond(), self.parse_to_do(), self.parse_to_do()]
            return children
        elif val == 2:
            children = [self.parse_cond(), self.parse_cond(), self.parse_to_do()]
            return children
        elif val == 3:
            children = [self.parse_to_do(), self.parse_to_do(), self.parse_to_do()]
            return children
        elif val == 4:
            children = [self.parse_to_do(), self.parse_cond(), self.parse_to_do()]
            return children
        # should it end on self.parse_cond() in any instance?