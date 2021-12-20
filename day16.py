# -*- coding: utf-8 -*-
"""
Created on Thu Dec 16 18:08:51 2021

@author: Connor

NOTE: Is this code messy as all hell?
Yep
Is this code functioning?
Oh yes.
"""

import numpy as np

def parse_input(filename):
    with open(filename, "r") as fh:
        lines = fh.readlines()
    
    vals = [bin(int("0x"+cc, 16))[2:].zfill(4) for cc in lines[0].strip()]
    return "".join(vals)

def product(ll):
    out = 1
    for item in ll:
        out *= item
    return out

def parse_literal(bits, ind=0):
    # literal value
    c = bits[ind]
    ind += 1
    vals = ""
    while int(c):
        vals += bits[ind:ind+4]
        c = bits[ind+4]
        ind += 5
    vals += bits[ind:ind+4]
    value = int(vals, 2)
    
    # Cut off the bit of bits we used
    bits = bits[ind+4:]
    return bits, value

def parse_subpackets_l(bits, l=0):
    ii = 0
    values = list()
    versions = list()
    while ii < l:
        ind = 0
        V = int(bits[ind:ind+3], 2)
        versions.append(V)
        T = int(bits[ind+3:ind+6], 2)
        ind += 6
        ii += 6
        if T == 4:
            bits = bits[ind:]
            init_bits_len = len(bits)
            bits, value = parse_literal(bits)
            ii += init_bits_len - len(bits)
            values.append(value)
        else:
            # Operator
            I = int(bits[ind])
            ind += 1
            ii += 1
            if I:
                # next 11 bits are a number that represents the number of 
                # subpackets immediately contained by this packet
                L = int(bits[ind:ind+11], 2)
                ind += 11
                ii += 11
                bits = bits[ind:]
                init_bits_len = len(bits)
                bits, vals, vers = parse_n_subpackets(bits, n=L)
                ii += init_bits_len - len(bits)
                versions.extend(vers)
            else:
                # next 15 bits are a number that represents the total length
                # in bits of the subpackets contains by this packet.
                L = int(bits[ind:ind+15], 2)
                ind += 15
                ii += 15
                bits = bits[ind:]
                init_bits_len = len(bits)
                bits, vals, vers = parse_subpackets_l(bits, l=L)
                ii += init_bits_len - len(bits)
                versions.extend(vers)
            if T == 0:
                vals = [sum(vals)]
            elif T == 1:
                vals = [product(vals)]
            elif T == 2:
                vals = [min(vals)]
            elif T == 3:
                vals = [max(vals)]
            elif T == 5:
                vals = [1 if vals[0] > vals[1] else 0]
            elif T == 6:
                vals = [1 if vals[0] < vals[1] else 0]
            elif T == 7:
                vals = [1 if vals[0] == vals[1] else 0]
            else:
                pass
            values.extend(vals)
    return bits, values, versions

def parse_n_subpackets(bits, n=0):
    values = list()
    versions = list()
    for ii in range(n):
        ind = 0
        V = int(bits[ind:ind+3], 2)
        versions.append(V)
        T = int(bits[ind+3:ind+6], 2)
        ind += 6
        if T == 4:
            bits = bits[ind:]
            init_bits_len = len(bits)
            bits, value = parse_literal(bits)
            values.append(value)
        else:
            # Operator
            I = int(bits[ind])
            ind += 1
            if I:
                # next 11 bits are a number that represents the number of 
                # subpackets immediately contained by this packet
                L = int(bits[ind:ind+11], 2)
                ind += 11
                bits = bits[ind:]
                ind = 0
                bits, vals, vers = parse_n_subpackets(bits, n=L)
                versions.extend(vers)
            else:
                # next 15 bits are a number that represents the total length
                # in bits of the subpackets contains by this packet.
                L = int(bits[ind:ind+15], 2)
                ind += 15
                bits = bits[ind:]
                ind = 0
                bits, vals, vers = parse_subpackets_l(bits, l=L)
                versions.extend(vers)
            if T == 0:
                vals = [sum(vals)]
            elif T == 1:
                vals = [product(vals)]
            elif T == 2:
                vals = [min(vals)]
            elif T == 3:
                vals = [max(vals)]
            elif T == 5:
                vals = [1 if vals[0] > vals[1] else 0]
            elif T == 6:
                vals = [1 if vals[0] < vals[1] else 0]
            elif T == 7:
                vals = [1 if vals[0] == vals[1] else 0]
            else:
                pass
            values.extend(vals)
    return bits, values, versions

def parse_packets(bits, ind=0):
    V = int(bits[ind:ind+3], 2)
    T = int(bits[ind+3:ind+6], 2)
    ind += 6
    versions = list()
    values = list()
    versions.append(V)
    if T == 4:
        bits = bits[ind:]
        init_bits_len = len(bits)
        bits, value = parse_literal(bits)
        values.append(value)
    else:
        # Operator
        I = int(bits[ind])
        ind += 1
        if I:
            # next 11 bits are a number that represents the number of 
            # subpackets immediately contained by this packet
            L = int(bits[ind:ind+11], 2)
            ind += 11
            bits = bits[ind:]
            bits, values, vers = parse_n_subpackets(bits, n=L)
            versions.extend(vers)
        else:
            # next 15 bits are a number that represents the total length
            # in bits of the subpackets contains by this packet.
            L = int(bits[ind:ind+15], 2)
            ind += 15
            bits = bits[ind:]
            ind = 0
            bits, values, vers = parse_subpackets_l(bits, l=L)
            versions.extend(vers)
        if T == 0:
            values = [sum(values)]
        elif T == 1:
            values = [product(values)]
        elif T == 2:
            values = [min(values)]
        elif T == 3:
            values = [max(values)]
        elif T == 5:
            values = [1 if values[0] > values[1] else 0]
        elif T == 6:
            values = [1 if values[0] < values[1] else 0]
        elif T == 7:
            values = [1 if values[0] == values[1] else 0]
        else:
            pass
    
    return bits, values, versions

def solve1(bits):
    values = list()
    versions = list()
    while len(bits) > 11:
        bits, p_values, versions = parse_packets(bits)
        values.extend(p_values)
    return bits, values, versions

def main():
    bits = parse_input("input16.txt")
    return solve1(bits)
    
    
if __name__ == "__main__":
    bits = main()
    # vals = [bin(int("0x"+cc,16))[2:].zfill(4) for cc in "D2FE28"]
    # vals = [bin(int("0x"+cc,16))[2:].zfill(4) for cc in "38006F45291200"]
    # vals = [bin(int("0x"+cc,16))[2:].zfill(4) for cc in "EE00D40C823060"]
    # vals = [bin(int("0x"+cc,16))[2:].zfill(4) for cc in "8A004A801A8002F478"]
    # vals = [bin(int("0x"+cc,16))[2:].zfill(4) for cc in "620080001611562C8802118E34"]
    # vals = [bin(int("0x"+cc,16))[2:].zfill(4) for cc in "C0015000016115A2E0802F182340"]
    # vals = [bin(int("0x"+cc,16))[2:].zfill(4) for cc in "A0016C880162017C3686B18A3D4780"]
    
    # Part 2
    vals = [bin(int("0x"+cc,16))[2:].zfill(4) for cc in "C200B40A82"]
    vals = [bin(int("0x"+cc,16))[2:].zfill(4) for cc in "9C0141080250320F1802104A08"]
    test = "".join(vals)
    out = solve1(test)
    