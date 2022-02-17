import copy
from rush_hour_app.helpers.graph import Graph
from rush_hour_app.rush_hour_solver import *

start_board = [[-1, -1, 0, 1, 1, 1], 
                [-1, -1, 0, 2, 3, 3], 
                [4, 5, 5, 2, 6, 7], 
                [4, 8, -1, -1, 6, 7], 
                [9, 8, 10, 10, 6, 11], 
                [9, 12, 12, 13, 13, 11]]

def test_init_represent():
    grid = init_represent(csv_reader(file_path="game_data/test.board"))
    assert grid == start_board

# def test_check_inbounds():
#     assert not move_allowed(start_board, 6, 0) and \
#             not move_allowed(start_board, 0, 6) and \
#             move_allowed(start_board, 1, 0) and \
#             move_allowed(start_board, 3, 2)

def test_shifts():
    correct_car_grid = [[4, -1, 0, 1, 1, 1], 
                        [4, -1, 0, -1, 3, 3], 
                        [9, 5, 5, 2, 6, 7], 
                        [9, 8, -1, 2, 6, 7], 
                        [-1, 8, 10, 10, 6, 11], 
                        [12, 12, -1, 13, 13, 11]]
    correct_right_car_grid = [[4, -1, 0, 1, 1, 1], 
                            [4, -1, 0, -1, 3, 3], 
                            [9, 5, 5, 2, 6, 7], 
                            [9, 8, -1, 2, 6, 7], 
                            [-1, 8, 10, 10, 6, 11], 
                            [-1, 12, 12, 13, 13, 11]]
    test_grid = shift_car_down(2, (1,3), copy.deepcopy(start_board))
    test_grid = shift_car_up(4, (2,0), listify_grid(test_grid))
    test_grid = shift_car_up(4, (1,0), listify_grid(test_grid))
    test_grid = shift_car_up(9, (4,0), listify_grid(test_grid))
    test_grid = shift_car_up(9, (3,0), listify_grid(test_grid))
    test_grid = shift_car_left(12, (5,1), listify_grid(test_grid))
    test_right_grid = shift_car_right(12, (5,0), listify_grid(test_grid))
    assert stringify_grid(correct_car_grid) == test_grid and test_right_grid == stringify_grid(correct_right_car_grid)
    

def test_calculate_potential_moves():
    start_board = init_represent(csv_reader(file_path="game_data/test.board"))
    upshift_matrix = shift_car_up(4, (2,0), copy.deepcopy(start_board))
    downshift_matrix = shift_car_down(2, (1,3), copy.deepcopy(start_board))
    car_four_moves = calculate_potential_moves(4, copy.deepcopy(start_board))
    car_two_moves = calculate_potential_moves(2, start_board)
    
    assert (len(car_four_moves) == 1 and car_four_moves[0][0] == upshift_matrix and car_four_moves[0][1] == (4, -1))
    assert (len(car_two_moves) == 1 and car_two_moves[0][0] == downshift_matrix and car_two_moves[0][1] == (2, 1))

def test_reached_goal():
    init_represent(csv_reader(file_path="game_data/test.board"))
    goal_matrix = [[-1 for i in range(6)] for i in range(6)]
    goal_matrix[2][4] = 5
    goal_matrix[2][5] = 5
    assert reached_goal(goal_matrix)


# def test_expand_node():
#     valid_state_space = Graph()
#     valid_state_space.add_node('init_represent(csv_reader(file_path="game_data/test.board")')
#     state_space, new_nodes, new_heuristic_mappings = expand_node(init_represent(csv_reader(file_path="game_data/test.board")), Graph())
#     print(state_space, new_nodes, new_heuristic_mappings)
#     assert 1 == 0