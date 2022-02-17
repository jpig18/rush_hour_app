"""
Heap Data Structure

Author: John Pignato

TLDR:
    Heap DS in vanilla python

Explaination:
    All heaps are assumed to consist of pairs. These pairs are tuples of the form: (number, object).
    If is suggested that you use a list to store the heap elements. If you do this then at element i the 
    left subtree root is located at position (2 ∗ i) + 1 and the right subtree root is located at position 
    (2 ∗ i) + 2. This also means that adding an element to the bottom of the tree is simplified to appending 
    it to the list.
"""
import math

class Heap:

    def __init__(self, is_max=True, lst=[]):
        self.__heap_array = lst
        self.__is_max = is_max
        for i in range(len(self.__heap_array), -1, -1):
            self.__heapify(i)

    def __len__(self):
        """
        size of heap

        Returns:
            [int]: amount of elements in heap
        """
        return len(self.__heap_array)
    
    def __repr__(self): #debug
        return_string = "-"*50 + "\n"
        for item in self.__heap_array:
            return_string += """
            Current Board: {}
            Value: {}
            History: {}
            """.format(item[1].unique_id, item[0], item[1].history)
        return return_string  

    def add(self, item)->None:
        """
        adds a leaf to heap tree

        Args:
            item (Any): item to add to heap
        """
        parent_calc = lambda x: math.floor((x/2)-1) if x!=0 and x%2==0 else math.floor(x/2)
        
        if type(item) is not tuple:
            return False
        
        self.__heap_array.append(item)
        current_loc = len(self.__heap_array)-1
        
        if self.__is_max:
            while self.__heap_array[parent_calc(current_loc)][0] < self.__heap_array[current_loc][0]:
                self.__heap_array[parent_calc(current_loc)], self.__heap_array[current_loc] = self.__heap_array[current_loc], self.__heap_array[parent_calc(current_loc)]
                current_loc = parent_calc(current_loc)
        else:
            while self.__heap_array[parent_calc(current_loc)][0] > self.__heap_array[current_loc][0]:
                self.__heap_array[parent_calc(current_loc)], self.__heap_array[current_loc] = self.__heap_array[current_loc], self.__heap_array[parent_calc(current_loc)]
                current_loc = parent_calc(current_loc)
        return True

    
    def pop(self)->tuple:
        """
        Removes the root from the heap

        Returns:
            tuple: returns to root leaf from the heap
        """
        max_node = self.__heap_array[0]
        self.__heap_array[0], self.__heap_array[-1] = self.__heap_array[-1], self.__heap_array[0]
        self.__heap_array.pop()
        self.__heapify(0)
        return max_node
    
    def peek(self)->tuple:
        """
        Allows you to check the root value

        Returns:
            tuple: returns the root leaf
        """
        try:
            return self.__heap_array[0]
        except KeyError:
            return None

    def size(self)->int: #to be deprecated in favor of __len__()
        """
        size of heap

        Returns:
            [int]: amount of elements in heap
        """
        return len(self.__heap_array)

    def __heapify(self, loc)->None:
        """
        Recursive function to arrange one leaf correctly in heap.

        Args:
            loc ([int]): location of leaf
        """
        left_node_loc = loc*2+1
        right_node_loc = loc*2+2
        higher_priority_loc = None

        try:
            if self.__is_max:
                if self.__heap_array[left_node_loc] and self.__heap_array[left_node_loc] > self.__heap_array[loc]:
                    higher_priority_loc = left_node_loc
                else:
                    higher_priority_loc = loc
            else:
                if self.__heap_array[left_node_loc] and self.__heap_array[left_node_loc] < self.__heap_array[loc]:
                    higher_priority_loc = left_node_loc
                else:
                    higher_priority_loc = loc
        except IndexError:
            higher_priority_loc = loc

        try:
            if self.__is_max:
                if self.__heap_array[right_node_loc] and self.__heap_array[right_node_loc] > self.__heap_array[higher_priority_loc]:
                    higher_priority_loc = right_node_loc
            else:
                if self.__heap_array[right_node_loc] and self.__heap_array[right_node_loc] < self.__heap_array[higher_priority_loc]:
                    higher_priority_loc = right_node_loc
        except IndexError:
            pass

        if higher_priority_loc != loc:
            self.__heap_array[loc],  self.__heap_array[higher_priority_loc] = self.__heap_array[higher_priority_loc], self.__heap_array[loc]
            self.__heapify(higher_priority_loc)


if __name__ == '__main__':
    print([(i,i) for i in range(10)])
    h = Heap([(i,i) for i in range(10)])
    print(h.pop())
    print(h)
