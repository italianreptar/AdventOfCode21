# -*- coding: utf-8 -*-
"""
Created on Sat Dec 18 18:48:24 2021

@author: Connor
"""

def parse_input(filename):
    with open(filename, "r") as fh:
        lines = fh.readlines()
    txt = lines[0]
    xvals, yvals = txt[txt.find(":")+2:].split(", ")
    xmin, xmax = xvals[2:].split("..")
    ymin, ymax = yvals[2:].split("..")
    return ((int(xmin), int(xmax)), (int(ymin), int(ymax)))

def step(xx, yy, xx_dot, yy_dot):
    xx += xx_dot
    yy += yy_dot
    if xx_dot > 0:
        xx_dot -= 1
    yy_dot -= 1
    return xx, yy, xx_dot, yy_dot

def run_probe_sim(target_area, xx_dot, yy_dot):
    (xmin, xmax), (ymin, ymax) = target_area
    xx = 0
    yy = 0
    run_flag = True
    y_max = 0
    while run_flag:
        y_max = max(y_max, yy)
        xx, yy, xx_dot, yy_dot = step(xx, yy, xx_dot, yy_dot)
        if yy < ymin or xx > xmax:
            run_flag = False
        elif xx <= xmax and xx >= xmin and yy >= ymin and yy <= ymax:
            run_flag = False
        else:
            pass
    
    if yy < ymin or yy > ymax:
        yin = False
    else:
        yin = True
    if xx < xmin or xx > xmax:
        xin = False
    else:
        xin = True
    return xx, yy, y_max, xin, yin

def addtorial(value):
    return (value)*(value+1)*0.5

def solve1(target_area):
    (xmin, xmax), (ymin, ymax) = target_area
    yy_max = 0
    counter = 0
    for xv in range(17, 1000):
        for yv in range(-100, 1000):
            xx, yy, y_max, xin, yin = run_probe_sim(target_area, xv, yv)
            if xin and yin:
                counter += 1
                if y_max > yy_max:
                    yy_max = y_max
                    best_xv = xv
                    best_yv = yv
    return yy_max, best_xv, best_yv, counter

def main():
    target_area = parse_input("input17.txt")
    yy_max, best_xv, best_yv, counter = solve1(target_area)
    return yy_max, best_xv, best_yv, counter
    
    
if __name__ == "__main__":
    out = main()
    
    