# -*- coding: utf-8 -*-
"""
Created on Mon Dec 13 00:03:55 2021

@author: Connor
"""

import numpy as np
import matplotlib.pyplot as plt

def parse_input(filename):
    with open(filename, "r") as fh:
        lines = fh.readlines()
    
    pts = []
    folds = []
    for line in lines:
        ll = line.rstrip()
        if "," in ll:
            a,b = ll.split(",")
            pts.append([int(a), int(b)])
        if "=" in ll:
            a,b = ll.split("=")
            folds.append((a.split()[-1], int(b)))
            
    return pts, folds

def solve1(pts, folds):
    # Only need the first one
    for fold in folds[0:1]:
        for pi, pt in enumerate(pts):
            if fold[0] == "x" and pt[0] > fold[1]:
                # Flip over x
                pts[pi] = [fold[1] - (pt[0] - fold[1]), pt[1]]
            elif fold[0] == "y" and pt[1] > fold[1]:
                # Flip over y
                pts[pi] = [pt[0], fold[1] - (pt[1] - fold[1])]
            else:
                pass
    return pts

def solve2(pts, folds):
    for fold in folds:
        for pi, pt in enumerate(pts):
            if fold[0] == "x" and pt[0] > fold[1]:
                # Flip over x
                pts[pi] = [fold[1] - (pt[0] - fold[1]), pt[1]]
            elif fold[0] == "y" and pt[1] > fold[1]:
                # Flip over y
                pts[pi] = [pt[0], fold[1] - (pt[1] - fold[1])]
            else:
                pass
    return pts

def main():
    pts, folds = parse_input("input13.txt")
    pts1 = solve1(pts.copy(), folds)
    
    pts2 = solve2(pts.copy(), folds)
    return pts1, pts2
    
if __name__ == "__main__":
    pts1, pts2 = main()
    print(len(np.unique(sorted(pts1), axis=0)))
    
    # To manually decode the message:
    pp = np.array(pts2)
    plt.style.use("seaborn")
    plt.plot(pp[:,0], -pp[:,1], "o")
