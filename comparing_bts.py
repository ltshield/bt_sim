from parser import *

NUM_FOOD = 0
environment = Environment(NUM_FOOD)
agent1 = environment.boids[0]
agent2 = environment.boids[1]

# agent1.curr_genome.genes = agent1.curr_genome.genes[:100]
# agent2.curr_genome.genes = agent2.curr_genome.genes[:100]
print(agent1.curr_genome.genes[:20])
print(agent2.curr_genome.genes[:20])

parser1 = Parser(agent1)
agent1.behaviour_tree = py_trees.trees.BehaviourTree(parser1.parse_tree())

parser2 = Parser(agent2)
agent2.behaviour_tree = py_trees.trees.BehaviourTree(parser2.parse_tree())

print("AGENT 1 BEHAVIOUR TREE")
print(py_trees.display.ascii_tree(agent1.behaviour_tree.root))

print("AGENT 2 BEHAVIOUR TREE")
print(py_trees.display.ascii_tree(agent2.behaviour_tree.root))


############################################################################
#                           DEPTH METRIC                                   #
############################################################################

def calculate_depth(node):
    if not hasattr(node, "children") or not node.children:
        return 1  # A leaf node has depth 1
    return 1 + max(calculate_depth(child) for child in node.children)

agent1depth = calculate_depth(agent1.behaviour_tree.root)
agent2depth = calculate_depth(agent2.behaviour_tree.root)
print(f"Depth of agent1 tree: {agent1depth}")
print(f"Depth of agent2 tree: {agent2depth}")


############################################################################
#                        MAX BREADTH METRIC                                #
############################################################################

from collections import deque

def calculate_breadth(node):
    if not hasattr(node, "children") or not node.children:
        return 1  # A single node has a breadth of 1
    
    queue = deque([node])
    max_breadth = 0
    
    while queue:
        level_size = len(queue)
        max_breadth = max(max_breadth, level_size)
        
        # Traverse the current level and add the children to the queue
        for _ in range(level_size):
            current_node = queue.popleft()
            if hasattr(current_node, "children"):
                queue.extend(current_node.children)
    
    return max_breadth

agent1width = calculate_breadth(agent1.behaviour_tree.root)
agent2width = calculate_breadth(agent2.behaviour_tree.root)

print(f'Width of agent1 tree: {agent1width}')
print(f'Width of agent2 tree: {agent2width}')

#########################################################
#             NODE CHECKS  (w/ recursion)               #
#########################################################

def check_node(node, node_dict):
    node_dict[node.name] += 1
    if not node.children:
        return node_dict
    else:
        node_dict = check_node(node, node_dict)
        return node_dict

def check_nodes(node):

    # init node dictionary
    node_dict = {
        'Move to food_area': 0,
        'Move to neighbor': 0,
        'Move to den': 0,
        'Do nothing': 0,
        'Food Check': 0,
        'Spot Check': 0,
        'Flock': 0,
        'Explore': 0,
        'Pick up': 0,
        'Drop it': 0,
        'Go den': 0,
        'Sequence': 0,
        'Selector': 0
    }

    node_dict = check_node(node, node_dict)

    return node_dict

# print()
# print()

# agent1_dict = check_nodes(agent1.behaviour_tree.root)
# print("AGENT 1 DICT VALUES")
# for key,value in agent1_dict.items():
#     print(f'Node name: {key}, Frequency: {value}')

# print()
# print()
# agent2_dict = check_nodes(agent2.behaviour_tree.root)
# print("AGENT 2 DICT VALUES")
# for key,value in agent2_dict.items():
#     print(f'Node name: {key}, Frequency: {value}')

#########################################################
#             NODE CHECKS  (w/ stacks)                  #
#########################################################

def check_nodes_stack(node):

    # init node dictionary
    node_dict = {
        'Move to food_area': 0,
        'Move to neighbor': 0,
        'Move to den': 0,
        'Do nothing': 0,
        'Food Check': 0,
        'Spot Check': 0,
        'Flock': 0,
        'Explore': 0,
        'Pick up': 0,
        'Drop it': 0,
        'Sequence': 0,
        'Selector': 0
    }

    node_dict = check_node_stack(node, node_dict)

    return node_dict

def check_node_stack(node, node_dict):
    stack = [node]
    
    while stack:
        current_node = stack.pop()

        node_dict[current_node.name] += 1

        if hasattr(current_node, "children"):
            stack.extend(current_node.children)
    
    return node_dict

print()
print()

agent1_dict = check_nodes_stack(agent1.behaviour_tree.root)
print("AGENT 1 DICT VALUES")
for key,value in agent1_dict.items():
    print(f'Node name: {key}, Frequency: {value}')

print()
print()

agent2_dict = check_nodes_stack(agent2.behaviour_tree.root)
print("AGENT 2 DICT VALUES")
for key,value in agent2_dict.items():
    print(f'Node name: {key}, Frequency: {value}')

# increment based on number of actions? decrement based on number of inactions? ie. do nothings?
agent1_fitness = 0
for key in agent1_dict.keys():
    if key in ["Move to food_area", "Move to neighbor", "Move to den", "Explore", "Pick up", "Drop it", "Flock"]:
        agent1_fitness += agent1_dict[key]
agent1_fitness -= agent1_dict["Do nothing"] // 2
print(agent1_fitness)

agent2_fitness = 0
for key in agent2_dict.keys():
    if key in ["Move to food_area", "Move to neighbor", "Move to den", "Explore", "Pick up", "Drop it", "Flock"]:
        agent2_fitness += agent2_dict[key]
agent2_fitness -= agent2_dict["Do nothing"] // 2
print(agent2_fitness)



