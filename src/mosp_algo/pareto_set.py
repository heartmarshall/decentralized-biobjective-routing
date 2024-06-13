from abc import ABC, abstractmethod
from typing import List, Set, Tuple, Union
import matplotlib.pyplot as plt

class Solution(ABC):
    @abstractmethod
    def __init__(self, solution_values: List[float]):
        self.solution_values: Tuple[float, ...] = tuple(solution_values)

    @abstractmethod
    def dominates(self, other: 'Solution') -> bool:
        pass

    @abstractmethod
    def is_dominated_by(self, other: 'Solution') -> bool:
        pass

class BiObjSolution(Solution):
    """
    Class representing a bi-objective solution.
    """
    def __init__(self, solution_state, solution_values: List[float]):
        """
        Initialize a bi-objective solution with the given values.

        Parameters:
        - solution_values (list): List of objective values.
        """
        self.solution_state = solution_state
        self.solution_values = tuple(solution_values)
        self.g1 = solution_values[0]
        self.g2 = solution_values[1]

    def dominates(self, other: 'BiObjSolution') ->  bool:
        """
        Check if this solution dominates another.
        """
        return (self.g1 < other.g1 and self.g2 <= other.g2) or (self.g1 <= other.g1 and self.g2 < other.g2)
    
    def is_dominated_by(self, other: 'BiObjSolution'):
        return not self.dominates(other)

    def __str__(self):
        return f"({self.g1}, {self.g2})"

    def __hash__(self) -> int:
        return hash((self.g1, self.g2))

    def __repr__(self) -> str:
        return f"BiObjSolution([{self.g1}, {self.g2}])"

    def __eq__(self, other: 'BiObjSolution') -> bool:
        return isinstance(other, BiObjSolution) and self.g1 == other.g1 and self.g2 == other.g2


class ParetoSet:
    """
    Class representing a Pareto set in multi-objective optimization.
    """
    def __init__(self, SolutionClass=BiObjSolution):

        self.solutions = set()
        self.SolutionClass = SolutionClass
 
        # For visualization
        # self.max_g1 = 0
        # self.max_g2 = 0
        # self.all_solusions_ever = set()

    def add_solution(self, solution:Solution)->bool:
        """Add a solution to the Pareto set if it is non-dominated.

        Args:
            solution (Solution): A solution to be added to the Pareto set.

        Raises:
            ValueError: If the solution is not an instance of the specified SolutionClass.

        Returns:
            bool: True if the solution was added to the Pareto set, False otherwise.
        """
        if not isinstance(solution, self.SolutionClass):
            raise ValueError(f"This Pareto set can only handle solutions of class {self.SolutionClass}; A solution of class {solution.__class__} has been provided.")
        non_dominated = self.check_dominance(solution)

        # For visualization
        # self.all_solusions_ever.add(solution)
        # self.max_g1= max(self.max_g1, solution.solution_values[0])
        # self.max_g2 = max(self.max_g2, solution.solution_values[1])

        if non_dominated:
            self.solutions = {s for s in self.solutions if not solution.dominates(s)}
            self.solutions.add(solution)
            return True
        return False
    
    def remove_solution(self, solution: Solution) -> None:
        if not isinstance(solution, self.SolutionClass):
            raise ValueError(f"This Pareto set can only handle solutions of class {self.SolutionClass}; "
                             f"A solution of class {solution.__class__} has been provided.")
        self.solutions.remove(solution)

    def check_dominance(self, solution) -> bool:
        return not any(s.dominates(solution) for s in self.solutions)

    def get_solutions_dominated_by(self, solution)-> List[Solution]:
        return [s for s in self.solutions if solution.dominates(s)]

    def remove_worse(self, better_solution: Solution) -> None:
        """
        Remove all solutions that are dominated by a better solution.
        """
        dominated_solutions = self.get_solutions_dominated_by(better_solution)
        self.solutions.difference_update(dominated_solutions)

    def get_plot(self, color='blue', marker='o'):
        """
        Create a plot visualizing the Pareto set.
        
        Returns:
            plt.Figure: The matplotlib figure object representing the plot.
        """
        if not self.solutions:
            print("Empty Pareto set. Nothing to visualize.")
            return None

        fig, ax = plt.subplots()
        x_values, y_values = zip(*[(sol.g1, sol.g2) for sol in self.solutions])
        ax.scatter(x_values, y_values, label='Pareto Set', color=color, marker=marker, s=100, edgecolors='black')
        ax.set_xlabel('Objective 1')
        ax.set_ylabel('Objective 2')
        ax.set_title('Pareto Set Visualization')
        ax.grid(True, linestyle='--', which='both', alpha=0.7)
        return fig

    def __str__(self) -> str:
        return f"({', '.join(str(sol) for sol in self.solutions)})"

    def __contains__(self, solution: Solution):
        return solution in self.solutions
    
    def get_solutions(self, values: bool = False) -> Union[Set[Solution], Set[Tuple[float, float]]]:
        """
        Get all solutions in the Pareto set.

        Parameters:
        - values: If True, return only the objective values of the solutions.

        Returns:
        - Union[Set[Solution], Set[Tuple[float, float]]]: A set of solutions or their objective values.
        """
        if values:
            return {solution.solution_values for solution in self.solutions}
        return self.solutions