from collections import defaultdict
from typing import Any, Dict, List, Tuple


class Graph:
    """
    Represents an directed graph with weighted edges.

    Attributes:
        adjacency_list: A defaultdict containing vertices as keys and dictionaries of neighbors and their costs as values.
    """

    def __init__(self):
        self.adjacency_list: Dict[Any, Dict[Any, List[Tuple[float, float]]]] = defaultdict(dict)

    def add_edge(self, vertex1, vertex2, cost1, cost2) -> None:
        """
        Adds an edge to the graph.

        Parameters:
        - vertex1: first vertex of the edge.
        - vertex2: second vertex of the edge.
        - cost1: cost of edge from vertex1 to vertex2.
        - cost2: cost of edge from vertex2 to vertex1.
        """
        if vertex2 not in self.adjacency_list[vertex1]:
            self.adjacency_list[vertex1][vertex2] = []
            
        self.adjacency_list[vertex1][vertex2].append((cost1, cost2))

    def read_from_file(self, file_path: str) -> None:
        """
        Reads graph data from a file and updates the graph.

        Parameters:
        - file_path: Path to the file containing graph data in the format: vertex1 vertex2 cost1 cost2.
        """
        self.reset()
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    parts = line.split()
                    if len(parts) != 4:
                        continue
                    vertex1, vertex2, cost1, cost2 = parts
                    self.add_edge(int(vertex1), int(vertex2), float(cost1), float(cost2))
        except FileNotFoundError:
            print(f"File {file_path} not found.")
        except Exception as e:
            print(f"Error reading from file {file_path}: {e}")

    def get_neighbors(self, node) -> List[Tuple[Any, List[Tuple[float, float]]]]:
        """
        Gets the neighbors and their costs of a given vertex.
        """
        if node not in self.adjacency_list:
            return []
        return list(self.adjacency_list[node].items())
    
    def reset(self):
        self.adjacency_list = defaultdict(dict)
        
    def get_edges(self) -> List[Tuple[Any, Any, List[Tuple[float, float]]]]:
        """
        Returns all the edges in the graph with their costs.

        Returns:
        - A list of tuples containing vertex pairs and their associated costs.
        """
        edges = []
        for vertex, neighbors in self.adjacency_list.items():
            for neighbor, costs in neighbors.items():
                edges.append((vertex, neighbor, costs))
        return edges
    
    def __str__(self) -> str:
        result = ["Graph:"]
        for vertex, neighbors in self.adjacency_list.items():
            for neighbor, costs in neighbors.items():
                costs_str = ', '.join(f"({c1}, {c2})" for c1, c2 in costs)
                result.append(f"{vertex} -> {neighbor} : {costs_str}")
        return '\n'.join(result)

    @property
    def vertices(self) -> List[Any]:
        return self.adjacency_list.keys()
