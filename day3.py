# -*- coding: utf-8 -*-
"""
Created on Thu Dec  2 23:30:41 2021

@author: Connor
"""
import numpy as np

def parse_input(filename):
    with open(filename, "r") as fh:
        lines = fh.readlines()
    
    output = np.zeros((len(lines),(len(lines[0])-1)))

    for ii, line in enumerate(lines):
        for jj, cc in enumerate(line):
            if cc == "1":
                output[ii,jj] = 1
    
    return output

def arr_to_binary(arr):
    num = 0
    for ii, val in enumerate(arr[::-1]):
        if val:
            num += 2**ii
    return num

def num_to_bin_padded(num, pad):
    key = bin(num)
    key = '0b' + "0"*(pad-(len(key)-2)) + key[2:]
    return key

def get_value(out, common=True):
    i = 2
    while len(out) > 1:
        if common:
            vals = sum(out) >= np.shape(out)[0] / 2
        else:
            vals = sum(out) < np.shape(out)[0] / 2
            
        num = arr_to_binary(vals)
        key = num_to_bin_padded(num, len(vals))
        bit = key[i]
        if bit == "0":
            bb = 0
        else:
            bb = 1
        
        out = out[out[:,i-2]==bb,:]
        i += 1

    return out

def main():
    out = parse_input("input3.txt")
    gamma_rate = sum(out) >= np.shape(out)[0] / 2
    epsilon_rate = sum(out) < np.shape(out)[0] / 2
    num = arr_to_binary(gamma_rate)
    num2 = arr_to_binary(epsilon_rate)
    print(num*num2)
    
    ogr = get_value(out).flatten()
    csr = get_value(out, False).flatten()

    num = arr_to_binary(ogr)
    num2 = arr_to_binary(csr)
    print(num*num2)

if __name__ == "__main__":
    main()
    
    
    