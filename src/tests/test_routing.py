import pytest
from mosp_algo.graph import Graph
from mosp_algo.pareto_set import BiObjSolution, ParetoSet

@pytest.fixture
def test_graph():
    test_graph = Graph()
    test_graph.read_from_file('test_graph_dbr.txt')
    return test_graph

def test_bi_obj_solution():
    solution1 = BiObjSolution(solution_state=0, solution_values=[6, 3])
    solution2 = BiObjSolution(solution_state=1, solution_values=[4, 2])

    assert solution1.dominates(solution2) is False
    assert solution2.dominates(solution1) is True
    assert solution1.is_dominated_by(solution2) is True
    assert solution2.is_dominated_by(solution1) is False
    assert solution1 != solution2
