# File: visual_car.py
# Author: Michael Huelsman
# Created On: 11 Nov 2021
# Purpose:
#   A class for handling information pertaining to the visual representation of a car.

from random import randint

from graphics import Rectangle, Point, color_rgb

class VisCar:
    # Precond:
    #   cell_dim is a pair of integers representing the size of a single board cell in pixels.
    #   location is the x,y board coordinates of the car's location.
    #   size is the length of the car in cells.
    #   horizontal is a boolean that is true if the car is in the horizontal orientation, otherwise it is considered to
    #       be vertical.
    #   goal is a boolean that is true if the car is the goal car.
    #
    # Postcond:
    #   Builds a new VisCar object based on the provided information.
    def __init__(self, cell_dim: tuple, location: tuple, size: int, horizontal: bool, goal: bool):
        self.cell_size = cell_dim
        self.location = location
        self.offset = [0, 0]
        self.size = size
        self.horizontal = horizontal
        self.goal = goal
        self.color = color_rgb(randint(0, 128), randint(10, 255), randint(10, 255))
        if self.goal:
            self.color = color_rgb(255, 0, 0)
        self.rect = None
        if self.horizontal:
            self.rect = Rectangle(Point(0, 0), Point(self.size * self.cell_size[0], self.cell_size[1]))
        else:
            self.rect = Rectangle(Point(0, 0), Point(self.cell_size[0], self.size * self.cell_size[1]))
        self.rect.setFill(self.color)
        self.rect.setOutline(color_rgb(0, 0, 0))
        self.rect.setWidth(3)
        self.move_to()

    # Precond:
    #   None.
    #
    # Postcond:
    #   Returns a pair of integers indicating the current pixel location of the car.
    def get_location(self) -> tuple:
        x = int((self.location[0] + self.offset[0]) * self.cell_size[0])
        y = int((self.location[1] + self.offset[1]) * self.cell_size[1])
        return x, y

    # Precond:
    #   None.
    #
    # Postcond:
    #   Returns a pair of integers indicating the current pixel location of the car.
    def get_unit_location(self) -> tuple:
        return self.location

    # Precond:
    #   None.
    #
    # Postcond:
    #   Moves the car's rectangle to the proper location.
    def move_to(self):
        ul = self.rect.getP1()
        nl = self.get_location()
        dx = nl[0] - ul.getX()
        dy = nl[1] - ul.getY()
        self.rect.move(dx, dy)

    # Precond:
    #   offset is a pair of float values to add to the offset.
    #
    # Postcond:
    #   Adds the offset to the current offset.
    def add_offset(self, offset: tuple) -> None:
        self.offset[0] += offset[0]
        self.offset[1] += offset[1]
        return

    # Precond:
    #   None.
    #
    # Postcond:
    #   Resets the offset to zero.
    def reset_offset(self):
        self.offset = [0, 0]

    # Precond:
    #   to is a pair of integers indicating a cell location.
    #
    # Postcond:
    #   Changes the location to the provided point.
    def set_location(self, to: tuple):
        self.location = to

    # Precond:
    #   None.
    #
    # Postcond:
    #   Returns the rectangle used to draw the car to the screen.
    def get_rectangle(self):
        return self.rect

    # Precond:
    #   None.
    #
    # Postcond:
    #   Returns true if the car is oriented horizontal.
    def is_horizontal(self):
        return self.horizontal
