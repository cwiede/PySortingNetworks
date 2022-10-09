from itertools import product
from PySortingNetworks.Base import BaseSortingNetwork
from PySortingNetworks.Batcher import batcher_merge
from PySortingNetworks.OptimalSorters import sort
from PySortingNetworks import AutoCompleter

def merge2x7():
    def geninputs():
        for n1, n2 in product(list(range(8)), list(range(8))):
            d_in = [0]*(7-n1) + [1]*n1 + [0]*(7-n2) + [1]*n2
            yield d_in
    res = BaseSortingNetwork(0)
    res.section("input sorter")
    res = BaseSortingNetwork.append(res, sort(7))
    res = BaseSortingNetwork.append(res, BaseSortingNetwork.relabel(sort(7), list(range( 7,14))))
    res.section("merge")
    for i in range(7):
        res.P(i, 7+i)
    best = None
    for i in range(50):
        if i == 0:
            sn = AutoCompleter.greedy(res, geninputs)
        else:
            sn = AutoCompleter.randbest5(res, geninputs)
        if best is None or sn.nops() < best.nops():
            best = sn
    best.prune(geninputs, ["merge"])
    best.focus(["merge"])
    return best

def from_scratch(premerge = False):
    # optimal sorters for the 5x5 inputs
    res = sort(7)
    res = BaseSortingNetwork.append(res, BaseSortingNetwork.relabel(sort(7), list(range( 7,14))))
    res = BaseSortingNetwork.append(res, BaseSortingNetwork.relabel(sort(7), list(range(14,21))))
    res = BaseSortingNetwork.append(res, BaseSortingNetwork.relabel(sort(7), list(range(21,28))))
    res = BaseSortingNetwork.append(res, BaseSortingNetwork.relabel(sort(7), list(range(28,35))))
    res = BaseSortingNetwork.append(res, BaseSortingNetwork.relabel(sort(7), list(range(35,42))))
    res = BaseSortingNetwork.append(res, BaseSortingNetwork.relabel(sort(7), list(range(42,49))))
    res.sections = [("input sorters", 0)]
    res.section("merge 2 of the sorted 7 lists to sorted 14 lists")
    if premerge:
        m2x7 = merge2x7()
        print("Merge 2 sorted lists, Number of operations:", m2x7.nops())
        print(m2x7)
        res = BaseSortingNetwork.append(res, m2x7)
        res = BaseSortingNetwork.append(res, BaseSortingNetwork.relabel(m2x7, list(range(14,28))))
        res = BaseSortingNetwork.append(res, BaseSortingNetwork.relabel(m2x7, list(range(35,49))))

    res.section("final merging network")
    # intermediate layer
    res = BaseSortingNetwork.append(res, BaseSortingNetwork.relabel(sort(7), [ 0, 7,14,21,28,35,42]))
    res = BaseSortingNetwork.append(res, BaseSortingNetwork.relabel(sort(7), [ 1, 8,15,22,29,36,43]))
    res = BaseSortingNetwork.append(res, BaseSortingNetwork.relabel(sort(7), [ 2, 9,16,23,30,37,44]))
    res = BaseSortingNetwork.append(res, BaseSortingNetwork.relabel(sort(7), [ 3,10,17,24,31,38,45]))
    res = BaseSortingNetwork.append(res, BaseSortingNetwork.relabel(sort(7), [ 4,11,18,25,32,39,46]))
    res = BaseSortingNetwork.append(res, BaseSortingNetwork.relabel(sort(7), [ 5,12,19,26,33,40,47]))
    res = BaseSortingNetwork.append(res, BaseSortingNetwork.relabel(sort(7), [ 6,13,20,27,34,41,48]))
    
    print("Incomplete base network: ", res.nops())
    print(res)
    
    # trial and error for the remaining network
    def geninputs():
        for n1, n2, n3, n4, n5, n6, n7 in product(list(range(8)), list(range(8)), list(range(8)), list(range(8)), list(range(8)), list(range(8)), list(range(8))):
            d_in = ([0]*(7-n1) + [1]*n1 + 
                    [0]*(7-n2) + [1]*n2 + 
                    [0]*(7-n3) + [1]*n3 + 
                    [0]*(7-n4) + [1]*n4 + 
                    [0]*(7-n5) + [1]*n5 + 
                    [0]*(7-n6) + [1]*n6 + 
                    [0]*(7-n7) + [1]*n7)
            yield d_in

    best = None
    nodeOfInterest = list(range(24, 49))
    for i in range(2):
        if i == 0:
            sn = AutoCompleter.greedy(res, geninputs, maxNumSuggestsToTry=3, doprint=True)
        else:
            sn = AutoCompleter.randbest5(res, geninputs, doprint=False)
        print("greedy network completed:", sn.nops(), sn.nops(nodeOfInterest))
        sn.prune(geninputs, ["final merging network"])
        sn.normalize("lower_indices_last", ["final merging network"])
        print("ops after pruning:", sn.nops(), sn.nops(nodeOfInterest))
        if best is None or sn.nops(nodeOfInterest) < best.nops(nodeOfInterest) or (sn.nops(nodeOfInterest) == best.nops(nodeOfInterest) and sn.nops() < best.nops()):
            best = sn
            print("Current best:", best.nops())
            print(best)
    passed,failed = best.test(geninputs())
    print("passed", passed, "failed", failed)
    
    return best

def batcher():
    # optimal sorters for the 5x5 inputs
    res = sort(7)
    for i in range(1,7):
        res = BaseSortingNetwork.append(res, BaseSortingNetwork.relabel(sort(7), list(range( 7*i,7*i+7))))
    res.sections = [("input sorters", 0)]
    res.section("merge")
    m77 = batcher_merge(7, 7)
    for i in range(3):
        res = BaseSortingNetwork.append(res, BaseSortingNetwork.relabel(m77, list(range(i*14, i*14+14))))
    # now we have [0..14], [14..28], [28..42] and [42..49] all sorted
    res = BaseSortingNetwork.append(res, batcher_merge(14,14))
    res = BaseSortingNetwork.append(res, BaseSortingNetwork.relabel(batcher_merge(14, 7), list(range(28,49))))
    res = BaseSortingNetwork.append(res, batcher_merge(28,21))
    def geninputs():
        for n1, n2, n3, n4, n5, n6, n7 in product(list(range(8)), list(range(8)), list(range(8)), 
                                                  list(range(8)), list(range(8)), list(range(8)), list(range(8))):
            d_in = ([0]*(7-n1) + [1]*n1 + 
                    [0]*(7-n2) + [1]*n2 + 
                    [0]*(7-n3) + [1]*n3 + 
                    [0]*(7-n4) + [1]*n4 + 
                    [0]*(7-n5) + [1]*n5 + 
                    [0]*(7-n6) + [1]*n6 + 
                    [0]*(7-n7) + [1]*n7)
            yield d_in    
    res.prune(geninputs, ["merge"])
    res.normalize("lower_indices_last", ["merge"])
    return res
    

def best_known():
    # nops = 405, median filter loop operations 295
    return BaseSortingNetwork(
        n=49, 
        ops=[(2, 6), (1, 5), (0, 4), (4, 6), (3, 5), (0, 2), (2, 4), (1, 3), (5, 6), (3, 4), (1, 2), (2, 5), (0, 3), (4, 5), (2, 3), (0, 1), (9, 13), (8, 12), (7, 11), (11, 13), (10, 12), (7, 9), (9, 11), (8, 10), (12, 13), (10, 11), (8, 9), (9, 12), (7, 10), (11, 12), (9, 10), (7, 8), (16, 20), (15, 19), (14, 18), (18, 20), (17, 19), (14, 16), (16, 18), (15, 17), (19, 20), (17, 18), (15, 16), (16, 19), (14, 17), (18, 19), (16, 17), (14, 15), (23, 27), (22, 26), (21, 25), (25, 27), (24, 26), (21, 23), (23, 25), (22, 24), (26, 27), (24, 25), (22, 23), (23, 26), (21, 24), (25, 26), (23, 24), (21, 22), (30, 34), (29, 33), (28, 32), (32, 34), (31, 33), (28, 30), (30, 32), (29, 31), (33, 34), (31, 32), (29, 30), (30, 33), (28, 31), (32, 33), (30, 31), (28, 29), (37, 41), (36, 40), (35, 39), (39, 41), (38, 40), (35, 37), (37, 39), (36, 38), (40, 41), (38, 39), (36, 37), (37, 40), (35, 38), (39, 40), (37, 38), (35, 36), (44, 48), (43, 47), (42, 46), (46, 48), (45, 47), (42, 44), (44, 46), (43, 45), (47, 48), (45, 46), (43, 44), (44, 47), (42, 45), (46, 47), (44, 45), (42, 43), (33, 41), (32, 40), (31, 39), (29, 37), (33, 37), (37, 39), (30, 38), (34, 38), (38, 40), (40, 41), (38, 39), (28, 36), (32, 36), (34, 36), (36, 37), (31, 35), (33, 35), (34, 35), (34, 42), (30, 32), (32, 33), (32, 48), (40, 48), (29, 31), (30, 31), (31, 47), (39, 47), (30, 46), (38, 46), (38, 42), (30, 34), (28, 29), (28, 44), (36, 44), (40, 44), (44, 46), (29, 45), (37, 45), (41, 45), (45, 47), (47, 48), (45, 46), (35, 43), (39, 43), (41, 43), (43, 44), (40, 42), (41, 42), (32, 36), (36, 38), (33, 37), (37, 39), (39, 40), (37, 38), (31, 35), (33, 35), (35, 36), (32, 34), (33, 34), (29, 31), (31, 32), (28, 30), (29, 30), (19, 27), (18, 26), (17, 25), (15, 23), (19, 23), (23, 25), (16, 24), (20, 24), (24, 26), (26, 27), (24, 25), (14, 22), (18, 22), (20, 22), (22, 23), (17, 21), (19, 21), (20, 21), (16, 18), (18, 19), (15, 17), (16, 17), (14, 15), (5, 13), (4, 12), (3, 11), (1, 9), (5, 9), (9, 11), (2, 10), (6, 10), (10, 12), (12, 13), (10, 11), (11, 27), (10, 26), (0, 8), (4, 8), (6, 8), (8, 9), (8, 24), (3, 7), (5, 7), (6, 7), (6, 22), (6, 14), (2, 4), (4, 5), (1, 3), (2, 3), (2, 18), (10, 18), (18, 22), (4, 20), (12, 20), (20, 24), (24, 26), (9, 25), (7, 23), (20, 22), (3, 19), (11, 19), (19, 23), (5, 21), (13, 21), (21, 25), (25, 27), (25, 26), (21, 23), (23, 24), (21, 22), (10, 14), (2, 6), (0, 1), (0, 16), (8, 16), (12, 16), (16, 18), (1, 17), (9, 17), (13, 17), (17, 19), (19, 20), (17, 18), (7, 15), (11, 15), (13, 15), (15, 16), (16, 48), (12, 14), (13, 14), (4, 8), (8, 10), (5, 9), (9, 11), (11, 12), (12, 44), (12, 28), (9, 10), (3, 7), (5, 7), (7, 8), (4, 6), (5, 6), (1, 3), (3, 4), (4, 36), (20, 36), (36, 44), (8, 40), (24, 40), (40, 48), (14, 46), (40, 44), (6, 38), (22, 38), (38, 46), (10, 42), (26, 42), (42, 46), (46, 48), (15, 47), (13, 45), (42, 44), (20, 28), (4, 12), (0, 2), (0, 32), (16, 32), (24, 32), (32, 36), (14, 30), (22, 30), (24, 28), (8, 16), (16, 20), (6, 14), (8, 12), (0, 4), (1, 2), (2, 34), (18, 34), (26, 34), (34, 38), (38, 40), (5, 37), (21, 37), (37, 45), (9, 41), (25, 41), (41, 45), (7, 39), (23, 39), (39, 47), (11, 43), (27, 43), (43, 47), (47, 48), (43, 45), (45, 46), (43, 44), (34, 36), (1, 33), (17, 33), (25, 33), (33, 37), (3, 35), (19, 35), (27, 35), (35, 39), (39, 41), (41, 42), (39, 40), (35, 37), (37, 38), (35, 36), (26, 30), (30, 32), (15, 31), (23, 31), (27, 31), (31, 33), (33, 34), (31, 32), (13, 29), (21, 29), (25, 29), (27, 29), (29, 30), (26, 28), (27, 28), (10, 18), (18, 22), (22, 24), (18, 20), (9, 17), (17, 21), (11, 19), (19, 23), (23, 25), (25, 26), (23, 24), (19, 21), (21, 22), (19, 20), (10, 14), (14, 16), (7, 15), (11, 15), (15, 17), (17, 18), (15, 16), (5, 13), (9, 13), (11, 13), (13, 14), (10, 12), (11, 12), (2, 6), (6, 8), (3, 7), (7, 9), (9, 10), (7, 8), (1, 5), (3, 5), (5, 6), (2, 4), (3, 4), (1, 2)], 
        sections=[('input sorters', 0), ('merge', 112)]
    )

if __name__ == "__main__":
    if True:
        s7x7 = best_known()
    elif True:
        s7x7 = batcher()
    else:
        s7x7 = from_scratch(premerge=False)
    print("Number of operations", s7x7.nops())
    print("Operations in 7x7median filter loop", s7x7.nops(list(range(14, 59))) - 16*6)
    print(s7x7)
    def geninputs():
        for n1, n2, n3, n4, n5, n6, n7 in product(list(range(8)), list(range(8)), list(range(8)), 
                                                  list(range(8)), list(range(8)), list(range(8)), list(range(8))):
            d_in = ([0]*(7-n1) + [1]*n1 + 
                    [0]*(7-n2) + [1]*n2 + 
                    [0]*(7-n3) + [1]*n3 + 
                    [0]*(7-n4) + [1]*n4 + 
                    [0]*(7-n5) + [1]*n5 + 
                    [0]*(7-n6) + [1]*n6 + 
                    [0]*(7-n7) + [1]*n7)
            yield d_in    
    passed, failed = s7x7.test(geninputs())
    print("passed", passed, "failed", failed)
