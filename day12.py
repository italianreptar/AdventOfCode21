# -*- coding: utf-8 -*-
"""
Created on Sun Dec 12 00:10:21 2021

@author: Connor
"""

import numpy as np

class Node:
    def __init__(self, identifier):
        self.identifier = identifier
        if identifier.upper() == identifier:
            self.big = True
        else:
            self.big = False

        self.connections = []
    
    def connect(self, other_node):
        if other_node.identifier not in self.connections:
            self.connections.append(other_node.identifier)
        if self.identifier not in other_node.connections:
            other_node.connect(self)
    
    def __repr__(self):
        out_str = ""
        for cc in self.connections[:-1]:
            out_str += f"{self.identifier}-{cc}; "
        out_str += f"{self.identifier}-{self.connections[-1]}"
        return out_str

def parse_input(filename):
    with open(filename, "r") as fh:
        lines = fh.readlines()
    connections = [line.rstrip() for line in lines]
    
    ids = []
    nodes = []
    for cc in connections:
        a,b = cc.split("-")
        A = None
        B = None
        if a in ids and b in ids:
            # just connect them
            for node in nodes:
                if node.identifier == a:
                    A = node
                if node.identifier == b:
                    B = node
                if A and B:
                    A.connect(B)
                    continue
                
        elif a in ids and b not in ids:
            # add b, connect a
            for node in nodes:
                if node.identifier == a:
                    A = node
                    continue
            B = Node(b)
            A.connect(B)
            ids.append(b)
            nodes.append(B)
        elif b in ids and a not in ids:
            # add a, connect b
            for node in nodes:
                if node.identifier == b:
                    B = node
                    continue
            A = Node(a)
            A.connect(B)
            ids.append(a)
            nodes.append(A)
        else:
            # add both, connect them
            A = Node(a)
            B = Node(b)
            A.connect(B)
            ids.append(a)
            ids.append(b)
            nodes.append(A)
            nodes.append(B)
    
    return ids, nodes

class Path:
    def __init__(self):
        self.node_ids = ["start"]
        self.allow_twice = False
    
    def __add__(self, other_id):
        self.node_ids += other_id
        return self
    def __repr__(self):
        return f"({self.allow_twice}, {self.node_ids})"
    
    def copy(self):
        out = Path()
        out.node_ids = self.node_ids.copy()
        out.allow_twice = bool(self.allow_twice)
        return out
    
def get_cave(connections, cave_id):
    for ii, cc in enumerate(connections):
        if cc.identifier == cave_id:
            out = connections[ii]
            continue
    return out

def solve(connections):
    output = []
    paths = [Path()]
    
    while paths:
        this_path = paths.pop()
        cave_id = this_path.node_ids[-1]
        
        if cave_id == "end":
            output.append(this_path)
            continue
        
        this_cave = get_cave(connections, cave_id)
        
        for cc in this_cave.connections:
            local_path = this_path.copy()
            if cc == "start":
                continue
            if cc.islower() and cc in local_path.node_ids:
                if not local_path.allow_twice:
                    local_path.allow_twice = True
                else:
                    continue
            paths.append(local_path + [cc])
    
    return output
                    
        
def main():
    nodes, connections = parse_input("input12.txt")
    
    # Start is not guarenteed to be listed first in input, so loop twice to 
    # avoid popping start before end and vice versa
    for ii, cc in enumerate(connections):
        if cc.identifier == "start":
            start = connections.pop(ii)
            
    for ii, cc in enumerate(connections):
        if cc.identifier == "end":
            end = connections.pop(ii)            
    
    connections.insert(0, start)
    connections.append(end)
    output = solve(connections)
    
    print(len([cc for cc in output if not cc.allow_twice]))
    print(len(output))    
    
if __name__ == "__main__":
    connections = main()