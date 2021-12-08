# -*- coding: utf-8 -*-
"""
Created on Tue Dec  7 23:55:37 2021

@author: Connor
"""

import numpy as np
import matplotlib.pyplot as plt

def parse_input(filename):
    with open(filename, "r") as fh:
        lines = fh.readlines()
    
    output = [(line.split(" | ")[0].split() ,line.split(" | ")[1].split()) for line in lines]
    
    return output

def solve1(inpt):
    count = 0
    for line in inpt:
        for num in line[1]:
            if len(num) == 7 or len(num) == 4 or len(num) == 3 or len(num) == 2:
                count += 1
    return count

class Digit:
    def __init__(self, string):
        self.string = string
        if len(string) == 7:
            self.digit = 8
        elif len(string) == 4:
            self.digit = 4
        elif len(string) == 3:
            self.digit = 7
        elif len(string) == 2:
            self.digit = 1
        else:
            if len(string) == 5:
                self.digit = None
            else:
                assert len(string) == 6
                self.digit = None
    
    def __repr__(self):
        return f"{self.digit}"
        
class Display:
    def __init__(self, code, digits):
        self.code = [Digit(item) for item in code]
        self.digits = [Digit(item) for item in digits]
        self.gen_decode_strings()
        self.decode()
    
    def __repr__(self):
        return f"| {self.digits} |"

    def gen_decode_strings(self):
        if len(self.code) != 10:
            raise ValueError("No")
        
        strings = [None for i in range(10)]
        for dig in self.code:
            if dig.digit == 1:
                strings[dig.digit] = dig.string
            elif dig.digit == 4:
                strings[dig.digit] = dig.string
            elif dig.digit == 7:
                strings[dig.digit] = dig.string
            elif dig.digit == 8:
                strings[dig.digit] = dig.string
            else:
                pass
        
        for dig in self.code:
            if len(dig.string) == 5:
                # can identify 3 here
                if np.sum(np.array([ss in dig.string for ss in strings[1]])) == 2:
                    strings[3] = dig.string
                    dig.digit = 3
                # can identify 2 here
                elif np.sum(np.array([ss in dig.string for ss in strings[4]])) == 2:
                    strings[2] = dig.string
                    dig.digit = 2
            elif len(dig.string) == 6:
                # Can get 6
                if np.sum(np.array([ss in dig.string for ss in strings[1]])) == 1:
                    strings[6] = dig.string
                    dig.digit = 6
                # Can get 9
                elif np.sum(np.array([ss in dig.string for ss in strings[4]])) == 4:
                    strings[9] = dig.string
                    dig.digit = 9
                # can identify 3 here
                elif np.sum(np.array([ss in dig.string for ss in strings[8]])) == 6:
                    strings[0] = dig.string
                    dig.digit = 0
        for dig in self.code:
            if len(dig.string) == 5 and dig.digit is None:
                dig.digit = 5
                strings[5] = dig.string
        self.strings = strings
    
    def decode(self):
        for dig in self.digits:
            for ii in range(0, 10):
                if sorted(dig.string) == sorted(self.strings[ii]):
                    dig.digit = ii
    
    def concat(self):
        return 1000*self.digits[0].digit + 100*self.digits[1].digit + 10*self.digits[2].digit + self.digits[3].digit
        

def solve2(digits_str):
    disp = []
    for line in digits_str:
        disp.append(Display(line[0], line[1]).concat())
    return disp

def main():
    out = parse_input("input8.txt")
    cnt = solve1(out)
    print(cnt)
    
    out = solve2(out)
    return out
    
if __name__ == "__main__":
    out = main()