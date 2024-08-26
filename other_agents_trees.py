from pytreesetup import *

def explore_tree(agent):
    explore = Expl(agent=agent)
    flock = Flo(agent=agent)
    pick_up = Pick_up(agent=agent)
    go_den = Go_den(agent=agent)
    drop_it = Drop_it(agent=agent)
    food_cond = FoodCheck(agent=agent)
    spot_cond = SpotCheck(agent=agent)

    root = py_trees.composites.Selector("All Selector", memory=False)
    food_node = py_trees.composites.Sequence("Food Node", memory=False)
    spot_node = py_trees.composites.Sequence("Spot Node", memory=False)
    food_node.add_children([food_cond,go_den,drop_it])
    spot_node.add_children([spot_cond, pick_up])

    root.add_children([food_node, spot_node, explore])

    return py_trees.trees.BehaviourTree(root)

def flock_tree(agent):
    explore = Expl(agent=agent)
    flock = Flo(agent=agent)
    pick_up = Pick_up(agent=agent)
    go_den = Go_den(agent=agent)
    drop_it = Drop_it(agent=agent)
    food_cond = FoodCheck(agent=agent)
    spot_cond = SpotCheck(agent=agent)

    root = py_trees.composites.Selector("All Selector", memory=False)
    food_node = py_trees.composites.Sequence("Food Node", memory=False)
    spot_node = py_trees.composites.Sequence("Spot Node", memory=False)
    food_node.add_children([food_cond,go_den,drop_it])
    spot_node.add_children([spot_cond, pick_up])

    root.add_children([food_node, spot_node, flock])

    return py_trees.trees.BehaviourTree(root)