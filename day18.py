# -*- coding: utf-8 -*-
"""
Created on Sat Dec 18 19:47:42 2021

@author: Connor
"""

from itertools import product, permutations
from copy import deepcopy

def parse_input(filename):
    with open(filename, "r") as fh:
        lines = fh.readlines()
    
    out = []
    global ll
    ll = None
    for line in lines:
        exec("global ll; ll=" + line, globals(), locals())
        out.append(ll)
    return out


def max_depth(l):
    depths = []
    for item in l:
        if isinstance(item, list):
            depths.append(max_depth(item))
    if len(depths) > 0:
        return 1 + max(depths)
    return 1


def explodable(sfnum):
    return max_depth(sfnum) > 4

def flatten(list_of_lists):
    if len(list_of_lists) == 0:
        return list_of_lists
    if isinstance(list_of_lists[0], list):
        return flatten(list_of_lists[0]) + flatten(list_of_lists[1:])
    return list_of_lists[:1] + flatten(list_of_lists[1:])

def get_right(inds):
    if len(inds) == inds.count(1):
        return None
    else:
        inds_b = "".join(str(ii) for ii in inds)
        effective_ind = int(inds_b, 2)
        effective_ind += 1
        new_inds_b = bin(effective_ind)[2:].zfill(len(inds))
        out = tuple([int(bb) for bb in new_inds_b])
        return out

def get_left(inds):
    if len(inds) == inds.count(0):
        return None
    else:
        inds_b = "".join(str(ii) for ii in inds)
        effective_ind = int(inds_b, 2)
        effective_ind -= 1
        new_inds_b = bin(effective_ind)[2:].zfill(len(inds))
        out = tuple([int(bb) for bb in new_inds_b])
        return out

def try_to_set(inds, sfnum, value):
    try:
        sfnum[inds[0]][inds[1]][inds[2]][inds[3]] = value
    except:
        try:
            sfnum[inds[0]][inds[1]][inds[2]] = value
        except:
            try:
                sfnum[inds[0]][inds[1]] = value
            except:
                try:
                    sfnum[inds[0]] = value
                except:
                    pass
    return sfnum

def try_to_inc(inds, sfnum, value, r_or_l):
    try:
        if isinstance(sfnum[inds[0]][inds[1]][inds[2]][inds[3]], list):
            sfnum[inds[0]][inds[1]][inds[2]][inds[3]][r_or_l] += value
        else:
            sfnum[inds[0]][inds[1]][inds[2]][inds[3]] += value
    except:
        try:
            if isinstance(sfnum[inds[0]][inds[1]][inds[2]], list):
                sfnum[inds[0]][inds[1]][inds[2]][r_or_l] += value
            else:
                sfnum[inds[0]][inds[1]][inds[2]] += value
        except:
            try:
                if isinstance(sfnum[inds[0]][inds[1]], list):
                    sfnum[inds[0]][inds[1]][r_or_l] += value
                else:
                    sfnum[inds[0]][inds[1]] += value
            except:
                try:
                    if isinstance(sfnum[inds[0]], list):
                        sfnum[inds[0]][r_or_l] += value
                    else:
                        sfnum[inds[0]] += value
                except:
                    pass
    return sfnum

def explode(sfnum):
    def get_explodable(sfnum):
        out = sfnum.copy()
        # Left-most pair explodes
        for inds in product(range(2), repeat=max_depth(sfnum)-1):
            invalid_flag = False
            for ii in inds:
                try:
                    out = out[ii]
                except IndexError:
                    out = sfnum.copy()
                    invalid_flag = True
                except TypeError:
                    out = sfnum.copy()
                    invalid_flag = True
            if isinstance(out, list) and not invalid_flag:
                return out, inds
            else:
                out = sfnum.copy()
    
    to_explode, inds = get_explodable(sfnum)
    rr = get_right(inds)
    ll = get_left(inds)
    
    # explode
    out = sfnum.copy()
    out = try_to_set(inds, out, 0)
    out = try_to_inc(ll, out, to_explode[0], 1)
    out = try_to_inc(rr, out, to_explode[1], 0)
    return out

def splitable(sfnum):
    def get_max_num(sfnum):
        if isinstance(sfnum[0], list):
            ll = get_max_num(sfnum[0])
        else:
            ll = sfnum[0]
        
        if isinstance(sfnum[1], list):
            rr = get_max_num(sfnum[1])
        else:
            rr = sfnum[1]
        return ll if ll > rr else rr

    return get_max_num(sfnum) >= 10

def split(sfnum):
    def get_splitable(sfnum):
        out = sfnum.copy()
        # Left-most pair explodes
        for inds in product(range(2), repeat=max_depth(sfnum)):
            for ii in inds:
                try:
                    out = out[ii]
                except IndexError:
                    out = sfnum.copy()
                except TypeError:
                    if isinstance(out, int) and out >= 10:
                        return out, inds
            if isinstance(out, int) and out >= 10:
                return out, inds
            else:
                out = sfnum.copy()
    
    to_split, inds = get_splitable(sfnum)
    if to_split % 2 == 1:
        sp = [to_split // 2, to_split // 2 + 1]
    else:
        sp = [to_split // 2, to_split // 2 ]
    
    # explode
    out = sfnum.copy()
    try_to_set(inds, out, sp)
    
    return out

def sf_add(ll, rr):
    sfnum = [ll, rr]
    
    while explodable(sfnum) or splitable(sfnum):
        while explodable(sfnum):
            sfnum = explode(sfnum.copy())
        else:
            if splitable(sfnum):
                sfnum = split(sfnum.copy())
    return sfnum

def solve1(sfnums):
    while len(sfnums) > 1:
        ll = sfnums.pop(0)
        rr = sfnums.pop(0)
        
        new_sfnum = sf_add(ll, rr)
        sfnums.insert(0, new_sfnum)
    return sfnums[0]


def magnitude(sfnum):
    if isinstance(sfnum[0], list):
        ll = magnitude(sfnum[0])
    else:
        ll = sfnum[0]
    
    if isinstance(sfnum[1], list):
        rr = magnitude(sfnum[1])
    else:
        rr = sfnum[1]
    return 3*ll+2*rr

def solve2(sfnums):
    max_mag = 0
    for ll, rr in permutations(sfnums, 2):
        new_mag = magnitude(sf_add(deepcopy(ll), deepcopy(rr)))
        if new_mag > max_mag:
            max_mag = new_mag
    return max_mag

def main():
    # sfnums = parse_input("input18.txt")
    # sfnum = solve1(sfnums)
    # print(magnitude(sfnum))

    sfnums = parse_input("input18.txt")   
    mm = solve2(sfnums)
    print(mm)
    # return sfnum
    

if __name__ == "__main__":
    out = main()
