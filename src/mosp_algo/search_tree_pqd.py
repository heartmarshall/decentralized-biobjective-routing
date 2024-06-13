from heapq import heapify, heappop, heappush
from typing import List, Optional, Set

class State:
    """
    Representation of a state in the search tree.

    Attributes:
        node: graph node associated with the state
        g1, g2: g-values of passing to the given state
        h1, h2: h-values of passing to the given state
        f1, f2: Values containing the sum of g and h values.
        parent: The parent state in the search tree.
    """

    def __init__(self, node, g1, g2, h1=0, h2=0, parent: Optional['State'] = None):
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
        self.parent = parent
        
    def __eq__(self, other: 'State'):

        if not isinstance(other, State):
            raise TypeError(f"Invalid comparison with object of class {other.__class__}")
        
        return (
            self.node == other.node and
            self.g1 == other.g1 and
            self.g2 == other.g2 and
            self.h1 == other.h1 and
            self.h2 == other.h2 and
            self.parent == other.parent
        )

    def __hash__(self) -> int:

        return hash((self.node, self.g1, self.g2, self.h1, self.h2, self.parent))

    def __lt__(self, other: 'State'):
        """
        Compares two states based on their total cost (f values).
        """
        if not isinstance(other, State):
            raise TypeError(f"Invalid comparison with object of class {other.__class__}")
        return (self.f1, self.f2) < (other.f1, other.f2)
    
    def is_dominates(self, other: 'State') -> bool:
        """
        Checks if the current state dominates another state (by f value).
        """
        if (self.f1 < other.f1 and self.f2 <= other.f2) or (self.f1 <= other.f1 and self.f2 < other.f2):
            return True
        return False
    
    def __str__(self) -> str:
        """
        Returns a string representation of the state.
        """
        return f"{self.node, self.f1, self.f2}"

def construct_path(node: State) -> List[State]:
    """
    Construct a path from the given search node to the root.

    Parameters:
        node (State): The end node of the path.

    Returns:
        List[State]: A list of search states representing the path from the root to the given node.
    """
    path = []
    while node is not None:
        path.append(node)
        node = node.parent
    return path[::-1]

class SearchTreePQD:
    """
    Priority queue-based search tree.
    """

    def __init__(self):
        self.open: List[State] = []
        self.closed: Set[State] = set()

    def __len__(self) -> int:
        return len(self.open) + len(self.closed)

    def open_is_empty(self) -> bool:
        return not self.open

    def add_to_open(self, state: State):
        """
        Adds a state to the open set. Lazy addition: checking that a path to a given node
        with the same price already exists is done when the state is expanded.
        """
        heappush(self.open, state)

    def get_best_node_from_open(self) -> Optional[State]:
        """
        Gets and removes the best state from the open set. Best = smallest f-values

        Returns:
        - State or None: The best state or None if the open set is empty.
        """
        while self.open:
            best_node = heappop(self.open)
            if not self.was_expanded(best_node):
                return best_node
        return None
    
    def remove_worse_states(self, f1: int, f2: int):
        """
        Clears the open set from states dominated by the specified f1, f2 values.
        """
        better_state = State(None, f1, f2)
        self.open = [state for state in self.open if not better_state.is_dominates(state)] 
        heapify(self.open)
    
    def add_to_closed(self, state: State):
        self.closed.add(state)

    def was_expanded(self, state: State) -> bool:
        return state in self.closed

    @property
    def opened(self):
        return self.open
