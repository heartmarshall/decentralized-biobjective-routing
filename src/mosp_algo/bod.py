from typing import Dict, List, Type
from mosp_algo.graph import Graph
from mosp_algo.pareto_set import ParetoSet, BiObjSolution
from mosp_algo.search_tree_pqd import SearchTreePQD, State
from collections import defaultdict

def bod(search_graph: Graph, start_node: int, search_tree_cls: Type[SearchTreePQD] = SearchTreePQD) -> Dict[int, ParetoSet]:
    """
    Bi-objective Dijkstra algorithm to find Pareto-optimal solutions set for each node.

    Parameters:
        search_graph (Graph): Graph to search.
        start_node (int): Starting node for the search.
        search_tree_cls (Type): Type of search tree to use (default: SearchTreePQD).

    Returns:
        Dict[int, ParetoSet]: Pareto-optimal solutions for all vertices of the search graph.
    """
    solutions: Dict[int, ParetoSet] = defaultdict(ParetoSet)
    g2_min: Dict[int, float] = defaultdict(lambda: float('inf'))
    start_state = State(node=start_node, g1=0, g2=0, parent=None)
    search_tree = search_tree_cls()
    search_tree.add_to_open(start_state)

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
                y = State(node=neighbour_node, g1=neighbour_g1, g2=neighbour_g2, parent=cur_state)
                if y.g2 >= g2_min[neighbour_node]:
                    continue
                search_tree.add_to_open(y)

    return solutions
