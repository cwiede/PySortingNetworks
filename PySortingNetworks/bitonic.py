# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2022 Christoph Wiedemann
#
# THE PROGRAM IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND.
#

from itertools import product
from PySortingNetworks.Base import BaseSortingNetwork
from PySortingNetworks.OptimalSorters import sort

ASCENDING=True
DESCENDING=False

def next_power2(n):
    res = 1
    while res < n:
        res *= 2
    return res

def bitonic_sort(n, direction=ASCENDING):
    if n <= 1:
        return BaseSortingNetwork(n)
    m = n//2
    bs1 = bitonic_sort(m, not direction)
    bs2 = bitonic_sort(n-m, direction)
    res = BaseSortingNetwork.append(bs1, BaseSortingNetwork.relabel(bs2, list(range(m, n))))
    m = bitonic_merge(n, direction)
    res = BaseSortingNetwork.append(res, m)
    return res
    
def bitonic_merge(n, direction):
    if n <= 1:
        return BaseSortingNetwork(n)
    res = BaseSortingNetwork(n)
    m = next_power2(n) // 2
    for i in range(n-m):
        if direction == ASCENDING:
            res.P(i, i+m)
        else:
            res.P(i+m, i)
    m1 = bitonic_merge(m, direction)
    m2 = bitonic_merge(n-m, direction)
    res = BaseSortingNetwork.append(res, m1)
    res = BaseSortingNetwork.append(res, BaseSortingNetwork.relabel(m2, list(range(m, n))))
    return res
    
if __name__ == "__main__":
    for n in range(26):
        sn = bitonic_sort(n)
        print("Bitonic", n, "Num Operations:", sn.nops())
        print(sn)
        def geninput(n):
            for i in product(*([[0,1]]*n)):
                yield i
        passed, failed = sn.test(geninput(n))
        print("Test passed", passed, "failed", failed)
        assert failed == 0
        
