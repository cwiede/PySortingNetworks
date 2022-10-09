from itertools import product
from PySortingNetworks.Base import BaseSortingNetwork
from PySortingNetworks.OptimalSorters import sort
from PySortingNetworks import AutoCompleter

def from_scratch():
    # optimal sorters for the 3x3 inputs
    res = BaseSortingNetwork(0)
    res.section("input sorters")
    res = BaseSortingNetwork.append(res, sort(3))
    res = BaseSortingNetwork.append(res, BaseSortingNetwork.relabel(sort(3), list(range(3,6))))
    res = BaseSortingNetwork.append(res, BaseSortingNetwork.relabel(sort(3), list(range(6,9))))
    
    res.section("intermediate network")
    # intermediate layer
    res = BaseSortingNetwork.append(res, BaseSortingNetwork.relabel(sort(3), [0,3,6]))
    res = BaseSortingNetwork.append(res, BaseSortingNetwork.relabel(sort(3), [1,4,7]))
    res = BaseSortingNetwork.append(res, BaseSortingNetwork.relabel(sort(3), [2,5,8]))
    
    res.section("f network")
    # trial and error for the remaining network
    def geninputs():
        for n1, n2, n3 in product(list(range(4)), list(range(4)), list(range(4))):
            d_in = [0]*(3-n1) + [1]*n1 + [0]*(3-n2) + [1]*n2 + [0]*(3-n3) + [1]*n3
            yield d_in

    best = None
    nodeOfInterest = [4,5,6,7,8]
    for i in range(100):
        sn = AutoCompleter.randbest5(res, geninputs)
        sn.prune(geninputs, ["intermediate network", "f network"])
        sn.normalize("lower_indices_last", ["intermediate network", "f network"])
        #print("ops after pruning:", sn.nops())
        if best is None or sn.nops(nodeOfInterest) < best.nops(nodeOfInterest) or (sn.nops(nodeOfInterest) == best.nops(nodeOfInterest) and sn.nops() < best.nops()):
            best = sn
    passed,failed = best.test(geninputs())
    print("passed", passed, "failed", failed)
    
    return best

def best_known():
    return BaseSortingNetwork(
        n=9, 
        ops=[(0, 2), (1, 2), (0, 1), (3, 5), (4, 5), (3, 4), (6, 8), (7, 8), (6, 7), (2, 8), (5, 8), (1, 7), (4, 7), (0, 6), (3, 6), (2, 5), (5, 7), (2, 6), (5, 6), (1, 4), (2, 4), (4, 5), (0, 3), (1, 3), (2, 3)], 
        sections=[('input sorters', 0), ('intermediate network', 9), ('f network', 18)]
    )
    

if __name__ == "__main__":
    s3x3 = best_known()
    print("Best known 3x3 median network with upper half sorted")
    print("Number of operations", s3x3.nops())
    print("Operations in 3x3 median filter loop", s3x3.nops(list(range(4, 9))) - 2*3)
    print(s3x3)
    print(repr(s3x3))
    print("Testing ...", end="", flush=True)
    passed, failed = s3x3.test(product(*([[0,1]]*9)))
    print("passed", passed, "failed", failed)
    print()
    print("Generating a new network")
    s3x3 = from_scratch()
    print("Result from current operation")
    print("Number of operations", s3x3.nops())
    print("Operations in 3x3 median filter loop", s3x3.nops(list(range(4, 9))) - 2*3)
    print(s3x3)
    print(repr(s3x3))
