import pytest
from mosp_algo.pareto_set import BiObjSolution, ParetoSet

@pytest.fixture
def pareto_set():
    return ParetoSet()

def test_bi_obj_solution():
    solution1 = BiObjSolution(solution_state=0, solution_values=[6, 3])
    solution2 = BiObjSolution(solution_state=1, solution_values=[4, 2])

    assert solution1.dominates(solution2) is False
    assert solution2.dominates(solution1) is True
    assert solution1.is_dominated_by(solution2) is True
    assert solution2.is_dominated_by(solution1) is False
    assert solution1 != solution2

def test_pareto_set_add_solution(pareto_set):
    pareto_set.add_solution(BiObjSolution(0, [1, 2]))
    pareto_set.add_solution(BiObjSolution(1, [3, 4]))
    pareto_set.add_solution(BiObjSolution(2, [2, 3]))
    pareto_set.add_solution(BiObjSolution(3, [5, 1]))

    solutions = pareto_set.get_solutions()
    assert len(solutions) == 2

def test_pareto_set_remove_solution(pareto_set):
    solution_values_1 = (1, 4)
    solution_values_2 = (3, 2)
    pareto_set.add_solution(BiObjSolution(0, solution_values_1))
    pareto_set.add_solution(BiObjSolution(1, solution_values_2))
    pareto_set.remove_solution(BiObjSolution(1, solution_values_1))

    deleted_solution = BiObjSolution(solution_state=0, solution_values=solution_values_1)
    solutions = pareto_set.get_solutions()
    assert deleted_solution not in solutions
    assert len(solutions) == 1

def test_pareto_set_contains(pareto_set):
    solution1 = BiObjSolution(0, [1, 7])
    solution2 = BiObjSolution(0, [2, 5])

    pareto_set.add_solution(solution1)
    pareto_set.add_solution(solution2)

    assert solution1 in pareto_set
    assert solution2 in pareto_set
    assert BiObjSolution(3, [1, 4]) not in pareto_set

def test_pareto_set_remove_non_existent(pareto_set):
    solution = BiObjSolution(0, [1, 1])
    with pytest.raises(KeyError):
        pareto_set.remove_solution(solution)
