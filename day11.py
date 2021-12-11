# -*- coding: utf-8 -*-
"""
Created on Sat Dec 11 00:11:40 2021

@author: Connor
"""

import numpy as np

def parse_input(filename):
    with open(filename, "r") as fh:
        lines = fh.readlines()
    
    # Strip input into 10x10 array of ints
    grid = np.zeros((10,10))
    for ii, line in enumerate(lines):
        for jj, cc in enumerate(line.rstrip()):
            grid[ii,jj] = int(cc)
        
    return grid

def is_valid(xy, xmax, ymax):
    # From day9, quick check to see if a point is valid in a grid
    return xy[0] >= 0 and xy[0] <= xmax and xy[1] >= 0 and xy[1] <= ymax

def resolve_flashes(grid, flash_mask):
    # Set up a clean mask to resolve new flashes that may appear
    clean_mask = np.zeros((10,10), dtype=bool)
    for ii, jj in zip(*np.nonzero(flash_mask)):
        pts = [(ii, jj), (ii+1, jj), (ii-1, jj), (ii, jj+1), (ii, jj-1), 
               (ii+1, jj+1), (ii+1, jj-1), (ii-1, jj+1), (ii-1, jj-1)]
        # for all valid points around a flash that haven't flashed this step
        flash = [pt for pt in pts if is_valid(pt, 9, 9) and grid[pt[0]][pt[1]]<=9]
        for ff in flash:
            # add one to their point and note them down on the clean_mask
            grid[ff[0]][ff[1]] += 1
            clean_mask[ff[0]][ff[1]] = grid[ff[0]][ff[1]] > 9
    if np.nonzero(clean_mask)[0].size > 0:
        # if any new flashes occurred, resolve those
        return resolve_flashes(grid, clean_mask)
    else:
        # once there were no flashes, collapse recursion
        return grid
 
def solve1(grid, num_steps=100):
    yy, xx = grid.shape
    ymax, xmax = yy-1, xx-1
    flash_cnt = 0
    # keep track of flash count
    for tt in range(num_steps):
        grid += 1
        grid = resolve_flashes(grid, grid > 9)
        # before clearing flashes, add them to the count
        flash_cnt += np.sum(grid > 9)
        grid[grid > 9] = 0
        
    return grid, flash_cnt

def solve2(grid):
    yy, xx = grid.shape
    ymax, xmax = yy-1, xx-1
    flash_cnt = 0
    # Keep track of iterations
    iter_cnt = 0
    # While not all just flashed
    while not np.all(grid==0):
        grid += 1
        grid = resolve_flashes(grid, grid > 9)
        flash_cnt += np.sum(grid > 9)
        grid[grid > 9] = 0
        iter_cnt += 1
    return grid, iter_cnt

def main():
    grid = parse_input("test_input11.txt")
    out = solve1(np.copy(grid))
    print(out[1])
    
    out = solve2(np.copy(grid))
    print(out[1])
    
if __name__ == "__main__":
    main()
