# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 23:08:23 2021

@author: Connor
"""
import numpy as np

def parse_input(filename):
    with open(filename, "r") as fh:
        lines = fh.readlines()
    
    output = np.array([int(ll) for ll in lines])
    
    return output

def main():
    # Parse input input numpy array
    data = parse_input("input1.txt")
    
    # Determine the times the measurements increase
    delta = np.sum(np.diff(data)>0)
    print(delta)
    
    # Determine the times the sum of 3 measurements increase
    # Formulate summed array
    data2 = np.zeros(data.shape)
    for i in range(len(data)-2):
        data2[i] = data[i] + data[i+1] + data[i+2]
    
    # Determine the times the measurements increase
    delta2 = np.sum(np.diff(data2)>0)
    print(delta2)

if __name__ == "__main__":
    main()