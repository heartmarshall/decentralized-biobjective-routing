import argparse
import time

from colorama import init, Fore, Style
init()

def parse_arguments():
    parser = argparse.ArgumentParser(description='Parse arguments for the program.')
    parser.add_argument('map_file_path', type=str, help='Path to the map file')
    parser.add_argument('start_node', type=int, help='ID of the start node')
    parser.add_argument('end_node', type=int, help='ID of the end node')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output')
    args = parser.parse_args()
    return args.map_file_path, args.start_node, args.end_node, args.verbose

def check_decentralization(pathfinding_algorithm: callable, decision_strategy_function: callable, map, start_node_id: int, end_node_id: int) -> bool:
    print(f'Start checking the decentralizability of the algorithm: {pathfinding_algorithm.__name__}')
    chosed_paths = []
    
    cur_node_id = start_node_id
    while cur_node_id != end_node_id:
        print(f'Started the search algorithm from the node with id: {cur_node_id}')
        all_solutions, _, _ = pathfinding_algorithm(map, cur_node_id)
        solutions = all_solutions[end_node_id]
        if len(solutions) == 0:
            raise(RuntimeError("The algorithm was unable to find solutions to the problem\n"
                               "Check the correctness of the algorithm and input data"))
        chosed_solution = decision_strategy_function(solutions)
        chosed_solution_number = 0
        print(f"Number of solutions found: {len(solutions)}")
        for sol_number in range(len(solutions)):
            if solutions[sol_number] == chosed_solution:
                chosed_solution_number = sol_number
            print(f'sol_№{sol_number}: {solutions[sol_number].path}')
        print(f"Out of all the solutions, the solution chosen is: {chosed_solution_number}")
        print(f"-----------------")

    for i in range(len(chosed_paths)-1):
        if chosed_paths[i][1:] != chosed_paths[i+1]:
            print(f"The proposed algorithm is not decentralized!")
            print(f"A mismatch is found on the following pair of paths:\n{chosed_paths[i]},\n{chosed_paths[i+1]}")
            return False
    print("The proposed algorithm worked truly decentralized")
    return True

def check_decentralization_verbose(pathfinding_algorithm: callable, decision_strategy_function: callable, map, start_node_id: int, end_node_id: int) -> bool:
    print(f'Checking algorithm: {pathfinding_algorithm.__name__}')
    first_solutions, _, _ = pathfinding_algorithm(map, start_node_id)
    chosed_solution = decision_strategy_function(first_solutions)
    print("->".join(chosed_solution.path))

    cur_node_id = start_node_id
    while cur_node_id != end_node_id:
        all_solutions, _, _ = pathfinding_algorithm(map, cur_node_id)
        solutions = all_solutions[end_node_id]
        if len(solutions) == 0:
            raise(RuntimeError("Cant find correct path"))
        chosed_solution = decision_strategy_function(solutions)
        chosed_solution_number = 0
        next_nodes = []
        for sol_number in range(len(solutions)):
            if solutions[sol_number] == chosed_solution:
                chosed_solution_number = sol_number
            next_nodes.append(solutions[sol_number])
        print(", ".join(next_nodes))
        print(f"{cur_node_id} -> {next_nodes[chosed_solution_number]}")
        