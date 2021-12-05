# -*- coding: utf-8 -*-
"""
Created on Sun Dec  5 00:06:10 2021

@author: Connor
"""
import numpy as np

# Create a custom line object for easy parsing and handling
class Line:
    def __init__(self, line):
        self.xp1 = int(line[0].split(",")[0])
        self.yp1 = int(line[0].split(",")[1])
        
        self.xp2 = int(line[1].split(",")[0])
        self.yp2 = int(line[1].split(",")[1])
    
    def __repr__(self):
        return f"({self.xp1, self.yp1})->({self.xp2, self.yp2})"

    def is_vert(self):
        return self.xp1 == self.xp2
    
    def is_horiz(self):
        return self.yp1 == self.yp2
    
    def get_p1(self):
        return (self.xp1, self.yp1)
    
    def get_p2(self):
        return (self.xp2, self.yp2)
    
    def pos_slope(self):
        return ((self.yp2 - self.yp1) / (self.xp2 - self.xp1)) > 0

def parse_input(filename):
    with open(filename, "r") as fh:
        lines = fh.readlines()
    
    # each line becomes a line object
    segments = []
    for line in lines:
        ll = Line(line.split(" -> "))
        segments.append(ll)
    
    return segments

def find_hv_overlaps(segments, max_size=1000):
    # Part 1
    grid = np.zeros((max_size, max_size))
    
    for segment in segments:
        p1 = segment.get_p1()
        p2 = segment.get_p2()
        if segment.is_horiz():
            # Make sure indexing is in the correct order
            min_x, max_x = min(p1[0], p2[0]), max(p1[0], p2[0])
            yy = p1[1]
            grid[yy, min_x:max_x+1] += 1
        elif segment.is_vert():
            # Make sure indexing is in the correct order
            xx = p1[0]
            min_y, max_y = min(p1[1], p2[1]), max(p1[1], p2[1])
            grid[min_y:max_y+1, xx] += 1
    
    return grid

def find_overlaps(segments, max_size=1000):
    # Part 2
    grid = np.zeros((max_size, max_size))
    
    for segment in segments:
        p1 = segment.get_p1()
        p2 = segment.get_p2()
        if segment.is_horiz():
            # Make sure indexing is in the correct order
            min_x, max_x = min(p1[0], p2[0]), max(p1[0], p2[0])
            yy = p1[1]
            grid[yy, min_x:max_x+1] += 1
        elif segment.is_vert():
            # Make sure indexing is in the correct order
            xx = p1[0]
            min_y, max_y = min(p1[1], p2[1]), max(p1[1], p2[1])
            grid[min_y:max_y+1, xx] += 1
        else:
            # Diagonals need to be handled specially
            if segment.pos_slope():
                min_x, max_x = min(p1[0], p2[0]), max(p1[0], p2[0])
                min_y, max_y = min(p1[1], p2[1]), max(p1[1], p2[1])
                for x,y in zip(range(min_x, max_x+1), range(min_y, max_y+1)):
                    grid[y, x] += 1
            else:
                min_x, max_x = min(p1[0], p2[0]), max(p1[0], p2[0])
                min_y, max_y = min(p1[1], p2[1]), max(p1[1], p2[1])
                # If slope is negative, iterate over y points backwards
                for x,y in zip(range(min_x, max_x+1), range(max_y, min_y-1, -1)):
                    grid[y, x] += 1
    # return final grid
    return grid       
     
    
if __name__ == "__main__":
    segments = parse_input("input5.txt")
    grid = find_hv_overlaps(segments)
    print(np.sum(grid >= 2))
    
    grid = find_overlaps(segments)
    print(np.sum(grid >= 2))