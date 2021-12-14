# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 00:03:02 2021

@author: Connor
"""

import numpy as np

def parse_input(filename):
    with open(filename, "r") as fh:
        lines = fh.readlines()
    
    insertions = []
    template = lines[0].rstrip()
    for line in lines[1:]:
        ll = line.rstrip()
        if "->" in ll:
            a, b = ll.split(" -> ")
            insertions.append((a, b))
            
    return template, insertions

def str_insert(string, idx, substr):
    return string[0:idx] + substr + string[idx:]

def solve1(tmp, inserts, num_steps=10):
    counts = []
    for step in range(num_steps):
        todos = list()
        for insert in inserts:
            ii = 0
            while insert[0] in tmp[ii:]:
                ii = tmp.find(insert[0], ii)+1
                todos.append((ii, insert[1]))
        todos = sorted(todos)[::-1]
        
        for todo in todos:
            tmp = str_insert(tmp, todo[0], todo[1])
            if todo[1] not in counts:
                counts.append(todo[1])
        
    vals = list()
    for count in counts:
        vals.append((tmp.count(count), count))

    vals = sorted(vals)
    print(vals[-1][0]-vals[0][0])
    return tmp, vals

def to_dict(tmp, inserts):
    tmp_d = {}
    counts = {}
    for insert in inserts:
        ii = 0
        tmp_d[insert[0]] = 0
    for i in range(len(tmp)-1):
        substr = tmp[i:i+2]
        tmp_d[substr] += 1
    for tt in tmp:
        if tt not in counts:
            counts[tt] = 1
        else:
            counts[tt] += 1
    return tmp_d, counts
            

def solve2(tmp, inserts, num_steps=2):
    tmp_d, counts = to_dict(tmp, inserts)
    for step in range(num_steps):
        decr = list()
        incr = list()
        
        for insert in inserts:
            if tmp_d[insert[0]]:
                decr.append((insert[0], tmp_d[insert[0]]))
                stra = insert[0][0] + insert[1]
                strb = insert[1] + insert[0][1]
                incr += [(stra, tmp_d[insert[0]]), (strb, tmp_d[insert[0]])]
                if insert[1] not in counts:
                    counts[insert[1]] = 1
                else:
                    counts[insert[1]] += tmp_d[insert[0]]
        
        for ii in incr:
            tmp_d[ii[0]] += ii[1]
        for dd in decr:
            tmp_d[dd[0]] -= dd[1]
            
    vals = list()
    for key, value in counts.items():
        vals.append((value, key))
    vals = sorted(vals)
    print(vals[-1][0]-vals[0][0])
    return tmp_d, counts
        

def main():
    tmp, inserts = parse_input("input14.txt")
    out, vals = solve1(tmp, inserts.copy(), 10)
    
    tmp_d, counts = solve2(tmp, inserts.copy(), 40)
    return tmp_d, counts
    
if __name__ == "__main__":
    tmp_d,  counts = main()
    
