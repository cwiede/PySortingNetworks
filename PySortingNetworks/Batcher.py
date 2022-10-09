from itertools import product
from PySortingNetworks.Base import BaseSortingNetwork
from PySortingNetworks.OptimalSorters import sort

def next_power2(n):
    res = 1
    while res < n:
        res *= 2
    return res

def batcher_sort(n):
    if n <= 1:
        res = BaseSortingNetwork(n)
    elif n == 2:
        res = BaseSortingNetwork(2, ops=[(0,1)])
    else:
        virtual_lanes = next_power2(n) - n
        vl_low = virtual_lanes//2
        vl_high = virtual_lanes - vl_low
        n += virtual_lanes
        # we set virtual lanes at the end (we can assume that the values of these lanes are larger than any other values)
        # these lanes will be removed at the end of the merge
        s1 = batcher_sort(n//2)
        s2 = BaseSortingNetwork.relabel(batcher_sort(n-n//2), list(range(n//2,n)))
        m = batcher_merge_p2(n)
        res = BaseSortingNetwork.append(s1, s2)
        res = BaseSortingNetwork.append(res, m)
        new_ops = []
        for i, j in res.ops:
            if vl_low <= i < n - vl_high and vl_low <= j < n - vl_high:
                # avoid having the same operation twice
                if len(new_ops) == 0 or new_ops[-1] != (i-vl_low,j-vl_low):
                    new_ops.append((i-vl_low,j-vl_low))
        res.ops = new_ops
        res.nodes = list(range(n-virtual_lanes))
        res.n -= virtual_lanes
        res.sections = None
    return res

def batcher_merge_p2(n):
    if n <= 1:
        return BaseSortingNetwork(n)
    if n == 2:
        return BaseSortingNetwork(2, ops=[(0,1)])
    idx_even = list(range(0, n, 2))
    idx_odd = list(range(1, n, 2))
    even = BaseSortingNetwork.relabel(batcher_merge_p2(len(idx_even)), idx_even)
    odd = BaseSortingNetwork.relabel(batcher_merge_p2(len(idx_odd)), idx_odd)
    res = BaseSortingNetwork.append(even, odd)
    for i in range(1, n-1, 2):
        res.P( i, i+1 )
    return res

def batcher_merge(k, m):
    n = max(next_power2(k), next_power2(m))
    vl_low = n-k
    vl_high = n-m
    n = vl_low + k + m + vl_high
    res = batcher_merge_p2(n)
    new_ops = []
    for i, j in res.ops:
        if vl_low <= i < n - vl_high and vl_low <= j < n - vl_high:
            # avoid having the same operation twice
            if len(new_ops) == 0 or new_ops[-1] != (i-vl_low,j-vl_low):
                new_ops.append((i-vl_low,j-vl_low))
    res.ops = new_ops
    res.nodes = list(range(k+m))
    res.n = k+m
    def geninput():
        for n1, n2 in product(range(k+1), range(m+1)):
            yield [0]*(k-n1) + [1]*n1 + [0]*(m-n2) + [1]*n2
    #assert res.test(geninput())[1] == 0
    res.prune(geninput)
    return res

if __name__ == "__main__":
    def geninput(n):
        for i in product(*([[0,1]]*n)):
            yield i
    for n in range(26):
        sn = batcher_sort(n)
        npruned = sn.prune(lambda: geninput(n))
        print("Batcher", n, "Num Operations:", sn.nops(), "(pruned=", npruned, ")")
        print(sn)
        passed, failed = sn.test(geninput(n))
        print("Test passed", passed, "failed", failed)
        assert failed == 0
