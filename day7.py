# -*- coding: utf-8 -*-
"""
Created on Tue Dec  7 00:03:16 2021

@author: Connor
"""

import numpy as np
import matplotlib.pyplot as plt

def parse_input(filename):
    with open(filename, "r") as fh:
        lines = fh.readlines()
    
    output = np.array([int(ll) for ll in lines[0].split(",")])
    
    return output

def solve1(crabs):
    min_ind = 0
    min_val = np.inf
    for ii, crab in enumerate(crabs):
        val = np.sum(np.abs(crabs-ii))
        if val < min_val:
            min_ind = ii
            min_val = val
    return min_ind, min_val

def addtorial(value):
    return (value)*(value+1)*0.5

def solve2(crabs):
    min_ind = 0
    min_val = np.inf
    values = np.zeros(crabs.size)
    for ii, crab in enumerate(crabs):
        val = np.sum(np.array([addtorial(cc) for cc in np.abs(crabs-ii)]))
        values[ii] = val
        if val < min_val:
            min_ind = ii
            min_val = val
    return min_ind, min_val, values

def main():
    crabs = parse_input("input7.txt")
    min_ind, min_val = solve1(crabs)
    print(min_ind, min_val)
    
    min_ind, min_val, values = solve2(crabs)
    print(min_ind, min_val)
    
    plt.style.use("seaborn")
    plt.figure()
    plt.plot(values)
    plt.xlabel("Crab Position")
    plt.ylabel("Fuel Cost")
    plt.savefig("day7.png")
    
if __name__ == "__main__":
    main()