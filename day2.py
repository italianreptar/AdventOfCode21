# -*- coding: utf-8 -*-
"""
Created on Thu Dec  2 00:20:50 2021

@author: Connor
"""

class Direction:
    def __init__(self, value):
        self.value = int(value)

class Forward(Direction):
    def __init__(self, value):
        super().__init__(value)

class Up(Direction):
    def __init__(self, value):
        super().__init__(value)
        
class Down(Direction):
    def __init__(self, value):
        super().__init__(value)

def parse_input(filename):
    with open(filename, "r") as fh:
        lines = fh.readlines()
    
    output = []
    
    for line in lines:
        key, val = line.split()
        if key.lower() == "forward":
            output.append(Forward(val))
        elif key.lower() == "up":
            output.append(Up(val))
        elif key.lower() == "down":
            output.append(Down(val))
        else:
            print(key, val)
    
    return output

def get_position(data):
    x, d = 0,0
    for dt in data:
        if isinstance(dt, Forward):
            x += dt.value
        elif isinstance(dt, Down):
            d += dt.value
        elif isinstance(dt, Up):
            d -= dt.value
        else:
            raise ValueError("")
    return x, d

def get_new_position(data):
    x, d, a = 0, 0, 0
    for dt in data:
        if isinstance(dt, Forward):
            x += dt.value
            d += a*dt.value
        elif isinstance(dt, Down):
            a += dt.value
        elif isinstance(dt, Up):
            a -= dt.value
        else:
            raise ValueError("")
    return x, d            

if __name__ == "__main__":
    
    data = parse_input("input2.txt")
    x, d = get_position(data)
    x2, d2 = get_new_position(data)
            