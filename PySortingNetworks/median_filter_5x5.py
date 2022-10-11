from itertools import product
from PySortingNetworks.Base import BaseSortingNetwork
from PySortingNetworks.Batcher import batcher_merge
from PySortingNetworks.OptimalSorters import sort
from PySortingNetworks import AutoCompleter

def merge2x5():
    def geninputs():
        for n1, n2 in product(list(range(6)), list(range(6))):
            d_in = [0]*(5-n1) + [1]*n1 + [0]*(5-n2) + [1]*n2
            yield d_in
    res = BaseSortingNetwork(0)
    res.section("input sorter")
    res = BaseSortingNetwork.append(res, sort(5))
    res = BaseSortingNetwork.append(res, BaseSortingNetwork.relabel(sort(5), list(range( 5,10))))
    res.section("merge")
    for i in range(5):
        res.P(i, 5+i)
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
    res = sort(5)
    res = BaseSortingNetwork.append(res, BaseSortingNetwork.relabel(sort(5), list(range( 5,10))))
    res = BaseSortingNetwork.append(res, BaseSortingNetwork.relabel(sort(5), list(range(10,15))))
    res = BaseSortingNetwork.append(res, BaseSortingNetwork.relabel(sort(5), list(range(15,20))))
    res = BaseSortingNetwork.append(res, BaseSortingNetwork.relabel(sort(5), list(range(20,25))))
    res.sections = [("input sorters", 0)]
    res.section("merge 2 of the sorted 5 lists to sorted 10 lists")
    if premerge:
        m2x5 = merge2x5()
        print("Merge 2 sorted lists, Number of operations:", m2x5.nops())
        print(m2x5)
        res = BaseSortingNetwork.append(res, m2x5)
        res = BaseSortingNetwork.append(res, BaseSortingNetwork.relabel(m2x5, list(range(15,25))))

    res.section("final merging network")
    # intermediate layer
    res = BaseSortingNetwork.append(res, BaseSortingNetwork.relabel(sort(5), [ 0, 5,10,15,20]))
    res = BaseSortingNetwork.append(res, BaseSortingNetwork.relabel(sort(5), [ 1, 6,11,16,21]))
    res = BaseSortingNetwork.append(res, BaseSortingNetwork.relabel(sort(5), [ 2, 7,12,17,22]))
    res = BaseSortingNetwork.append(res, BaseSortingNetwork.relabel(sort(5), [ 3, 8,13,18,23]))
    res = BaseSortingNetwork.append(res, BaseSortingNetwork.relabel(sort(5), [ 4, 9,14,19,24]))
    
    print("Incomplete base network: ", res.nops())
    print(res)
    
    # trial and error for the remaining network
    def geninputs():
        for n1, n2, n3, n4, n5 in product(list(range(6)), list(range(6)), list(range(6)), list(range(6)), list(range(6))):
            d_in = ([0]*(5-n1) + [1]*n1 + 
                    [0]*(5-n2) + [1]*n2 + 
                    [0]*(5-n3) + [1]*n3 + 
                    [0]*(5-n4) + [1]*n4 + 
                    [0]*(5-n5) + [1]*n5)
            yield d_in

    best = None
    nodeOfInterest = list(range(12, 25))
    for i in range(30):
        if i == 0:
            sn = AutoCompleter.greedy(res, geninputs, doprint=False)
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

def second_best():
    """
    This network has additional structure which might exploited in median filtering, however it will make the
    SW more complicated, especially for SIMD.
    """
    return BaseSortingNetwork(
        n=25, 
        ops=[(0, 4), (2, 4), (1, 3), (0, 2), (3, 4), (1, 2), (0, 3), (2, 3), (0, 1), (5, 9), (7, 9), (6, 8), 
             (5, 7), (8, 9), (6, 7), (5, 8), (7, 8), (5, 6), (10, 14), (12, 14), (11, 13), (10, 12), (13, 14), 
             (11, 12), (10, 13), (12, 13), (10, 11), (15, 19), (17, 19), (16, 18), (15, 17), (18, 19), (16, 17), 
             (15, 18), (17, 18), (15, 16), (20, 24), (22, 24), (21, 23), (20, 22), (23, 24), (21, 22), (20, 23), 
             (22, 23), (20, 21), (0, 5), (1, 6), (2, 7), (3, 8), (4, 9), (4, 5), (5, 7), (3, 6), (5, 6), (2, 4), 
             (1, 2), (3, 4), (7, 8), (15, 20), (16, 21), (17, 22), (18, 23), (19, 24), (19, 20), (20, 22), 
             (18, 21), (20, 21), (17, 19), (16, 17), (18, 19), (22, 23), (14, 24), (13, 23), (12, 22), (11, 21), 
             (10, 20), (5, 15), (15, 20), (6, 16), (16, 21), (7, 17), (17, 22), (8, 18), (18, 23), (9, 19), 
             (19, 24), (0, 10), (5, 10), (10, 15), (1, 11), (6, 11), (11, 16), (2, 12), (7, 12), (12, 17), 
             (3, 13), (8, 13), (13, 18), (4, 14), (9, 14), (14, 19), (19, 22), (22, 23), (14, 20), (12, 16), 
             (14, 16), (16, 17), (13, 15), (15, 16), (16, 21), (18, 21), (19, 21), (17, 20), (19, 20), (20, 21), 
             (21, 22), (18, 19), (17, 18), (4, 9), (9, 13), (12, 13), (9, 12), (9, 11), (4, 10), (3, 8), 
             (8, 10), (10, 11), (11, 12), (12, 14), (13, 14), (14, 15), (15, 16), (16, 17), (13, 14), (2, 7), 
             (7, 9), (8, 9), (9, 10), (10, 11), (7, 8), (1, 6), (3, 6), (4, 6), (6, 7), (7, 8), (8, 9), (0, 5), 
             (2, 5), (4, 5), (3, 4), (4, 5), (5, 6), (1, 3), (1, 2)], 
        sections=[('input sorters', 0), ('merge 2 of the sorted 5 lists to sorted 10 lists', 45), ('final merging network', 71)]
    )
    
def batcher():
    # optimal sorters for the 5x5 inputs
    res = sort(5)
    res = BaseSortingNetwork.append(res, BaseSortingNetwork.relabel(sort(5), list(range( 5,10))))
    res = BaseSortingNetwork.append(res, BaseSortingNetwork.relabel(sort(5), list(range(10,15))))
    res = BaseSortingNetwork.append(res, BaseSortingNetwork.relabel(sort(5), list(range(15,20))))
    res = BaseSortingNetwork.append(res, BaseSortingNetwork.relabel(sort(5), list(range(20,25))))
    res.sections = [("input sorters", 0)]
    res.section("merge")
    m55 = batcher_merge(5, 5)
    print("merge5x5", m55)
    res = BaseSortingNetwork.append(res, m55)
    res = BaseSortingNetwork.append(res, BaseSortingNetwork.relabel(m55, list(range(15, 25))))
    # now we have [0..10], [10..15] and [15..25] all sorted, we merge [10..25] and afterwards we merge [0..25]
    m105 = batcher_merge(5, 10)
    res = BaseSortingNetwork.append(res, BaseSortingNetwork.relabel(m105, list(range(10, 25))))
    res = BaseSortingNetwork.append(res, batcher_merge(10, 15))
    def geninputs():
        for n1, n2, n3, n4, n5 in product(list(range(6)), list(range(6)), list(range(6)), list(range(6)), list(range(6))):
            d_in = ([0]*(5-n1) + [1]*n1 + 
                    [0]*(5-n2) + [1]*n2 + 
                    [0]*(5-n3) + [1]*n3 + 
                    [0]*(5-n4) + [1]*n4 + 
                    [0]*(5-n5) + [1]*n5)
            yield d_in    
    res.prune(geninputs, ["merge"])
    res.normalize("lower_indices_last", ["merge"])
    return res
    
def best_known():
    return BaseSortingNetwork(
        n=25, 
        ops=[(0, 4), (2, 4), (1, 3), (0, 2), (3, 4), (1, 2), (0, 3), (2, 3), (0, 1), (5, 9), (7, 9), (6, 8), 
             (5, 7), (8, 9), (6, 7), (5, 8), (7, 8), (5, 6), (10, 14), (12, 14), (11, 13), (10, 12), (13, 14), 
             (11, 12), (10, 13), (12, 13), (10, 11), (15, 19), (17, 19), (16, 18), (15, 17), (18, 19), (16, 17), 
             (15, 18), (17, 18), (15, 16), (20, 24), (22, 24), (21, 23), (20, 22), (23, 24), (21, 22), (20, 23), 
             (22, 23), (20, 21), (4, 24), (14, 24), (3, 23), (13, 23), (2, 22), (12, 22), (1, 21), (11, 21), 
             (0, 20), (10, 20), (5, 15), (15, 20), (6, 16), (16, 21), (7, 17), (17, 22), (8, 18), (18, 23), 
             (9, 19), (19, 24), (0, 10), (0, 15), (5, 10), (10, 15), (1, 11), (1, 16), (6, 11), (11, 16), 
             (2, 12), (2, 17), (7, 12), (12, 17), (3, 13), (3, 18), (8, 13), (13, 18), (4, 14), (4, 19), (9, 14), 
             (14, 19), (19, 22), (22, 23), (14, 20), (13, 16), (4, 9), (9, 15), (15, 21), (18, 21), (19, 20), 
             (20, 21), (21, 22), (20, 21), (4, 10), (10, 14), (3, 8), (8, 11), (11, 13), (2, 7), (7, 10), 
             (10, 12), (12, 14), (14, 17), (3, 9), (9, 11), (11, 12), (12, 13), (13, 15), (15, 16), (16, 17), 
             (17, 18), (18, 19), (19, 20), (17, 18), (13, 14), (14, 15), (15, 16), (16, 17), (15, 16), (12, 13), 
             (13, 14), (14, 15), (10, 11), (11, 12), (12, 13), (8, 9), (9, 10), (10, 11), (7, 8), (8, 9), (1, 6), 
             (3, 6), (6, 7), (0, 5), (2, 5), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9), (9, 10), (3, 4), (1, 3), 
             (3, 4), (4, 5), (1, 2)], 
        sections=[('input sorters', 0), ('final merging network', 45)]
    )

if __name__ == "__main__":
    if False:
        s5x5 = from_scratch(premerge=True)
    else:
        s5x5 = best_known()
        s5x5.normalize("median_first_lower_indices_last", ["final merging network"])
    print("Number of operations", s5x5.nops())
    print("Operations in 5x5 upper half sorted filter loop", s5x5.nops(list(range(12, 25))) - 9*4)
    print("Operations in 5x5 median filter loop", s5x5.nops([12]) - 9*4)
    print(s5x5)
    passed, failed = s5x5.test(product(*([[0,1]]*25)))
    print("passed", passed, "failed", failed)
