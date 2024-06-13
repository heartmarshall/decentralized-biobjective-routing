import math

from mosp_algo.graph import Graph
from bod_optimizations import bod_limited, bod_stage_1, bod_stage_2, bod_stage_3
from mosp_algo.pareto_set import BiObjSolution, ParetoSet, Solution
from mosp_algo.search_tree_pqd import SearchTreePQD, State

def reverse_graph(graph: Graph, costs_matter=True):
    reverse_graph = Graph()
    for start_node in graph.adjacency_list:
        for end_node in graph.adjacency_list[start_node]:
            if costs_matter:
                for cost in graph.adjacency_list[start_node][end_node]:
                    reverse_graph.add_edge(end_node, start_node, cost[0], cost[1])
            else:
                reverse_graph.add_edge(end_node, start_node, 1, 1)
   
def distance_to_line(point, line):
    x, y = point
    a, b = line
    distance = abs(a*x - y + b) / math.sqrt(a**2 + 1)
    return distance

def select_solution_from_pareto_set(solutions_Pareto_set: ParetoSet, C1, C2) -> BiObjSolution:
    solutions = []
    for sol in solutions_Pareto_set.solutions:
        if sol.g1 <= C1 or sol.g2 <= C2:
            solutions.append(sol)
    solution_number = len(solutions) // 2
    if len(solutions) == 0:
        solutions = solutions_Pareto_set.solutions
    return sorted(sorted(solutions, key=lambda sol: distance_to_line(sol.solution_values, (1,0))))[solution_number]

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
        solution = select_solution_from_pareto_set(reacheble_nodes[target], C1, C2).solution_state
        next_hop_table[target][start_node] = solution.next_node_in_path
    
    # Stage #2: Possible senders - find all nodes from where packets can come to us given the constraints.
    reverse_network_graph = reverse_graph(network_graph, costs_matter=False)
    possible_predecessors = list(bod_stage_2(reverse_network_graph, start_node).keys())

    # Stage #3: Modeling - model the operation of each node from the possible senders 
    for sender in possible_predecessors:
        sender_reacheble_nodes = bod_stage_3(network_graph, sender, C1, C2)
        for target in sender_reacheble_nodes:
            if target == start_node:
                continue
            solution_state = select_solution_from_pareto_set(reacheble_nodes[target], C1, C2).solution_state
            next_hop_table[target][sender] = solution_state.next_node
    
    # Stage #4: Route table optimization
    if len(possible_predecessors) == 0:
        return next_hop_table
    
    for target in next_hop_table:
        next_hops = set()
        for sender in possible_predecessors[1:]:
            next_hops.add(next_hop_table[target][sender])
        next_hops = next_hops.discard(None)
        if len(next_hops) == 1:
            next_hop_table[target] = next_hops.pop()
    
    return next_hop_table
