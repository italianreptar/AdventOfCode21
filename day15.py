# -*- coding: utf-8 -*-
"""
Created on Wed Dec 15 18:35:52 2021

@author: Connor
"""

import numpy as np

def parse_input(filename):
    with open(filename, "r") as fh:
        lines = fh.readlines()
    
    # Strip input into 10x10 array of ints
    grid = np.zeros((len(lines),len(lines[0].rstrip())))
    for ii, line in enumerate(lines):
        for jj, cc in enumerate(line.rstrip()):
            grid[ii,jj] = int(cc)
        
    return grid

class Path(list):
    def __init__(self, *args):
        super().__init__(*args)
    
    def cost(self, grid):
        out = 0
        for ii in self[1:]:
            out += grid[ii[0]][ii[1]]
        return out
    
    def cost_two(self, grid, target):
        out = self.cost(grid)
        out += abs(target[0] - self[-1][0]) + abs(target[1] - self[-1][1])
        return out

def is_valid(xy, xmax, ymax):
    # From day9, quick check to see if a point is valid in a grid
    return xy[0] >= 0 and xy[0] <= xmax and xy[1] >= 0 and xy[1] <= ymax

def solve1(grid):
    start_pos = (0, 0) # y, x (indices)
    ymax, xmax = grid.shape
    target_pos = (ymax-1, xmax-1)
    closed_list = list()
    start_p = Path((start_pos,))
    open_list = [(start_p.cost_two(grid, target_pos), start_p)]
    counter = 0
    while open_list:
        pt = open_list.pop(0)
        this_p = pt[1].copy()      # unpack point
        ii, jj = this_p[-1]  # unpack last point
        pts = [(ii+1, jj), (ii-1, jj), (ii, jj+1), (ii, jj-1)]
        pts = [point for point in pts if is_valid(point, ymax-1, xmax-1)]
        for pp in pts:
            if pp == target_pos:
                new_p = Path(this_p + [pp])
                closed_list.append((new_p.cost_two(grid, target_pos), new_p))
            elif pp not in this_p:
                # check to see if pp is in any other path in open list
                # if yes, see which cost is lower
                # if its cost is lower, skip
                kill_list = list()
                break_flag = False
                new_p = Path(this_p + [pp])
                for ii, (cost2, path) in enumerate(open_list):
                    if pp in path:
                        comp_p = Path(path[0:path.index(pp)+1])
                        if comp_p.cost_two(grid, target_pos) < new_p.cost_two(grid, target_pos):
                            break_flag = True
                            break
                        else:
                            kill_list.append(ii)
                
                # check to see if pp is in any path is in the closed list
                # if yes, see which cost is lower
                # if its cost is lower, skip
                # otherwise, add this node to the open list
                if not break_flag:
                    for ii, (cost2, path) in enumerate(closed_list):
                        if pp in path:
                            comp_p = Path(path[0:path.index(pp)+1])
                            if comp_p.cost_two(grid, target_pos) < new_p.cost_two(grid, target_pos):
                                break_flag = True
                                break
                if not break_flag:
                    open_list.append((new_p.cost_two(grid, target_pos), new_p))
                if kill_list:
                    for ii in sorted(kill_list, reverse=True):
                        open_list.pop(ii)                
            else:
                pass
        if counter % 100 == 0:
            print(len(open_list))
        counter += 1
        open_list = sorted(open_list)
        
    return closed_list

def get_lowest(dd):
    min_cost = 1e99
    min_key = None
    for key, (cost, pp) in dd.items():
        if cost < min_cost:
            min_key = key
            min_cost = cost
    return dd.pop(min_key)

def solve1_better(grid):
    start_pos = (0, 0) # y, x (indices)
    ymax, xmax = grid.shape
    target_pos = (ymax-1, xmax-1)
    closed_list = {}
    start_p = Path((start_pos,))
    open_dict = {start_pos: (start_p.cost_two(grid, target_pos), start_p)}
    counter = 0
    while open_dict:
        pt = get_lowest(open_dict)
        this_p = pt[1].copy()      # unpack point
        ii, jj = this_p[-1]  # unpack last point
        pts = [(ii+1, jj), (ii-1, jj), (ii, jj+1), (ii, jj-1)]
        pts = [point for point in pts if is_valid(point, ymax-1, xmax-1) and point not in this_p]
        for pp in pts:
            if pp == target_pos:
                new_p = Path(this_p + [pp])
                closed_list[pp] = (new_p.cost_two(grid, target_pos), new_p)
            else:
                # check to see if pp is in any other path in open list
                # if yes, see which cost is lower
                # if its cost is lower, skip
                break_flag = False
                new_p = Path(this_p + [pp])
                if pp in open_dict:
                    new_cost = new_p.cost_two(grid, target_pos)
                    if open_dict[pp][0] > new_cost:
                        open_dict[pp] = (new_cost, new_p)
                else:
                    open_dict[pp] = (new_p.cost_two(grid, target_pos), new_p)
                
        if counter % 100 == 0:
            print(len(open_dict))
        counter += 1
        
    return closed_list

def main():
    grid = parse_input("input15.txt")
    # cl = solve1_better(grid)
    
    grid2 = np.vstack((grid, grid+1, grid+2, grid+3, grid+4))
    grid3 = np.hstack((grid2, grid2+1, grid2+2, grid2+3, grid2+4))
    grid4 = grid3 % 10
    cl2 = solve1(grid3)
    
    return grid, cl
    
if __name__ == "__main__":
    grid, cl = main()
    