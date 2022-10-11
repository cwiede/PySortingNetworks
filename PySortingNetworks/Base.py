class BaseSortingNetwork:
    def __init__(self, n, ops=None, sections=None):
        assert n >= 0
        self.n = n
        self.nodes = list(range(n))
        self.ops = []
        self.sections = None
        if ops is not None:
            for i,j in ops:
                self.P(i, j)
        self.sections = sections
        
    def nops(self, nodes=None):
        if nodes is None:
            return len(self.ops)
        res = len(self.ops)
        while True:
            if self.ops[res-1][0] in nodes or self.ops[res-1][1] in nodes or res == 0:
                break
            else:
                res -= 1
        for i,j in self.ops[res:]:
            assert i not in nodes and j not in nodes
        return res
        
    def section(self, name):
        if self.sections is None:
            if len(self.ops) > 0:
                self.sections = [("<unnamed>", 0)]
            else:
                self.sections = []
        self.sections.append( (name, len(self.ops)) )
        
    def focus(self, sections):
        assert self.sections is not None
        for idx in list(range(len(self.sections)))[::-1]:
            name, opidx = self.sections[idx]
            if not name in sections:
                nextOpIdx = self.sections[idx+1][1] if idx < len(self.sections)-1 else len(self.ops)
                self.ops = self.ops[:opidx] + self.ops[nextOpIdx:]
        self.sections = None
        
    def P(self, i, j):
        """swap elements i and j if comparison result is unsorted"""
        assert i in self.nodes and j in self.nodes and i != j
        self.ops.append( (i,j) )
        
    def __str__(self):
        """return ascii art of the network"""
        cols = [(("%3d: "%self.nodes[k])+chr(0x2500)) for k in range(self.n)]
        secIdx = 0
        for opidx, (i,j) in enumerate(self.ops):
            if self.sections is not None and secIdx < len(self.sections):
                if opidx == self.sections[secIdx][1]:
                    secIdx += 1
                    for k in range(len(cols)):
                        cols[k] += chr(0x250a)
            for k in range(min(i,j)):
                cols[k] += chr(0x2500) if k != self.n//2 else chr(0x2501)
            if i < j:
                cols[i] += chr(0x252c) if i != self.n//2 else chr(0x252f)
                for k in range(i+1, j):
                    cols[k] += chr(0x253c) if k != self.n//2 else chr(0x253f)
                cols[j] += chr(0x2534) if j != self.n//2 else chr(0x2537)
            else:
                cols[j] += chr(0x2530) if j != self.n//2 else chr(0x2533)
                for k in range(j+1, i):
                    cols[k] += chr(0x2542) if k != self.n//2 else chr(0x254b)
                cols[i] += chr(0x2538) if i != self.n//2 else chr(0x253b)
            for k in range(max(i,j)+1, len(cols)):
                cols[k] += chr(0x2500) if k != self.n//2 else chr(0x2501)
        return repr(self) + "\n" + ("\n".join(cols))
    
    def __repr__(self):
        return f"""
BaseSortingNetwork(
    n={self.n}, 
    ops={self.ops}, 
    sections={self.sections}
)"""
    
    def execute(self, d_in):
        assert len(d_in) == self.n
        assert self.nodes == list(range(self.n))
        a = list(d_in[:])
        for i,j in self.ops:
            if a[i] > a[j]:
                a[i], a[j] = a[j], a[i]
        return a
    
    def execute_stat(self, d_in, stat):
        assert len(stat) == len(self.ops)
        assert len(d_in) == self.n
        assert self.nodes == list(range(self.n))
        a = list(d_in[:])
        for opidx, (i,j) in enumerate(self.ops):
            if a[i] > a[j]:
                a[i], a[j] = a[j], a[i]
                stat[opidx] += 1
        return a        
    
    def test(self, inputs, callback_if_failed=None, callback_if_passed=None):
        """tests the network for each input yielded by the generator and gather statistics"""
        passed = 0
        failed = 0
        for d_in in inputs:
            d_out = self.execute(d_in)
            if not all(d_out[i] <= d_out[i+1] for i in range(self.n-1)):
                failed += 1
                if callback_if_failed is not None:
                    callback_if_failed(d_in, d_out)
            else:
                passed += 1
                if callback_if_passed is not None:
                    callback_if_passed(d_in, d_out)
        return passed, failed
    
    def opidx2secname(self):
        res = None
        if self.sections is not None:
            res = {}
            for sidx in range(len(self.sections)):
                name, opidx0 = self.sections[sidx]
                opidx1 = self.sections[sidx+1][1] if sidx+1 < len(self.sections) else len(self.ops)
                for opidx in range(opidx0, opidx1):
                    res[opidx] = name
        return res
    
    def prune(self, input_generator, sections=None):
        seqidx = 0
        opidx2secname = self.opidx2secname()
        if self.sections is not None:
            if sections is None:
                sections = [name for name, _ in self.sections]
            for s in sections:
                assert s in [name for name, _ in self.sections]
        else:
            assert sections is None
        stats = [0] * len(self.ops)
        for d_in in input_generator():
            d_out = self.execute_stat(d_in, stats)
        indices = list(range(len(self.ops)))[::-1]
        numPruned = 0
        for opidx in indices:
            if stats[opidx] == 0 and (opidx2secname is None or opidx2secname[opidx] in sections):
                # opidx can be removed because it was a noop
                numPruned += 1
                self.ops = self.ops[:opidx] + self.ops[opidx+1:]
                if self.sections is not None:
                    # check if we need to adapt the section indices
                    newsections = []
                    for name, idx in self.sections:
                        if idx == opidx:
                            newsections.append( (name, idx+1) )
                        elif idx > opidx:
                            newsections.append( (name, idx-1) )
                        else:
                            newsections.append( (name, idx) )
        return numPruned
    
    def normalize(self, method, sections=None):
        if sections is None and self.sections is not None:
            sections = [name for name, _ in self.sections]
        if method == "lower_indices_last":
            opidx2secname = self.opidx2secname()
            changed = True
            while changed:
                changed = False
                for i in range(len(self.ops)-1):
                    if opidx2secname is None or (opidx2secname[i] in sections and opidx2secname[i+1] in sections):
                        i0, i1 = self.ops[i]
                        j0, j1 = self.ops[i+1]
                        if j1 > i1:
                            # we'd like to swap the elements if possible
                            if i0 != j0 and i0 != j1 and i1 != j0 and i1 != j1:
                                self.ops[i], self.ops[i+1] = self.ops[i+1], self.ops[i]
                                changed = True
            return
        if method == "higher_indices_last":
            opidx2secname = self.opidx2secname()
            changed = True
            while changed:
                changed = False
                for i in range(len(self.ops)-1):
                    if opidx2secname is None or (opidx2secname[i] in sections and opidx2secname[i+1] in sections):
                        i0, i1 = self.ops[i]
                        j0, j1 = self.ops[i+1]
                        if j0 < i0:
                            # we'd like to swap the elements if possible
                            if i0 != j0 and i0 != j1 and i1 != j0 and i1 != j1:
                                self.ops[i], self.ops[i+1] = self.ops[i+1], self.ops[i]
                                changed = True
            return            
        if method == "non_median_last":
            opidx2secname = self.opidx2secname()
            idx_median = self.n // 2
            changed = True
            while changed:
                last_median_idx = 0
                for i in range(len(self.ops)):
                    i0, i1 = self.ops[i]
                    if i0 == idx_median or i1 == idx_median:
                        last_median_idx = i
                for start in range(len(self.ops)-2):
                    for i in range(start, len(self.ops)-1):
                        if opidx2secname is None or (opidx2secname[i] in sections and opidx2secname[i+1] in sections):
                            i0, i1 = self.ops[i]
                            j0, j1 = self.ops[i+1]
                            if i0 != idx_median and i1 != idx_median:
                                # we'd like to swap the elements if possible
                                if i0 != j0 and i0 != j1 and i1 != j0 and i1 != j1:
                                    self.ops[i], self.ops[i+1] = self.ops[i+1], self.ops[i]
                    curr_median_idx = 0
                    for i in range(len(self.ops)):
                        i0, i1 = self.ops[i]
                        if i0 == idx_median or i1 == idx_median:
                            curr_median_idx = i
                    changed = last_median_idx > curr_median_idx
                    if changed:
                        break
            return
        if method == "median_first_lower_indices_last":
            self.normalize("lower_indices_last", sections=sections)
            # fix the last indices
            fixed_from = len(self.ops)
            idx_median = self.n // 2
            while fixed_from > 0:
                i, j = self.ops[fixed_from-1]
                if i >= idx_median or j >= idx_median:
                    break
                fixed_from -= 1
            last_ops = self.ops[fixed_from:]
            self.ops = self.ops[:fixed_from]
            self.normalize("non_median_last", sections=sections)
            self.ops = self.ops + last_ops
            last_median_idx = None
            opidx2secname = self.opidx2secname()
            for k in range(len(self.ops)):
                i,j = self.ops[k]
                if i == idx_median or j == idx_median and (opidx2secname is None or opidx2secname[k] in sections):
                    last_median_idx = k+1
            first_ops = self.ops[:last_median_idx]
            self.ops = self.ops[last_median_idx:]
            self.normalize("lower_indices_last", sections=None)
            self.ops = first_ops + self.ops
            # add sections for median and upper half sorted positions
            last_median_idx = None
            last_upper_half_idx = None
            for k in range(len(self.ops)):
                i,j = self.ops[k]
                if i == idx_median or j == idx_median:
                    last_median_idx = k+1
                    last_upper_half_idx = k+1
                elif i > idx_median or j > idx_median:
                    last_upper_half_idx = k+1
            if last_median_idx is not None:
                self.sections.append( ("median", last_median_idx) )
            if last_upper_half_idx is not None:
                self.sections.append( ("last_upper_half_sorted", last_upper_half_idx) )
            self.sections.sort(key=lambda x: x[1])
            return
        raise RuntimeError("Unknown method %s" % method)
        
    def copy(self):
        res = BaseSortingNetwork(self.n)
        res.nodes = self.nodes[:]
        res.ops = self.ops[:]
        if self.sections is not None:
            res.sections = self.sections[:]
        return res
    
    @staticmethod
    def relabel(sn, node_map):
        res = BaseSortingNetwork(sn.n)
        res.nodes = [node_map[i] for i in sn.nodes]
        if sn.sections is not None:
            res.sections = sn.sections[:]
        for i,j in sn.ops:
            res.P(node_map[i], node_map[j])
        return res
    
    @staticmethod
    def append(sn1, sn2):
        if len(set(sn1.nodes) & set(sn2.nodes)) == 0:
            # intersection of nodes is empty
            res = BaseSortingNetwork(sn1.n + sn2.n)
            res.nodes = sn1.nodes + sn2.nodes
            res.nodes.sort()
            for i,j in sn1.ops + sn2.ops:
                res.P(i, j)
            if sn1.sections is not None:
                res.sections = sn1.sections[:]
            if sn2.sections is not None:
                if res.sections is None: res.sections = [("<unnamed>", 0)]
                for name, idx in sn2.sections:
                    res.sections.append( (name, sn1.n + idx) )
            return res
        if set(sn1.nodes) & set(sn2.nodes) == set(sn1.nodes):
            res = BaseSortingNetwork(sn2.n)
            res.nodes = sn2.nodes[:]
            for i,j in sn1.ops:
                res.P(i,j)
            for i,j in sn2.ops:
                res.P(i,j)
            if sn1.sections is not None:
                res.sections = sn1.sections[:]
            if sn2.sections is not None:
                if res.sections is None:
                    res.sections = [("<unnamed>", 0)]
                for name, idx in sn2.sections:
                    res.sections.append( (name, len(sn1.ops) + idx) )
            return res
        if set(sn1.nodes) & set(sn2.nodes) == set(sn2.nodes):
            res = BaseSortingNetwork(sn1.n)
            res.nodes = sn1.nodes[:]
            for i,j in sn1.ops:
                res.P(i,j)
            for i,j in sn2.ops:
                res.P(i,j)
            if sn1.sections is not None:
                res.sections = sn1.sections[:]
            if sn2.sections is not None:
                if res.sections is None:
                    res.sections = [("<unnamed>", 0)]
                for name, idx in sn2.sections:
                    res.sections.append( (name, len(sn1.ops) + idx) )
            return res
        raise RuntimeError("Don't know how to append both networks n1=%s n2=%s" % (sn1.nodes, sn2.nodes))
