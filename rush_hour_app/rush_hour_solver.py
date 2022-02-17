"""
File: rush_hour_solver.py
Author: John Pignato
Date: Feb 16, 2022

TLDR:
Finds the shorest path to victory given any rush hour game board

Explaination:
This app solves any rush hour board that adheres to the specified csv format.
It uses a the A* algorithm to find the shortest path to victory and makese use
of a customer min heap and graph to solve the problem.
"""
try:
    import os
    import json
    import copy
    import random
    from datetime import datetime
    from helpers.graph import Graph
    from helpers.heap import Heap
    from collections import namedtuple
except ImportError as e:
    print(e)
    exit(1)

#Position cars leftmost side needs to reach to win game
GOAL_POS = (2,4)
#ID of the goal car
GOAL_CAR_ID = None
#Hashmap that holds all initial car information
cars = {}
#Quasi-structs...classes too bulky
car = namedtuple('Car', ['x_pos', 'y_pos', 'direction', 'len', 'goal_car'])
queue_entry = namedtuple('Entry', ['unique_id', 'history'])
move_tuple = namedtuple('Move', ['grid_string', 'move_val'])

def init_represent(csv_contents: str)->list:
    """
    Creates the matrix which represents the starting position of the board.
    CSV MUST ADHERES TO STRICT FORMAT:
        Each file’s first line will be the dimensions of the board. Each remaining line describes a
        car/truck which has been placed on the board.
        Each line describing a car/truck has the following elements (separated by commas):
            1. A unique ID (Integer)
            2. The upper left X-coordinate of the car on the grid. (Integer)
            3. The upper left Y-coordinate of the car on the grid. (Integer)
            4. A V or H indicating that the car/truck is horizontal or vertical. (String)
            5. The length of the car. (Integer)
            6. A T or F indicating if the car is the goal car (T means it is the goal car). (String)

    Args:
        csv_contents (str): contents of a given csv file

    Returns:
        list: matrix representation of board
    """
    global GOAL_CAR_ID, cars
    demensions = csv_contents[0].split(',')
    #create -1 matrix
    grid = [[-1 for i in range(int(demensions[0]))] for i in range(int(demensions[1]))]
    for automobile in csv_contents[1:]:
        info = automobile.split(',')
        if len(info) <= 1:
            continue
        name_of_car = int(info[0])
        if info[5].strip() == 'T':
            GOAL_CAR_ID = name_of_car
        #namedtuple car
        cars[name_of_car] = car(int(info[1]), int(info[2]), info[3], int(info[4]), (True if info[5] == 'T' else False))

        #add cars to matrix
        for i in range(cars[name_of_car].len):
            if cars[name_of_car].direction == 'V':
                grid[cars[name_of_car].y_pos + i][cars[name_of_car].x_pos] = name_of_car
            else:
                grid[cars[name_of_car].y_pos][cars[name_of_car].x_pos + i] = name_of_car

    return grid


def stringify_grid(grid:list)->str:
    """
    Creates matrix "fingerprint"

    Args:
        grid (list): a board state matrix

    Returns:
        str: str repr of board state
    """
    return json.dumps(grid)

def listify_grid(grid:str)->list:
    """
    dumps matrix "fingerprint" to matrix

    Args:
        grid (str): str repr of board state

    Returns:
        list: a board state matrix
    """
    return json.loads(grid)


def shift_car_left(car_id: str, pos: tuple, grid: list)->str:
    """
    Shifts a car left on board

    Args:
        car_id (str): ID of car
        pos (tuple): col and row indexs
        grid (list): a board state

    Returns:
        str: a "fingerprint" of new board state
    """
    old_end_pos = (pos[1] + cars[car_id].len)-1
    grid[pos[0]][pos[1]-1] = car_id
    grid[pos[0]][old_end_pos] = -1
    return stringify_grid(grid)

def shift_car_right(car_id: str, pos: tuple, grid: list)->str:
    """
    Shifts a car right on board

    Args:
        car_id (str): ID of car
        pos (tuple): col and row indexs
        grid (list): a board state

    Returns:
        str: a "fingerprint" of new board state
    """
    grid[pos[0]][pos[1]] = -1
    grid[pos[0]][pos[1] + cars[car_id].len] = car_id
    return stringify_grid(grid)

def shift_car_down(car_id: str, pos: tuple, grid: list)->str:
    """
    Shifts a car down on board

    Args:
        car_id (str): ID of car
        pos (tuple): col and row indexs
        grid (list): a board state

    Returns:
        str: a "fingerprint" of new board state
    """
    grid[pos[0]][pos[1]] = -1
    grid[pos[0]+ cars[car_id].len][pos[1]] = car_id
    return stringify_grid(grid)

def shift_car_up(car_id: str, pos: tuple, grid: list)->str:
    """
    Shifts a car up on board

    Args:
        car_id (str): ID of car
        pos (tuple): col and row indexs
        grid (list): a board state

    Returns:
        str: a "fingerprint" of new board state
    """
    old_end_pos = (pos[0] + cars[car_id].len)-1
    grid[pos[0]-1][pos[1]] = car_id
    grid[old_end_pos][pos[1]] = -1
    return stringify_grid(grid)


def calculate_potential_moves(car_id: str, grid: list)->list:
    """
    Calculates all possible moves for specified car

    Args:
        car_id (str): ID of the car
        grid (list): current board state

    Returns:
        list: all possibles moves as "moves" namedtuples
    """
    moves = []
    car_init_state = cars[car_id]

    move_allowed = lambda y, x: (y >= 0 and y < len(grid)) and (x >= 0 and x < len(grid[y])) and grid[y][x] == -1

    #finds where car starts in matrix
    start_pos = (-1,-1) #x,y
    for row_index, row in enumerate(grid):
        if start_pos != (-1,-1):
            break
        for col_index, col in enumerate(row):
            if col == car_id:
                start_pos = (row_index, col_index)
                break
    
    if car_init_state.direction == 'H': #horizontal
        if move_allowed(start_pos[0], start_pos[1]-1): #check left
            moves.append(move_tuple(shift_car_left(car_id, start_pos, copy.deepcopy(grid)), (car_id, -1)))
        if move_allowed(start_pos[0], start_pos[1] + car_init_state.len):#check right
            moves.append(move_tuple(shift_car_right(car_id, start_pos, copy.deepcopy(grid)), (car_id, 1)))
    else: #vertical
        if move_allowed(start_pos[0]-1, start_pos[1]): #check up 
            moves.append(move_tuple(shift_car_up(car_id, start_pos, copy.deepcopy(grid)), (car_id, -1)))
        if move_allowed(start_pos[0] + car_init_state.len, start_pos[1]): #check down
            moves.append(move_tuple(shift_car_down(car_id, start_pos, copy.deepcopy(grid)), (car_id, 1)))

    return moves


def calculate_node_hueristic(move: tuple)->float:
    """
    Returns the hueristic of a move.
    1 -> moves goal car in positive direction
    2 -> For veticals cars...if truck(size 3) move down || if car(size 2) move up
    3 -> Given to horizontal cars that can move in the negative direction   
    3.5 -> moves goal car in negative direction || move horizontal cars in positive direction || opposite moves from '3'

    Args:
        move (tuple): 'move' namedtuple of move to calculate

    Returns:
        float: a hueristic for the move
    """
    car_info = cars[move.move_val[0]]
    #if goal car can move right this is highest priority else set low prioirity
    if car_info.goal_car:
        if move.move_val[1] == 1:
            return 1.0
        else:
            return 3.5
    #medium priority to horizontal cars that can move left
    elif car_info.direction == 'H':
        if move.move_val[1] == -1:
            return 3.0
        else:
            return 3.5
    else: #vertical (medium priority)
        #priority to move trucks(size 3) down
        if car_info.len == 3 and move.move_val[1] == 1:
            return 2.0
        elif car_info.len == 2 and move.move_val[1] == -1:
            return 2.0
        else:
            return 3.5


def expand_node(grid:list, state_space:Graph)->tuple:
    """
    "Expands" node by finding all possible board states from current state and updates the state space

    Args:
        grid (list): current board state
        state_space (Graph): all discovered states thus far

    Returns:
        tuple: new state space, all newly found states from current board state, new/updated hueristics for current state
    """
    hueristic_map = {}
    new_nodes = []
    for automobile in cars.keys():
        potential_moves = calculate_potential_moves(automobile, copy.deepcopy(grid))
        for move in potential_moves:
            #arc name is the movement code. If node does not exist function will create it.
            state_space.add_arc(stringify_grid(grid), move.grid_string, label=move.move_val)#arc label is move to achieve state
            hueristic_map[move.grid_string] = calculate_node_hueristic(move)
            new_nodes.append(move.grid_string)
    return state_space, new_nodes, hueristic_map


def reached_goal(grid: list):
    """
    Checks is state is the goal state

    Args:
        grid (list): current board state

    Returns:
        _type_: if state is goal state true
    """
    return grid[GOAL_POS[0]][GOAL_POS[1]] == GOAL_CAR_ID and grid[GOAL_POS[0]][GOAL_POS[1]+1] == GOAL_CAR_ID


def a_star(grid: list)->list:
    """
    Expands and traverses through the state space until the shortest path is found using A* algorithm.

    Args:
        grid (list): initial state of board

    Returns:
        list: tuple moves to travese shortest path to goal state
    """
    visited = []
    heuristic_map = {}
    state_space = Graph()
    priority_queue = Heap(is_max=False)

    #f(x) = g(x) + h(x)
    #adds length of history to the precalculated heuristic for that state
    f_value = lambda q_element: heuristic_map[q_element.unique_id] + len(q_element.history)

    #init
    init_id = stringify_grid(grid)
    heuristic_map[init_id] = 4 #random high init value
    init_q_entry = queue_entry(init_id, [])
    priority_queue.add((f_value(init_q_entry), init_q_entry))
    state_space.add_node(init_id)

    while len(priority_queue) > 0:
        node = priority_queue.pop()
        if node[1].unique_id not in visited:
            visited.append(node[1].unique_id)
            #turns str "fingerprint" of state into a matrix
            grid = listify_grid(node[1].unique_id)
            if reached_goal(grid): #goal state found -> exit with history
                return node[1].history
            state_space, new_nodes, new_heuristic_mappings = expand_node(copy.deepcopy(grid), state_space)
            #combine maps. This will overwrite old values in map with updated ones
            heuristic_map = {**heuristic_map, **new_heuristic_mappings}
            #get all arcs associated with current board state
            nodes_arcs = state_space._get_node_arcs(stringify_grid(grid))

            for new_node in new_nodes:
                #get movement code from arc name
                movement_code = ""
                for arc in nodes_arcs:
                    if arc.dest == new_node:
                        movement_code = arc.arc_name
                #update history
                new_history = copy.deepcopy(node[1].history) 
                new_history.append(movement_code)
                new_q_entry = queue_entry(new_node, new_history)
                priority_queue.add((f_value(new_q_entry), new_q_entry))
        
    return None

#FOR DEBUG
# def pprint(grid: list):
#     for index, i in enumerate(grid):
#         for index2, j in enumerate(grid[index]):
#             if grid[index][index2] == -1:
#                 grid[index][index2] = 'x'
#             else:
#                 grid[index][index2] = str(grid[index][index2])
#         print(grid[index])
#     print("\n")


def csv_reader(file_path="")->tuple:
    """
    Reads in a csv files contents. If one is not specified in option this function will prompt user.

    Args:
        file_path (str, optional): path to '.board' file. Defaults to "".

    Returns:
        str: contents of csv
    """
    file_contents = ""

    while not file_path and file_path.split('.')[-1] not in ['board', 'csv']:
        file_path = input("Please enter the name of the board file: ")

    with open(file_path, 'r') as fi:
        file_contents = fi.read().split('\n')

    return file_contents, file_path

def write_sol_to_file(path: list, board_file_path: str)->str:
    """
    Writes a paths history to a '.sol' file.

    Args:
        path (list): history of shortest path...tuples

    Returns:
        str: file name
    """
    board_file_name = board_file_path.split('/')[-1].split('.')[0]
    #create file name following format solution_<BOARD FILE NAME>_<RANDOM 10 NUMS>.sol
    file_name = "game_data/solution_{0}_{1}.sol".format(board_file_name, "".join([str(random.randint(0,9)) for i in range(10)])) 
    with open(file_name, 'w') as fi:
        for tups in path:
            #tups -> car_id, move
            fi.write("{0},{1}\n".format(tups[0], tups[1]))
    
    return file_name


def driver()->tuple:
    """
    Runs the program and provides snazzy & insightful output

    Returns:
        tuple: board_file, solution_file
    """
    file_contents, file_path = csv_reader()
    print('Setting up the board...🏗️ ')
    init_state = init_represent(file_contents)
    print('Navigating traffic...🚗 ')
    start = datetime.now()
    path = a_star(init_state)
    end = datetime.now()
    if path is not None:
        print('✅ Successfully found a way out in {0} using {1} move(s)'.format(end - start, len(path)))
        print("Solution written to file: {}".format(write_sol_to_file(path, file_path)))
    else:
        print("❌ Board has no solutions. Took {}".format(end-start))

if __name__ == '__main__':
    driver()
