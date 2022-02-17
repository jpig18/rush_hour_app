# File: visualize.py
# Author: Michael Huelsman
# Created On: 11 Nov 2021
# Purpose:
#   Allows the visualization of rush hour move lists.

from visual_car import VisCar
from animation_controller import MoveCarAnimation, AnimationController
from graphics import *
from time import time
from os.path import exists

def parse_board(fname, cell_dim):
    dim = None
    cars = None
    with open(fname, 'r') as fin:
        first_line = True
        cars = {}
        for line in fin:
            line = line.strip()
            if line == '':
                continue
            line = line.split(',')
            if first_line:
                dim = tuple(map(lambda x: int(x), line))
                first_line = False
            else:
                loc = (int(line[1]), int(line[2]))
                size = int(line[4])
                horz = (line[3].upper() == 'H')
                goal = (line[5].upper() == 'T')
                ident = int(line[0])
                cars[ident] = VisCar(cell_dim, loc, size, horz, goal)
    return dim, cars

def parse_moves(fname, cars, fpm):
    result = []
    with open(fname, 'r') as fin:
        for line in fin:
            line = line.strip().split(',')
            ident = int(line[0])
            move = int(line[1])
            result.append(MoveCarAnimation(cars[ident], move, fpm))
    return result

def render_board(cars, win):
    for car in cars:
        cars[car].get_rectangle().draw(win)

def update_board(cars):
    for car in cars:
        cars[car].move_to()


def main(board_file = None, sol_file = None):
    while board_file is None:
        board_file = input('Which board should I load: ')
        if not exists(board_file):
            print("File does not exist.")
            print("Please input a valid file.")
            board_file = None
    while sol_file is None:
        sol_file = input('Which solution should I load: ')
        if not exists(sol_file):
            print("File does not exist.")
            print("Please input a valid file.")
            sol_file = None
    win = GraphWin("Rush Solver Visualizer", 600, 600)
    cell_dim = (100, 100)
    ani_control = AnimationController()
    board = parse_board(board_file, cell_dim)
    render_board(board[1], win)
    sol = parse_moves(sol_file, board[1], 10)
    for ani in sol:
        ani_control.add_animation(ani)
    active = True
    frame_count = 0
    win.getMouse()
    start = time()
    while active:
        if time()-start >= 0.03:
            ani_control.next_frame()
            win.update()
            start = time()
            frame_count += 1
            if ani_control.empty():
                active = False
    win.getMouse()
    print("It took",frame_count,"frames.")



if __name__ == '__main__':
    main()
