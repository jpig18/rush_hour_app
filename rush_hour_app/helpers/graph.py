"""
Graph Data Structure 

Author: John Pignato

TLDR:
    Graph DS in vanilla python

Explaination:
    Graph DS in vanilla python. Made of a dictionary that maps str to a list of namedtuples -> "ARC"
"""
from collections import namedtuple
from queue import Queue

class Graph:
    """
    A basic graph class
    """

    def __init__(self):
        #Node name is key value and value is a list of named tuples
        self.__graph = {}
        #Decision to use named tuple over py class is since collections module is written in C 
        #It will always be faster than a pure python implemented class
        #sibling_index None if arc is directed
        self.__arc = namedtuple('ARC', ['arc_name', 'dest', 'sibling_index'])

    def __len__(self):
        return len(self.__graph.keys())
    
    def __repr__(self): #debug
        repr_str = ""
        for k in self.__graph.keys():
            repr_str += "Node:{}\n".format(k)
            for arc in self.__graph[k]:
                repr_str += "\t{}\n".format(str(arc))
        repr_str += '\n'
        return repr_str

    def _get_node_arcs(self, label: str)->list:
        try:
            return self.__graph[label]
        except KeyError:
            return None


    def add_node(self, label: str):
        """
        Adds node to graph

        Args:
            label (str): name of node
        """
        try: #check existence of node
            self.__graph[label]
        except KeyError:
            self.__graph[label] = []


    def add_arc(self, src: str, dest: str, label:str = None):
        """
        Adds directed arc in graph

        Args:
            src (str): source node
            dest (str): source node
            label (str, optional): name of arc. Defaults to None.
        """
        try:
            self.__graph[src]
        except KeyError:
            self.__graph[src] = []
        try:
            self.__graph[dest]
        except KeyError:
            self.__graph[dest] = []
        
        self.__graph[src].append(self.__arc(label, dest, None))


    def add_arc_undirected(self, src: str, dest: str, label:str = None):
        """
        Adds undirected arc to graph

        Args:
            src (str): source node
            dest (str): source node
            label (str, optional): name of arc. Defaults to None.
        """
        try:
            self.__graph[src]
        except KeyError:
            self.__graph[src] = []
        try:
            self.__graph[dest]
        except KeyError:
            self.__graph[dest] = []

        self.__graph[src].append(self.__arc(label, dest, len(self.__graph[dest])))
        self.__graph[dest].append(self.__arc(label, src, len(self.__graph[src])-1))


    def remove_node(self, label: str):
        """
        Removes a node from the graph and all associated arcs.

        Args:
            label (str): name of node
        """
        try:
            del self.__graph[label]
        except KeyError:
            pass

    
    def remove_arc(self, src: str, dest: str):
        """
        Removes an arc from a graph

        Args:
            src (str): source of arc
            dest (str): destination of arc
        """
        try:
            for index, arc in enumerate(self.__graph[src]):
                if arc.dest == dest:
                    del self.__graph[src][index]
                    if arc.sibling_index is not None:
                        del self.__graph[dest][arc.sibling_index]
                    break
        except KeyError:
            pass

    def reachable(self, src: str, dest: str)->bool:
        """
        Checks if a node is reachable from a specified source.

        Args:
            src (str): source node
            dest (str): destination node

        Returns:
            bool: is reachable?
        """
        path = self.shortest_path(src, dest)
        return False if path is None or len(path) == 0 else True

    def shortest_path(self, src: str, dest: str)->list:
        """
        Attempts to find shortest path from source to destination nodes.
        Uses breadth first search to brute force a solution.

        Args:
            src (str): source node
            dest (str): dest node

        Returns:
            list: returns list of nodes to traverse. None if no path exists
        """
        frontier = Queue()
        try:
            frontier.add((src, [arc.dest for arc in self.__graph[src]]))
        except KeyError:
            return None #src node does not exist
        visited = []
        current_node = frontier.pop()
        visited.append(current_node[0])
        while current_node[0] != dest:
            for arc_dest in [arc.dest for arc in self.__graph[current_node[0]]]:
                if arc_dest not in visited:
                    if current_node[0] != src:
                        pair = (arc_dest, current_node[1]+list(current_node[0])) 
                    else:
                        pair = (arc_dest, list(current_node[0])) 
                    visited.append(arc_dest)
                    frontier.add(pair)
            if frontier.size() == 0:
                break
            current_node = frontier.pop()
            if current_node[0] == dest:
                return current_node[1] + list(current_node[0])
        
        if frontier.size() == 0:
            return None



if __name__ == '__main__':
    temp = Graph()
    temp.add_arc('a','b')
    temp.add_arc('b','c')
    temp.add_arc('c','d')
    temp.add_arc('a','e')
    temp.add_arc('e','f')
    path = temp.shortest_path('a','d')
    print(path)