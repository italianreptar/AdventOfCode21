# -*- coding: utf-8 -*-
"""
Created on Thu Dec  9 07:42:23 2021

@author: Connor
"""

import numpy as np
import matplotlib.pyplot as plt

def parse_input(filename):
    with open(filename, "r") as fh:
        lines = fh.readlines()
    
    yy = len(lines)
    xx = len(lines[0])-1
    output = np.zeros((yy,xx))
    for ii in range(yy):
        for jj in range(xx):
            output[ii,jj] = int(lines[ii][jj])
    
    return output

def is_valid(xy, xmax, ymax):
    return xy[0] >= 0 and xy[0] <= xmax and xy[1] >= 0 and xy[1] <= ymax

def solve1(inpt):
    yy, xx = inpt.shape
    ymax, xmax = yy-1, xx-1
    out = np.zeros((yy,xx), dtype=bool)
    for ii in range(yy):
        for jj in range(xx):
            pts = [(ii+1, jj), (ii-1, jj), (ii, jj+1), (ii, jj-1)]
            vals = np.array([inpt[ii,jj]])
            vals = np.append(vals, [inpt[pt[0]][pt[1]] for pt in pts if is_valid(pt, ymax, xmax)])
            out[ii][jj] = np.min(vals) == vals[0] and np.min(vals) not in vals[1:]
    return out

# solve 2                
# Iterate over msk
# all 9's define the walls
# find the biggest basins

def solve2(inpt):
    edge_msk = inpt == 9
    basins_msk = inpt != 9
    yy, xx = inpt.shape
    ymax, xmax = yy-1, xx-1
    visited = np.zeros((yy,xx), dtype=bool)
    basins = []
    for ii, jj in zip(*np.nonzero(basins_msk)):
        pts = [(ii, jj), (ii+1, jj), (ii-1, jj), (ii, jj+1), (ii, jj-1)]
        # new_basin_flag = False
        bi = -1
        for pt in pts:
            if is_valid(pt, ymax, xmax) and basins_msk[pt[0]][pt[1]]:
                if [basin for basin in basins if pt in basin]:
                    # if a pt is in a basin
                    # store that basin for later use
                    for basin_index, basin in enumerate(basins):
                        if pt in basin:
                            bi = basin_index
                            continue
            if bi>=0:
                continue
        if bi>=0:
            for pt in pts:
                if pt not in basins[bi] and is_valid(pt, ymax, xmax) and basins_msk[pt[0]][pt[1]]:
                    basins[bi].append(pt)
        else:
            the_basin = [pt for pt in pts if is_valid(pt, ymax, xmax) and basins_msk[pt[0]][pt[1]]]
            if the_basin not in basins:
                basins.append(the_basin)
    
    for ii in range(yy):
        for jj in range(xx):
            bb = [(ind, basin) for ind, basin in enumerate(basins) if (ii,jj) in basin]
            if len(bb) > 1:
                for b in bb[:0:-1]:
                    bb[0][1].extend(b[1])
                    basins.pop(b[0])
    basins = [np.unique(basin, axis=0) for basin in basins]
    return edge_msk, basins_msk, basins

def main():
    out = parse_input("input9.txt")
    msk = solve1(out)
    print(np.sum(out[msk]+1))
    
    edge, basins_msk, basins  = solve2(out)
    arr = np.array([len(basin) for basin in basins])
    print(sorted(arr)[::-1][:10])
    return out, msk, edge, basins
    
if __name__ == "__main__":
    out, msk, edge, basins = main()