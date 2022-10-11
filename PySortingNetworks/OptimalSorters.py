# SPDX-License-Identifier: Apache-2.0
# Copyright (C) 2022 Christoph Wiedemann
#
# THE PROGRAM IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND.
#

from PySortingNetworks.Base import BaseSortingNetwork

def sort2():
    res = BaseSortingNetwork(2)
    res.P(0, 1)
    return res

def sort3():
    res = BaseSortingNetwork(3)
    res.P(0, 2)
    res.P(1, 2)
    res.P(0, 1)
    return res

def sort4():
    res = BaseSortingNetwork(4)
    res.P(1, 3)
    res.P(0, 2)
    res.P(2, 3)
    res.P(0, 1)
    res.P(1, 2)
    return res

def sort5():
    res = BaseSortingNetwork(5)
    res.P(0, 4)
    res.P(2, 4)
    res.P(1, 3)
    res.P(0, 2)
    res.P(3, 4)
    res.P(1, 2)
    res.P(0, 3)
    res.P(2, 3)
    res.P(0, 1)
    return res

def sort6():
    res = BaseSortingNetwork(6)
    res.P(1, 5)
    res.P(0, 4)
    res.P(3, 5)
    res.P(2, 4)
    res.P(1, 3)
    res.P(0, 2)
    res.P(4, 5)
    res.P(2, 3)
    res.P(0, 1)
    res.P(1, 4)
    res.P(3, 4)
    res.P(1, 2)
    return res

def sort7():
    res = BaseSortingNetwork(7)
    res.P(2, 6)
    res.P(1, 5)
    res.P(0, 4)
    res.P(4, 6)
    res.P(3, 5)
    res.P(0, 2)
    res.P(2, 4)
    res.P(1, 3)
    res.P(5, 6)
    res.P(3, 4)
    res.P(1, 2)
    res.P(2, 5)
    res.P(0, 3)
    res.P(4, 5)
    res.P(2, 3)
    res.P(0, 1)
    return res

def sort8():
    return BaseSortingNetwork(8,
        [
            (3, 7),
            (2, 6),
            (1, 5),
            (0, 4),
            (5, 7),
            (4, 6),
            (1, 3),
            (0, 2),
            (3, 5),
            (2, 4),
            (6, 7),
            (4, 5),
            (2, 3),
            (0, 1),
            (3, 6),
            (1, 4),
            (5, 6),
            (3, 4), 
            (1, 2)
        ]
    )

def sort9():
    return BaseSortingNetwork(9,
        [
            (7,8),
            (4,5),
            (1,2),
            (6,7),
            (3,4),
            (0,1),
            (7,8),
            (4,5),
            (1,2),
            (3,6),
            (5,8),
            (4,7),
            (0,3),
            (2,5),
            (1,4),
            (3,6),
            (5,8),
            (4,7),
            (1,3),
            (2,6),
            (5,7),
            (2,4),
            (4,6),
            (2,3),
            (5,6)
        ]
    )

def sort10():
    return BaseSortingNetwork(10,
        [
            (0,5), (1,6), (2,7), (3,8), (4,9), (5,8), (0,3),
            (6,9), (1,4), (7,9), (3,6), (0,2), (8,9), (5,7),
            (2,4), (0,1), (7,8), (3,5), (1,2), (4,6), (1,2),
            (4,6), (4,7), (1,3), (6,8), (2,5), (6,7), (2,3),
            (5,6), (3,4), (4,5)
        ]
    )
        
def sort(n):
    if n == 1:
        return BaseSortingNetwork(1)
    if n == 2:
        return sort2()
    if n == 3:
        return sort3()
    if n == 4:
        return sort4()
    if n == 5:
        return sort5()
    if n == 6:
        return sort6()
    if n == 7:
        return sort7()
    if n == 8:
        return sort8()
    if n == 9:
        return sort9()
    if n == 10: 
        return sort10()
    raise RuntimeError("optimal sorting network for n=%d is unknown" % n)

if __name__ == "__main__":
    from itertools import product
    for n in range(1,11):
        sn = sort(n)
        print("Sort(",n,"): operations=", sn.nops())
        print(sn)
        passed, failed = sn.test(product(*([[0,1]]*n)), lambda d_in, d_out: print(d_in, d_out))
        print("Test result: passed:", passed, "failed:", failed)
        assert failed == 0
