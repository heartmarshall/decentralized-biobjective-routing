from typing import Dict, Optional, Type
from mosp_algo.graph import Graph
from mosp_algo.pareto_set import BiObjSolution, ParetoSet
from mosp_algo.search_tree_pqd import SearchTreePQD, State
from collections import defaultdict


def bod_limited(search_graph: Graph, start_node: int, C1: float, C2: float, search_tree_cls: Type[SearchTreePQD] = SearchTreePQD) -> Dict[int, ParetoSet]:
    search_tree=SearchTreePQD
    solutions = defaultdict(ParetoSet)
    g2_min = defaultdict(lambda: float('inf'))
    start_node = State(node=start_node, g1=0, g2=0, parent=None)
    search_tree = search_tree()
    search_tree.add_to_open(start_node)

    while not search_tree.open_is_empty():
        cur_state = search_tree.get_best_node_from_open()  # Retrieve nodes in lexicographical order
        if cur_state.g2 >= g2_min[cur_state.node]:
            continue
        g2_min[cur_state.node] = cur_state.g2
        solutions[cur_state.node].add_solution(BiObjSolution(cur_state, (cur_state.g1, cur_state.g2)))
        for neighbour_node, costs in search_graph.get_neighbors(cur_state.node):
            for cost in costs:
                neighbour_g1 = cur_state.g1 + cost[0]
                neighbour_g2 = cur_state.g2 + cost[1]
                if neighbour_g2 >= g2_min[neighbour_node]:
                    continue
                if neighbour_g1 > C1 or neighbour_g2 > C2:
                    continue
                y = State(node=neighbour_node, g1=neighbour_g1, g2=neighbour_g2, parent=cur_state)
                search_tree.add_to_open(y)
    return solutions

# Stage #1: Reacheble_nodes - find all vertices reachable from start_node with total path cost less than given C_1, C_2
# Optimization - state store only first node in a path, not parent 
class StateStage_1(State):
    def __init__(self, node, g1, g2, h1=0, h2=0, next_node_in_path = None):
        """
        Initializes a node in the search tree.

        Parameters:
        - state: The state represented by the node.
        - g1, g2: Values of the cost function g from two sources.
        - h1, h2: Values of the heuristic function h from two sources.
        - parent: The parent node in the search tree.
        """
        self.node = node
        self.g1, self.g2 = g1, g2
        self.h1, self.h2 = h1, h2
        self.f1, self.f2 = self.g1 + self.h1, self.g2 + self.h2
        self.next_node_in_path = next_node_in_path
        

def bod_stage_1(search_graph: Graph, start_node: int, C1: float, C2: float, search_tree_cls: Type[SearchTreePQD] = SearchTreePQD) -> Dict[int, ParetoSet]:
    search_tree=SearchTreePQD
    solutions = defaultdict(ParetoSet)
    g2_min = defaultdict(lambda: float('inf'))
    start_node = StateStage_1(node=start_node, g1=0, g2=0, next_node_in_path=None)
    search_tree = search_tree()
    search_tree.add_to_open(start_node)

    while not search_tree.open_is_empty():
        cur_state = search_tree.get_best_node_from_open()  # Retrieve nodes in lexicographical order
        if cur_state.g2 >= g2_min[cur_state.node]:
            continue
        g2_min[cur_state.node] = cur_state.g2
        solutions[cur_state.node].add_solution(BiObjSolution(cur_state, (cur_state.g1, cur_state.g2)))
        
        for neighbour_node, costs in search_graph.get_neighbors(cur_state.node):
            for cost in costs:
                neighbour_g1 = cur_state.g1 + cost[0]
                neighbour_g2 = cur_state.g2 + cost[1]
                if neighbour_g2 >= g2_min[neighbour_node]:
                    continue
                if neighbour_g1 > C1 or neighbour_g2 > C2:
                    continue
                if cur_state == start_node:
                    next_node_in_path = neighbour_node
                else:
                    next_node_in_path = cur_state.next_node_in_path
                y = StateStage_1(node=neighbour_node, g1=neighbour_g1, g2=neighbour_g2, next_node_in_path=cur_state)
                search_tree.add_to_open(y)
    return solutions


# Stage #2: Possible senders - find all nodes from where packets can come to us given the constraints.
# Optimization - don't keep a record of the state's ancestor in state
class StateStage_2(State):
    def __init__(self, node, g1, g2, h1=0, h2=0):
        """
        Initializes a node in the search tree.

        Parameters:
        - state: The state represented by the node.
        - g1, g2: Values of the cost function g from two sources.
        - h1, h2: Values of the heuristic function h from two sources.
        - parent: The parent node in the search tree.
        """
        self.node = node
        self.g1, self.g2 = g1, g2
        self.h1, self.h2 = h1, h2
        self.f1, self.f2 = self.g1 + self.h1, self.g2 + self.h2

def bod_stage_2(search_graph: Graph, start_node: int, C1: float, C2: float, search_tree_cls: Type[SearchTreePQD] = SearchTreePQD) -> Dict[int, ParetoSet]:
    search_tree=SearchTreePQD
    solutions = defaultdict(ParetoSet)
    g2_min = defaultdict(lambda: float('inf'))
    start_node = StateStage_2(node=start_node, g1=0, g2=0)
    search_tree = search_tree()
    search_tree.add_to_open(start_node)

    while not search_tree.open_is_empty():
        cur_state = search_tree.get_best_node_from_open()  # Retrieve nodes in lexicographical order
        if cur_state.g2 >= g2_min[cur_state.node]:
            continue
        g2_min[cur_state.node] = cur_state.g2
        solutions[cur_state.node].add_solution(BiObjSolution(cur_state, (cur_state.g1, cur_state.g2)))
        
        for neighbour_node, costs in search_graph.get_neighbors(cur_state.node):
            for cost in costs:
                neighbour_g1 = cur_state.g1 + cost[0]
                neighbour_g2 = cur_state.g2 + cost[1]
                if neighbour_g2 >= g2_min[neighbour_node]:
                    continue
                if neighbour_g1 > C1 or neighbour_g2 > C2:
                    continue
                y = StateStage_2(node=neighbour_node, g1=neighbour_g1, g2=neighbour_g2)
                search_tree.add_to_open(y)
    return solutions


# Stage #3: Modeling - model the operation of each node from the possible senders 
# Optimization - store in each state not the ancestor, but the vertex following the cur node, if we have traversed the cur node.
class StateStage_3(State):
    def __init__(self, node, g1, g2, h1=0, h2=0, next_node = None):
        """
        Initializes a node in the search tree.

        Parameters:
        - state: The state represented by the node.
        - g1, g2: Values of the cost function g from two sources.
        - h1, h2: Values of the heuristic function h from two sources.
        - parent: The parent node in the search tree.
        """
        self.node = node
        self.g1, self.g2 = g1, g2
        self.h1, self.h2 = h1, h2
        self.f1, self.f2 = self.g1 + self.h1, self.g2 + self.h2
        self.next_node = next_node

def bod_stage_3(search_graph: Graph, start_node: int, C1: float, C2: float, target_node:int, search_tree_cls: Type[SearchTreePQD] = SearchTreePQD) -> Dict[int, ParetoSet]:
    search_tree=SearchTreePQD
    solutions = defaultdict(ParetoSet)
    g2_min = defaultdict(lambda: float('inf'))
    start_node = StateStage_3(node=start_node, g1=0, g2=0, next_node_in_path=None)
    search_tree = search_tree()
    search_tree.add_to_open(start_node)

    while not search_tree.open_is_empty():
        cur_state = search_tree.get_best_node_from_open()  # Retrieve nodes in lexicographical order
        if cur_state.g2 >= g2_min[cur_state.node]:
            continue
        g2_min[cur_state.node] = cur_state.g2
        solutions[cur_state.node].add_solution(BiObjSolution(cur_state, (cur_state.g1, cur_state.g2)))
        
        for neighbour_node, costs in search_graph.get_neighbors(cur_state.node):
            for cost in costs:
                neighbour_g1 = cur_state.g1 + cost[0]
                neighbour_g2 = cur_state.g2 + cost[1]
                if neighbour_g2 >= g2_min[neighbour_node]:
                    continue
                if neighbour_g1 > C1 or neighbour_g2 > C2:
                    continue
                if cur_state.node == target_node:
                    next_node = neighbour_node
                else:
                    next_node = cur_state.next_node
                y = StateStage_3(node=neighbour_node, g1=neighbour_g1, g2=neighbour_g2, next_node=next_node)
                search_tree.add_to_open(y)
    return solutions
