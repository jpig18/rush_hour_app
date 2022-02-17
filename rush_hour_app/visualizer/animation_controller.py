# File: animation_controller.py
# Author: Michael Huelsman
# Created On: 11 Nov 2021
# Purpose:
#   A simple animation controller and related classes.
from visual_car import VisCar


class MoveCarAnimation:
    # Precond:
    #   car is a valid VisCar object.
    #   units is an integer indicating how many cells to move the car.
    #   length is an integer indicating how many frames the move should take in total.
    #
    # Postcond:
    #   Builds a new MoveCarAnimation object with the given parameters.
    def __init__(self, car: VisCar, units: int, length: int):
        self.car = car
        self.frames = length
        self.offset = units/self.frames
        self.current_frame = 0
        self.final_pos = list(self.car.get_unit_location())
        self.units = units
        if self.car.is_horizontal():
            self.final_pos[0] += units
        else:
            self.final_pos[1] += units
        self.final_pos = tuple(self.final_pos)

    # Precond:
    #   None.
    #
    # Postcond:
    #   Returns true if the animation is completed.
    def finished(self):
        return self.current_frame == self.frames

    # Precond:
    #   None.
    #
    # Postcond:
    #   Animates the next frame by moving the car.
    def next_frame(self):
        if self.finished():
            return
        self.current_frame += 1
        if self.car.is_horizontal():
            self.car.add_offset((self.offset, 0))
        else:
            self.car.add_offset((0, self.offset))
        if self.current_frame == self.frames:
            self.car.set_location(self.final_pos)
            self.car.reset_offset()
        self.car.move_to()

    def set_final(self):
        self.final_pos = list(self.car.get_unit_location())
        if self.car.is_horizontal():
            self.final_pos[0] += self.units
        else:
            self.final_pos[1] += self.units
        self.final_pos = tuple(self.final_pos)

class AnimationController:
    # Precond:
    #   None.
    #
    # Postcond:
    #   Builds an animation controller with an empty animation queue.
    def __init__(self):
        self.animation_queue = []

    # Precond:
    #   animiation is an object with the following methods:
    #       next_frame: renders the next frame of the animation.
    #       finished: returns true when the animation is complete.
    #
    # Postcond:
    #   Adds the animation to the queue.
    def add_animation(self, animation):
        self.animation_queue.append(animation)

    # Precond:
    #   None.
    #
    # Postcond:
    #   Renders the next frame. If there is not animation in the queue does nothing.
    def next_frame(self):
        if  len(self.animation_queue) > 0:
            self.animation_queue[0].next_frame()
            if self.animation_queue[0].finished():
                self.animation_queue.pop(0)
                if len(self.animation_queue) > 0:
                    self.animation_queue[0].set_final()

    # Precond:
    #   None.
    #
    # Postcond:
    #   Returns true if the queue is empty.
    def empty(self):
        return len(self.animation_queue) == 0