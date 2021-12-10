# -*- coding: utf-8 -*-
"""
Created on Thu Dec  9 23:59:47 2021

@author: Connor
"""

score_table = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137
}

opens = ["(", "[", "{", "<"]

open_close = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">"
}

def parse_input(filename):
    with open(filename, "r") as fh:
        lines = fh.readlines()
    
    output = [line.rstrip() for line in lines]
    return output

def is_corrupted(line):
    last_openned = []
    for cc in line:
        if cc in opens:
            last_openned.append(cc)
        else:
            lo = last_openned[-1]
            if lo == opens[0] and cc == ")":
                last_openned.pop()
            elif lo == opens[1] and cc == "]":
                last_openned.pop()
            elif lo == opens[2] and cc == "}":
                last_openned.pop()
            elif lo == opens[3] and cc == ">":
                last_openned.pop()
            elif cc not in opens and cc != ")":
                return cc
            elif cc not in opens and cc != "]":
                return cc
            elif cc not in opens and cc != "}":
                return cc
            elif cc not in opens and cc != ">":
                return cc
            else:
                continue
         
def finish(line):
    last_openned = []
    for cc in line:
        if cc in opens:
            last_openned.append(cc)
        else:
            lo = last_openned[-1]
            if lo == opens[0] and cc == ")":
                last_openned.pop()
            elif lo == opens[1] and cc == "]":
                last_openned.pop()
            elif lo == opens[2] and cc == "}":
                last_openned.pop()
            elif lo == opens[3] and cc == ">":
                last_openned.pop()
            else:
                continue
    
    finish = []
    for ll in last_openned[::-1]:
        finish.append(open_close[ll])
    return finish
            
def solve1(lines):
    corr_lines = [is_corrupted(line) for line in lines if is_corrupted(line)]
    score = 0
    for cc in corr_lines:
        score += score_table[cc]
    return score

score_table2 = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4
}

def solve2(lines):
    inc_lines = [line for line in lines if not is_corrupted(line)]
    scores = []
    for ll in inc_lines:
        ff = finish(ll)
        score = 0
        for f in ff:
            score = (score*5) + score_table2[f]
        scores.append(score)
    return scores

def main():
    out = parse_input("input10.txt")
    score = solve1(out)
    print(score)
    oo = solve2(out)
    print(sorted(oo)[len(sorted(oo))//2])
    
if __name__ == "__main__":
    main()
