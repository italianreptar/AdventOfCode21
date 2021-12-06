# -*- coding: utf-8 -*-
"""
Created on Mon Dec  6 00:00:49 2021

@author: Connor
"""

import numpy as np
import matplotlib.pyplot as plt

# The bad way to solve it
class Fish():
    def __init__(self, value: int):
        self.value = value
    
    def __repr__(self):
        return f"{self.value}"
    
    def decrement(self):
        self.value -= 1
        if self.value == -1:
            self.value = 6
            return True
        else:
            return False

# Man this was dumb
def sim_day(fish):
    num_fish = len(fish)
    offset = 0
    for ii in range(num_fish):
        ff = fish[ii]
        if ff.decrement():
            fish[num_fish+offset] = Fish(8)
            offset+=1
    return fish

def parse_input(filename):
    with open(filename, "r") as fh:
        lines = fh.readlines()
    
    # each line becomes a line object
    fish = {}
    fish = {ii: Fish(int(value)) for ii, value in enumerate(lines[0].split(","))}
    return fish

# The good way to solve it
class School:
    def __init__(self, fish):
        self.school = np.zeros((9,))
        for key, ff in fish.items():
            self.school[ff.value] += 1
    
    def __repr__(self):
        return repr(self.school)
    
    def sim_day(self):
        school_a = np.roll(self.school[0:7], -1)
        tmp = self.school[7]
        school_b = np.roll(self.school[7:], -1)
        school_b[-1] = school_a[-1]
        school_a[-1] += tmp
        self.school = np.append(school_a, school_b)
        
def main():
    # The bad way to solve it:
    fish = parse_input("test_input6.txt")
    num_days = 18
    for i in range(num_days):
        fish = sim_day(fish)
    print(len(fish))

    # The right way!
    fish = parse_input("input6.txt")
    ss = School(fish)
    for i in range(num_days):
        ss.sim_day()
    print(np.sum(ss.school))
    
    xx = np.arange(0, 256, 1)
    yy = np.zeros(xx.shape)
    ss = School(fish)
    for i in range(256):
        ss.sim_day()
        yy[i] = np.sum(ss.school)
    print(np.sum(ss.school))
    
    plt.style.use("seaborn")
    plt.figure()
    plt.semilogy(xx, yy)
    plt.xlabel("Day Number")
    plt.ylabel("Number of Fish")
    
if __name__ == "__main__":
    main()
    