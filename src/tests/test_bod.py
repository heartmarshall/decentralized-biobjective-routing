import pytest
from mosp_algo.bod import bod
from mosp_algo.graph import Graph

@pytest.fixture
def cycle_graph():
    test_graph = Graph()
    test_graph.add_edge(1, 2, 1, 1)
    test_graph.add_edge(1, 4, 6, 6)
    test_graph.add_edge(2, 3, 1, 8)
    test_graph.add_edge(2, 1, 5, 1)
    test_graph.add_edge(3, 1, 1, 5)
    test_graph.add_edge(4, 3, 1, 1)
    return test_graph

@pytest.fixture
def simple_graph():
    test_graph = Graph()
    test_graph.add_edge(0, 2, 1, 5)
    test_graph.add_edge(0, 4, 5, 1)
    test_graph.add_edge(2, 3, 1, 4)
    test_graph.add_edge(2, 5, 1, 2)
    test_graph.add_edge(2, 5, 2, 1)
    test_graph.add_edge(4, 3, 1, 3)
    test_graph.add_edge(3, 1, 9, 3)
    test_graph.add_edge(4, 1, 2, 1)
    test_graph.add_edge(5, 1, 1, 1)
    return test_graph

def test_dijkstra_base_case(simple_graph):
    start_state = 0
    solutions = bod(simple_graph, start_state)
    assert len(solutions) == 6
    assert solutions[0].get_solutions(values=True) == {(0, 0)}
    assert solutions[2].get_solutions(values=True) == {(1, 5)}

def test_dijkstra_alternative_paths(simple_graph):
    start_state = 0
    solutions = bod(simple_graph, start_state)
    assert len(solutions) == 6
    assert solutions[1].get_solutions(values=True) == {(3, 8), (4, 7), (7, 2)}

def test_dijkstra_no_paths(simple_graph):
    start_state = 1
    solutions = bod(simple_graph, start_state)
    assert len(solutions) == 1 # Only one path - to stay in start node

def test_dijkstra_cycle_graph(cycle_graph):
    start_state = 1
    solutions = bod(cycle_graph, start_state)
    assert len(solutions) == 4
    assert solutions[3].get_solutions(values=True) == {(2, 9), (7, 7)}