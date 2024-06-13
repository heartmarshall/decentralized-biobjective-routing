import math

from mosp_algo.graph import Graph
from mosp_algo.pareto_set import BiObjSolution, ParetoSet
from routing.bod_optimizations import bod_stage_1

def distance_to_line(point, line):
    x, y = point
    a, b = line
    distance = abs(a*x - y + b) / math.sqrt(a**2 + 1)
    return distance

def select_solution_from_pareto_set_mid(solutions_Pareto_set: ParetoSet, C1, C2) -> BiObjSolution:
    solutions = []
    for sol in solutions_Pareto_set.solutions:
        if sol.g1 <= C1 or sol.g2 <= C2:
            solutions.append(sol)
    solution_number = len(solutions) // 2
    if len(solutions) == 0:
        solutions = solutions_Pareto_set.solutions
    return sorted(sorted(solutions, key=lambda sol: distance_to_line(sol.solution_values, (1,0))))[solution_number]

def select_solution_from_pareto_set_min_g1(solutions_Pareto_set: ParetoSet, C1, C2) -> BiObjSolution:
    solutions = []
    min_g1 = solutions_Pareto_set.solutions[0].g1
    solution = solutions_Pareto_set.solutions[0]
    for sol in solutions_Pareto_set.solutions:
        min_g1 = min(min_g1, sol.g1)
        solution = sol
    return solution

def select_solution_from_pareto_set_min_g2(solutions_Pareto_set: ParetoSet, C1, C2) -> BiObjSolution:
    solutions = []
    min_g2 = solutions_Pareto_set.solutions[0].g2
    solution = solutions_Pareto_set.solutions[0]
    for sol in solutions_Pareto_set.solutions:
        min_g1 = min(min_g1, sol.g2)
        solution = sol
    return solution

def make_routing_table(network_graph: Graph, start_node, C1, C2):
    next_hop_table = {}
    start_node_neighbours = network_graph.get_neighbors(start_node)
    if len(start_node_neighbours) == 0:
        return next_hop_table # selected node has no output ports => no need to create a routing table
    for target in network_graph.adjacency_list:
        next_hop_table[target] = start_node_neighbours[0] # dummy plug
    
    # Stage #1: Reacheble_nodes - find all vertices reachable from start_node with total path cost less than given C_1, C_2.
    reacheble_nodes = bod_stage_1(network_graph, start_node, C1, C2).keys() ^ {start_node}
    for target in reacheble_nodes:
        solution = select_solution_from_pareto_set_mid(reacheble_nodes[target], C1, C2).solution_state
        next_hop_table[target][start_node] = solution.next_node_in_path
    
    return next_hop_table
